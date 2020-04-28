# nlp-sandwich-shop
An exercise in using simple, low-level techniques to parse typed natural language in the context of a sandwich ordering system. This exercise was created as part of an introductory AI class at Northeastern University.

To run the program, clone this directory, navigate to it, and run `python sandwich.py` or `python3 sandwich.py`, depending on your system (you need to use Python 3; I used Python 3.8). You can also see example runs of the program at the bottom of this README.

If you follow the prompts of the program, it should guide you through the process. You can write in *mostly* natural language. The order only needs to have the sandwich name first, followed by bread, spread and option choices. Exceptions should be at the end of the order. Be sure not to use any of the exception keywords before this section (described further below). Everything after the first occurrence of one of these words will be considered an exception. This is also why exceptions are not printed in full, but used as a filter for ingredients instead.

---

A description of the hypothetical sandwich shop follows:

## Sandwiches Offered

Evan's BLT: Bacon, Lettuce, Tomato in a Pita wrap with Hummus

Turkey Bacon: Turkey, Bacon, Lettuce, Tomato, Avocado, Swiss cheese on White bread with Mayo

Classic Ham: Ham, Lettuce, Tomato, Onion, Cheddar cheese, on White bread with Dijon Mustard

Italian: Ham, Salami, Pepperoni, Lettuce, Tomato, Onion, Provolone cheese on White bread with Mayo

### Options

* Bread Options: White, Whole Wheat & Pita
* Spread Options: Mayo/Mayonnaise, Dijon Mustard & Hummus
* General Options: Toasted, Extra Cheese, Extra Meat, Extra Spread
* Any exceptions are possible. If a customer wants to pay for a single ingredient, or nothing, we won't stop them.

## Handling Orders

All of the following will be case insensitive.

If customers do not mention a bread or spread, it will be assumed that they want
the default options. The defaults are written on the menu, and customers would not want to 
specify those options if that is what they want. However, they will be told when ordering that they can
substitute any bread or spread at no cost.

Exceptions will not be shown to the customer. Instead, usual ingredients will be listed without the exceptions
specified. It is reasonable to assume that customers will be able to tell if their exception is still listed.

### Equivalent Terms

