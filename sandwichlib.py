import re
import string


def print_list(lst):
    '''Prints a list as comma seperated values, without brackets or quotes.'''
    if len(lst) == 0:
        return

    print(lst[0], end="")
    for i in range(1, len(lst)):
        print(",", lst[i], end="")


class Sandwich:
    '''A simple representation of a sandwich'''

    def __init__(self,
                 name: str,
                 usual_ingredients: [str],
                 bread: str,
                 spread: str,
                 options: [str],
                 exceptions: [str]) -> None:
        self.name = name
        self.usual_ingredients = usual_ingredients
        self.bread = bread
        self.spread = spread
        self.options = options
        self.exceptions = exceptions

    def display(self):
        print(self.name, "with", end=" ")
        ingredients = [
            x for x in self.usual_ingredients if x not in self.exceptions]
        print_list(ingredients)
        print(" on", self.bread, "with", self.spread, end="")
        if len(self.options) > 0:
            print(". ", end="")
            print_list(self.options)
        print(".")


class SandwichShop:
    '''Represents the sandwich shop'''

    def __init__(self, name: str) -> None:
        self.name = name

        # This represents the knowledge base for sandwiches.
        self.menu = {
            # Name: ([ingredients], default bread, default spread)
            "Evan's BLT": (["Bacon", "Lettuce", "Tomato"],
                           "Pita",
                           "Hummus"),
            "Turkey Bacon": (["Turkey", "Bacon", "Lettuce", "Tomato", "Avocado", "Swiss Cheese"],
                             "White",
                             "Mayonnaise"),
            "Classic Ham": (["Ham", "Lettuce", "Tomato", "Onion", "Cheddar Cheese"],
                            "White",
                            "Dijon Mustard"),
            "Italian": (["Ham", "Salami", "Pepperoni", "Lettuce", "Tomato", "Onion", "Provolone Cheese"],
                        "White",
                        "Mayonnaise")
        }

        self.breads = ["White", "Whole Wheat", "Pita"]
        self.spreads = ["Mayonnaise", "Dijon Mustard", "Hummus"]
        self.options = ["Toasted", "Extra Cheese",
                        "Extra Meat", "Extra Spread"]

    def greeting(self):
        '''Simple greeting'''
        print("Welcome to ", self.name, "!", sep="")

    def print_menu(self):
        '''Displays the shop menu'''
        print("          MENU          ")
        print("------------------------")
        print("Sandwiches")
        for name, (ingredients, bread, spread) in self.menu.items():
            print(name)
            print("\t", end="")
            for ingredient in ingredients:
                print(ingredient + ", ", end="")
            print("on", bread, "bread with", spread)

        print()
        print("Substitute bread or spread at no cost")
        print()

        print("Choice of breads")
        print("\t", end="")
        print_list(self.breads)
        print()

        print("Choice of spreads")
        print("\t", end="")
        print_list(self.spreads)
        print()

        print()
        print("Upgrade your sandwich with the following options:")
        print("\t", end="")
        print_list(self.options)
        print()

    def make_sandwich(self, name: str, bread="", spread="", options=[], exceptions=[]) -> Sandwich:
        '''Makes a sandwich.

        Name will specify the type of sandwich and default options.
        If bread or spread are not specified default options will be chosen.
        Can specify options for the sandwich, such as 'toasted' in options.
        Can specify exceptions for the sandwich, such as 'no tomato', in exceptions.
        '''
        if bread == "":
            bread = self.menu[name][1]
        if spread == "":
            spread = self.menu[name][2]

        usual_ingredients = self.menu[name][0]

        return Sandwich(name, usual_ingredients, bread, spread, options, exceptions)


class OrderParser:

    def __init__(self, menu: dict, order: str) -> None:
        self.menu = menu
        self.raw_order = order
        self.cleaned_order = self._remove_punctuation(order.strip().lower())

        self.name = self._get_name(self.cleaned_order)
        self.bread = self._get_bread(self.cleaned_order)
        self.spread = self._get_spread(self.cleaned_order)
        self.options = self._get_options(self.cleaned_order)
        self.exceptions = self._get_exceptions(self.cleaned_order)

    def get_order(self) -> (str, str, str, {str}, {str}):
        '''Returns an organized order from a customer's typed order.'''
        return (self.name, self.bread, self.spread, self.options, self.exceptions)

    def _get_name(self, order: str) -> str:
        '''Gets the name of the sandwich ordered. This is not at all scaleable, nor robust.'''
        name = re.search("blt", order)
        if name:
            return "Evan's BLT"

        name = re.search("turkey", order)
        if name:
            return "Turkey Bacon"

        name = re.search("ham", order)
        if name:
            return "Classic Ham"

        name = re.search("italian", order)
        if name:
            return "Italian"

        raise ValueError("Could not find a name in the order")

    def _get_bread(self, order: str) -> str:
        '''Gets the bread'''
        bread = re.search("white", order)
        if bread:
            return "White"

        bread = re.search("wheat", order)
        if bread:
            return "Wheat"

        bread = re.search("pita", order)
        if bread:
            return "Pita"

        # Get default choice if bread not specified
        return self.menu[self.name][1]

    def _get_spread(self, order: str) -> str:
        '''Gets the spread'''
        spread = re.search("mayo|mayonnaise", order)
        if spread:
            return "Mayonnaise"

        spread = re.search("dijon|mustard", order)
        if spread:
            return "Dijon Mustard"

        spread = re.search("hummus", order)
        if spread:
            return "Hummus"

        # Get default choice if spread not specified
        return self.menu[self.name][2]

    def _get_options(self, order: str) -> [str]:
        '''Gets the options for the sandwich.'''
        final_options = []

        option = re.search("toasted|toast", order)
        if option:
            final_options.append("Toasted")

        option = re.search("extra meat", order)
        if option:
            final_options.append("Extra Meat")

        option = re.search("extra cheese", order)
        if option:
            final_options.append("Extra Cheese")

        option = re.search("extra spread", order)
        if option:
            final_options.append("Extra Spread")

        return final_options

    def _get_exceptions(self, order: str) -> [str]:
        '''Gets exceptions from an order.
        All exceptions must come at the end of the order. After seeing an exception
        keyword, everything is treated as an exception. These are never printed,
        but used as a filter.
        '''
        exceptions = []

        # Split the string at the first occurrence of an exception keyword
        ex_string = re.split(
            "no|hold the|without|minus|except|I don't want", order, 1)
        if len(ex_string) == 1:
            # No exceptions
            return exceptions
        else:
            # Get the last part of the string and split that into words
            ex_string = ex_string[1].split()

        # Add all words to exceptions as title case
        # Check for a few special cases
        for word in ex_string:
            if word == "tomatoes":
                exceptions.append("Tomato")

            elif word == "onions":
                exceptions.append("Onion")

            elif word == "mayo":
                exceptions.append("Mayonnaise")

            elif word == "cheese":
                exceptions.append("Swiss Cheese")
                exceptions.append("Cheddar Cheese")
                exceptions.append("Provolone Cheese")

            elif word == "swiss" or word == "cheddar" or word == "provolone":
                word = (word + " cheese").title()
                exceptions.append(word)

            else:
                exceptions.append(word.title())

        return exceptions

    def _remove_punctuation(self, order: str) -> str:
        '''Removes any punctuation from a string.'''
        return order.translate(str.maketrans('', '', string.punctuation))
