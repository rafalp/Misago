Category styles
===============

Misago categories allow you to specify their css class when editing them in admin control panel.

This class is then used to build proper css class names used around the UI. For example, entering "protoss" in class's css name will result in category on categories lists and threads in this class on threads list having `list-group-category-has-flavor` and `list-group-item-category-protoss` css classes on them, allowing you to differentiate this category and its threads on lists. In addition to this, such category's page and its thread page would have `page-protoss` class so you could customize it further.


## CSS shared for all custom classed

Items on list that have custom class added to them also have `list-group-category-has-flavor` css class that allows you to include customisations common for all classes in one place for both simplicity and css size reduction.


## Default classes

Misago's default theme defines basic classes named after colors in `Material Design Palette <https://material.io/guidelines/style/color.html#color-color-palette>`_, visualised as bands added to left side of category and its threads on lists:

- `red`
- `light-red`
- `pink`
- `light-pink`
- `purple`
- `light-purple`
- `deep-purple`
- `indigo`
- `light-indigo`
- `blue`
- `light-blue`
- `cyan`
- `light-cyan`
- `teal`
- `light-teal`
- `green`
- `light-green`
- `lime`
- `yellow`
- `amber`
- `orange`
- `deep-orange`
- `brown`
- `light-brown`
- `blue-grey`
- `light-blue-grey`
- `grey`
- `black`