import sandwichlib as sl


def main():
    '''Gets an order from a customer, records the order, and confirms it is correct.'''

    # Init the shop
    shop = sl.SandwichShop("Evan's Sandwich Shop")

    # Greet the customer
    shop.greeting()

    while True:
        # Ask if they want to see a menu
        affirmatives = {"yes", "yep", "yeah", "yes please", "yes, please", "please",
                        "yup", "y", "sure", "ok", "why not"}
        choice = input("Would you like to see the menu? (q to quit)\n")
        if choice == "q":
            print()
            print("Come again!")
            break

        # Assume anything other than an affirmative means no
        if choice.strip().lower() in affirmatives:
            shop.print_menu()
        print()

        # Ask what they want / Get order
        prompt = ("After the sandwich name, let me know if you want to substitute\n" +
                  "a different bread or spread, and any extra options you'd like.\n" +
                  "Please include exceptions at the end of your order.\n\n" +
                  "What can I get for you today? (q to quit)\n")
        order = input(prompt)
        if order == "q":
            print()
            print("Come again!")
            break

        # Process order
        try:
            parser = sl.OrderParser(shop.menu, order)
            (name, bread, spread, options, exceptions) = parser.get_order()
            sandwich = shop.make_sandwich(
                name, bread, spread, options, exceptions)
        except ValueError:
            print()
            print("Sorry, I didn't recognize the sandwich you ordered.")
            print("Please order again.")
            continue

        # Check everything is correct
        negatives = {"no", "nope", "nah", "n", "no thanks"}
        print()
        print("Let's make sure we got everything right. We have a:")
        sandwich.display()
        is_correct = input("Is that correct? (Type 'no' to reorder)\n")
        print()
        if is_correct.lower() in negatives:
            print("Sorry about that! Let me try again.")
            print()
            continue
        else:
            print("Great! We'll have that right out for you.")
            break


if __name__ == "__main__":
    main()
