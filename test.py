import pytest
from sandwichlib import SandwichShop
from sandwichlib import Sandwich
from sandwichlib import OrderParser


class TestShop:
    def test_greeting(self, capsys):
        shop = SandwichShop("Evan's Sandwich Shop")
        shop.greeting()
        captured = capsys.readouterr()
        assert captured.out == "Welcome to Evan's Sandwich Shop!\n"

    def test_default_values_on_sandwich_blt(self):
        shop = SandwichShop("Evan's Sandwich Shop")
        sandwich = shop.make_sandwich("Evan's BLT")
        assert sandwich.name == "Evan's BLT"
        assert sandwich.usual_ingredients == ["Bacon", "Lettuce", "Tomato"]
        assert sandwich.bread == "Pita"
        assert sandwich.spread == "Hummus"
        assert sandwich.options == []
        assert sandwich.exceptions == []

    def test_custom_values_on_sandwich_turkey_bacon(self):
        shop = SandwichShop("Evan's Sandwich Shop")
        sandwich = shop.make_sandwich("Turkey Bacon", "Whole Wheat", "Mayo",
                                      ["Toasted"], ["Tomato", "Avocado"])
        assert sandwich.usual_ingredients == [
            "Turkey", "Bacon", "Lettuce", "Tomato", "Avocado", "Swiss Cheese"]
        assert sandwich.bread == "Whole Wheat"
        assert sandwich.spread == "Mayo"
        assert sandwich.options == ["Toasted"]
        assert sandwich.exceptions == ["Tomato", "Avocado"]


class TestSandwich:

    def test_print_sandwich(self, capsys):
        sandwich = Sandwich("My Sandwich",
                            ["Turkey", "Lettuce", "Avocado", "Swiss Cheese"],
                            "White",
                            "Dijon",
                            ["Toasted", "Extra Cheese"],
                            ["Lettuce"])

        sandwich.display()
        captured = capsys.readouterr()
        assert captured.out == "My Sandwich with Turkey, Avocado, Swiss Cheese on White with Dijon. Toasted, Extra Cheese.\n"


class TestOrderParser:

    menu = SandwichShop("").menu

    def test_extract_order(self):
        order = "Can I get the blt sandwich on white bread with Mustard, I'd like that toasted with extra meat. No tomatoes, please"
        parser = OrderParser(self.menu, order)
        (name, bread, spread, options, exceptions) = parser.get_order()

        assert name == "Evan's BLT"
        assert bread == "White"
        assert spread == "Dijon Mustard"
        assert options == ["Toasted", "Extra Meat"]
        assert exceptions == ["Tomato", "Please"]

    def test_clean_order(self):
        parser = OrderParser(self.menu,
                             "ThIs. SHOULD, be: LoWeRCaSe, -BLt-, WIThout puncTUATION!")
        assert parser.cleaned_order == "this should be lowercase blt without punctuation"

    def test_get_name_success(self):
        parser = OrderParser(self.menu, "blt")

        order = "hello here is blt a sandwich title"
        name = parser._get_name(order)
        assert name == "Evan's BLT"

        order = "hello here is turkey a sandwich title"
        name = parser._get_name(order)
        assert name == "Turkey Bacon"

        order = "hello here is ham a sandwich title"
        name = parser._get_name(order)
        assert name == "Classic Ham"

        order = "hello here is italian a sandwich title"
        name = parser._get_name(order)
        assert name == "Italian"

    def test_get_name_failure(self):
        parser = OrderParser(self.menu, "turkey")

        with pytest.raises(ValueError):
            order = "this will match nothing"
            parser._get_name(order)

    def test_get_bread_chosen(self):
        parser = OrderParser(self.menu, "ham")

        order = "hello id like white bread"
        bread = parser._get_bread(order)
        assert bread == "White"

        order = "hello id like wheat bread"
        bread = parser._get_bread(order)
        assert bread == "Wheat"

        order = "hello id like a pita"
        bread = parser._get_bread(order)
        assert bread == "Pita"

    def test_get_bread_default(self):
        order = "this order has no bread option"

        parser = OrderParser(self.menu, "blt")
        bread = parser._get_bread(order)
        assert bread == "Pita"

        parser = OrderParser(self.menu, "italian")
        bread = parser._get_bread(order)
        assert bread == "White"

    def test_get_spread_chosen(self):
        parser = OrderParser(self.menu, "blt")

        order = "hello id like hummus spread"
        spread = parser._get_spread(order)
        assert spread == "Hummus"

        order = "hello id like mayo spread"
        spread = parser._get_spread(order)
        assert spread == "Mayonnaise"

        order = "hello id like mayonnaise on my sandie"
        spread = parser._get_spread(order)
        assert spread == "Mayonnaise"

        order = "hello id like dijon on my sandie"
        spread = parser._get_spread(order)
        assert spread == "Dijon Mustard"

        order = "hello id like mustard on my sandie"
        spread = parser._get_spread(order)
        assert spread == "Dijon Mustard"

    def test_get_spread_default(self):
        order = "this order has no spread option"

        parser = OrderParser(self.menu, "blt")
        spread = parser._get_spread(order)
        assert spread == "Hummus"

        parser = OrderParser(self.menu, "italian")
        spread = parser._get_spread(order)
        assert spread == "Mayonnaise"

    def test_options(self):
        parser = OrderParser(self.menu, "turkey")

        order = "i want that toasted with extra cheese extra meat and extra spread"
        options = parser._get_options(order)
        assert options == ["Toasted", "Extra Meat",
                           "Extra Cheese", "Extra Spread"]

        order = "no extras thanks"
        options = parser._get_options(order)
        assert options == []

    def test_exceptions(self):
        parser = OrderParser(self.menu, "italian")

        order = "i want a blt with some stuff but no provolone lettuce or ahhh you know tomatoes"
        exceptions = parser._get_exceptions(order)
        assert exceptions == ["Provolone Cheese", "Lettuce",
                              "Or", "Ahhh", "You", "Know", "Tomato"]

        order = "i want a blt with some stuff hold the swiss lettuce or ahhh you know tomato"
        exceptions = parser._get_exceptions(order)
        assert exceptions == ["Swiss Cheese", "Lettuce",
                              "Or", "Ahhh", "You", "Know", "Tomato"]

        order = "i want a blt with some stuff but without cheddar lettuce or ahhh you know tomato"
        exceptions = parser._get_exceptions(order)
        assert exceptions == ["Cheddar Cheese", "Lettuce",
                              "Or", "Ahhh", "You", "Know", "Tomato"]

        order = "i want a blt with some stuff minus cheese lettuce or ahhh you know tomato"
        exceptions = parser._get_exceptions(order)
        assert exceptions == ["Swiss Cheese", "Cheddar Cheese", "Provolone Cheese",
                              "Lettuce", "Or", "Ahhh", "You", "Know", "Tomato"]

        order = "i want a blt with some stuff except cheese lettuce or ahhh you know tomato"
        exceptions = parser._get_exceptions(order)
        assert exceptions == ["Swiss Cheese", "Cheddar Cheese", "Provolone Cheese",
                              "Lettuce", "Or", "Ahhh", "You", "Know", "Tomato"]

        order = "there arent any keywords here"
        exceptions = parser._get_exceptions(order)
        assert exceptions == []