* {Evan's BLT, Evans BLT, Evan BLT, BLT}
* {Turkey Bacon, Turkey}
* {Classic Ham, Ham}
* {Mayo, Mayonnaise}
* {Dijon, Dijon Mustard, Mustard}
* {Whole Wheat, Wheat, Wheat}
* {Tomato, Tomatoes}
* {Onion, Onions}
* {sub, substitute}
* {yes, yep, yup, yeah, sure, ok, y, why not}
* {no, nope, nah, n, no thanks}

### Ignored Words

Please, Thanks, Sandwich, Bread, I'd like the, I'd like that, I want the, Can I have the, but, with, on, and, Can I get it, <any-punctuation>

Some of the equivalent terms above will be essentially ignored. For example, if someone orders 
the BLT, the words Evan's, Evans, and Evan can be ignored. Similarly, if someone asks for no cheese,
the type of cheese does not matter.

### Exception Formatting

* Hold the ...
* no ...
* without ...
* minus ...
* except ...

## Examples

As stated earlier, this system does not check with the customer if they leave out which bread or spread they want. It would be annoying to customers who want the defaults to have to specify them, and those who don't will ask for the substitutions. However, the system will always check that it got the correct order, and allow the customer to reorder if they want.

### Example 1 - User makes a default choice then changes their mind

```
Welcome to Evan's Sandwich Shop!
Would you like to see the menu? (q to quit)
sure
          MENU          
------------------------
Sandwiches
Evan's BLT
	Bacon, Lettuce, Tomato, on Pita bread with Hummus
Turkey Bacon
	Turkey, Bacon, Lettuce, Tomato, Avocado, Swiss Cheese, on White bread with Mayonnaise
Classic Ham
	Ham, Lettuce, Tomato, Onion, Cheddar Cheese, on White bread with Dijon Mustard
Italian
	Ham, Salami, Pepperoni, Lettuce, Tomato, Onion, Provolone Cheese, on White bread with Mayonnaise

Substitute bread or spread at no cost

Choice of breads
	White, Whole Wheat, Pita
Choice of spreads
	Mayonnaise, Dijon Mustard, Hummus

Upgrade your sandwich with the following options:
	Toasted, Extra Cheese, Extra Meat, Extra Spread

After the sandwich name, let me know if you want to substitute
a different bread or spread, and any extra options you'd like.
Please include exceptions at the end of your order.

What can I get for you today? (q to quit)
I'd like the BLT, please

Let's make sure we got everything right. We have a:
Evan's BLT with Bacon, Lettuce, Tomato on Pita with Hummus.
Is that correct? (Type 'no' to reorder)
no

Sorry about that! Let me try again.

Would you like to see the menu? (q to quit)
no

After the sandwich name, let me know if you want to substitute
a different bread or spread, and any extra options you'd like.
Please include exceptions at the end of your order.

What can I get for you today? (q to quit)
Actually, could I have the BLT but on white bread with mayo? I'd also like that toasted, please.

Let's make sure we got everything right. We have a:
Evan's BLT with Bacon, Lettuce, Tomato on White with Mayonnaise. Toasted.
Is that correct? (Type 'no' to reorder)
yes

Great! We'll have that right out for you.
```

### Example 2 - Customer specifies only the bread to substitute

```
Welcome to Evan's Sandwich Shop!
Would you like to see the menu? (q to quit)
nah

After the sandwich name, let me know if you want to substitute
a different bread or spread, and any extra options you'd like.
Please include exceptions at the end of your order.

What can I get for you today? (q to quit)
Gimme the classic ham on whole wheat bread. Extra cheese and extra meat. Hold the onions and tomatoes.

Let's make sure we got everything right. We have a:
Classic Ham with Ham, Lettuce, Cheddar Cheese on Wheat with Dijon Mustard. Extra Meat, Extra Cheese.
Is that correct? (Type 'no' to reorder)
looks good!

Great! We'll have that right out for you.
```

### Example 3 - Customer specifies only the spread to substitute

```
Welcome to Evan's Sandwich Shop!
Would you like to see the menu? (q to quit)
ok
          MENU          
------------------------
Sandwiches
Evan's BLT
	Bacon, Lettuce, Tomato, on Pita bread with Hummus
Turkey Bacon
	Turkey, Bacon, Lettuce, Tomato, Avocado, Swiss Cheese, on White bread with Mayonnaise
Classic Ham
	Ham, Lettuce, Tomato, Onion, Cheddar Cheese, on White bread with Dijon Mustard
Italian
	Ham, Salami, Pepperoni, Lettuce, Tomato, Onion, Provolone Cheese, on White bread with Mayonnaise

Substitute bread or spread at no cost

Choice of breads
	White, Whole Wheat, Pita
Choice of spreads
	Mayonnaise, Dijon Mustard, Hummus

Upgrade your sandwich with the following options:
	Toasted, Extra Cheese, Extra Meat, Extra Spread

After the sandwich name, let me know if you want to substitute
a different bread or spread, and any extra options you'd like.
Please include exceptions at the end of your order.

What can I get for you today? (q to quit)
Let's see... ummm can I get the Italian? But I want it with mustard. Also I want extra spread. But I want it without pepperoni and no cheese

Let's make sure we got everything right. We have a:
Italian with Ham, Salami, Lettuce, Tomato, Onion on White with Dijon Mustard. Extra Spread.
Is that correct? (Type 'no' to reorder)


Great! We'll have that right out for you.
```

### Example 4 - The Customer orders something that isn't on the menu and gets in a loop until quitting.

```
Welcome to Evan's Sandwich Shop!
Would you like to see the menu? (q to quit)


After the sandwich name, let me know if you want to substitute
a different bread or spread, and any extra options you'd like.
Please include exceptions at the end of your order.

What can I get for you today? (q to quit)
I want a burger, ya hear!?!

Sorry, I didn't recognize the sandwich you ordered.
Please order again.
Would you like to see the menu? (q to quit)
Nah, I'm going to McDonald's

After the sandwich name, let me know if you want to substitute
a different bread or spread, and any extra options you'd like.
Please include exceptions at the end of your order.

What can I get for you today? (q to quit)
I said I'm leaving!!!

Sorry, I didn't recognize the sandwich you ordered.
Please order again.
Would you like to see the menu? (q to quit)
q

Come again!
```

The program will look for keywords in sandwich titles which allow it to figure out ingredients and defaults for the sandwiches. If it does not find one of the keywords, it will display an error message to the customer and ask if they want to re-order. The program is fairly robust, so it doesn't crash with unexpected input, but this required the customer to "opt-out" of the order loop by pressing 'q'.

### Example 4b - Customer gives a malformed order.

```
Welcome to Evan's Sandwich Shop!
Would you like to see the menu? (q to quit)


After the sandwich name, let me know if you want to substitute
a different bread or spread, and any extra options you'd like.
Please include exceptions at the end of your order.

What can I get for you today? (q to quit)
the turkey sandwich, but without bacon. Extra avocado and cheese

Let's make sure we got everything right. We have a:
Turkey Bacon with Turkey, Lettuce, Tomato on White with Mayonnaise.
Is that correct? (Type 'no' to reorder)


Great! We'll have that right out for you.
```

Here the customer asked for an exception before asking for extras. This caused the resulting sandwich to be listed without the extras they wanted. However, if the options were typed just like they are on the menu (the only valid way to do it), it would not have been a problem because the exceptions are checked last in the OrderParser.