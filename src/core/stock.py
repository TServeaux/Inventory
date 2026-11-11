"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    Business layer. The Stock class holds the components and the categories,
    checks every rule (unique name, valid quantity, enough stock...) and asks
    Save to write the data after each change.
    The views never modify the data directly: they call the methods of Stock.
    When a rule is broken, a StockError is raised with a message for the user.
"""

from core.icons import COLORS, DEFAULT_COLOR, DEFAULT_ICON, ICONS

class StockError(Exception):
    """
    Description : Raised when an operation on the stock is refused.
        The message explains why and can be shown to the user.
    """


class Stock:
    """
    Description : Components + categories, with the rules and the automatic saving.
    """

    def __init__(self, save):
        """
        Description : Load the saved data, or start with no category
            and an empty stock on the first launch.

        Args :
            save (Save) : object used to read and write the data file.

        Output :
            None
        """

        self.__save = save
        data = save.loadData() or {}

        # Each category is {"name": str, "icon": str, "color": str}. Older files
        # stored only the name (a str): they get the default icon and color.
        self.__categories = [
            c if isinstance(c, dict)
            else {"name": c, "icon": DEFAULT_ICON, "color": DEFAULT_COLOR}
            for c in data.get("categories", [])
        ]

        # Older files had a "picture" field: it is no longer used.
        self.__components = data.get("components", [])
        for component in self.__components:
            component.pop("picture", None)

    # ---------- Reading ----------

    @property
    def categories(self):
        """
        Description : List of the category names (a copy: modifying it changes nothing).

        Args :
            None

        Output :
            list[str] : the category names, in display order.
        """
        return [c["name"] for c in self.__categories]

    def categoryStyle(self, name):
        """
        Description : Icon and color of a category.

        Args :
            name (str) : name of the category.

        Output :
            tuple[str, str] : (icon name, color name), the defaults if the
                category is unknown.
        """

        for category in self.__categories:
            if category["name"] == name:
                return category.get("icon", DEFAULT_ICON), category.get("color", DEFAULT_COLOR)

        return DEFAULT_ICON, DEFAULT_COLOR

    @property
    def components(self):
        """
        Description : List of all the components.

        Args :
            None

        Output :
            list[dict] : the components ({"name", "category", "quantity", "description"}).
        """
        return list(self.__components)

    def findComponent(self, name):
        """
        Description : Look for a component by its name (case and spaces ignored).

        Args :
            name (str) : name of the component.

        Output :
            dict | None : the component, or None if it does not exist.
        """

        key = self.__normalize(name)

        for component in self.__components:
            if self.__normalize(component["name"]) == key:
                return component

        return None

    # ---------- Changes ----------

    def addCategory(self, name, icon=DEFAULT_ICON, color=DEFAULT_COLOR):
        """
        Description : Create a new category (added at the end of the list), then save.

        Args :
            name (str) : name of the new category.
            icon (str) : icon of the category (a key of ICONS).
            color (str) : color of the icon (a key of COLORS).

        Output :
            str : the name actually stored (spaces removed at both ends).

        Raises :
            StockError : empty name, the category already exists, unknown icon or color.
        """

        name = (name or "").strip()

        if not name:
            raise StockError("Please enter a category name")

        if self.__normalize(name) in [self.__normalize(c) for c in self.categories]:
            raise StockError("This category already exists")

        if icon not in ICONS:
            raise StockError("Please choose an icon")

        if color not in COLORS:
            raise StockError("Please choose a color")

        self.__categories.append({"name": name, "icon": icon, "color": color})
        self.__write()
        return name

    def addComponent(self, name, category, quantity, description=""):
        """
        Description : Create a new component, then save.

        Args :
            name (str) : name of the component, must be unique.
            category (str) : one of the existing categories.
            quantity (int | str) : initial quantity (>= 0).
            description (str) : optional description.

        Output :
            None

        Raises :
            StockError : empty or already used name, unknown category, or invalid quantity.
        """

        name = (name or "").strip()

        if not name:
            raise StockError("Please give it a name")

        if self.findComponent(name):
            raise StockError(f'"{name}" already exists')

        if category not in self.categories:
            raise StockError("Please choose a category")

        quantity = self.__checkQuantity(quantity, minimum=0)

        self.__components.append({
            "name": name,
            "category": category,
            "quantity": quantity,
            "description": (description or "").strip(),
        })
        self.__write()

    def addStock(self, name, quantity):
        """
        Description : Add units to an existing component, then save.

        Args :
            name (str) : name of the component.
            quantity (int | str) : number of units to add (>= 1).

        Output :
            int : the new quantity in stock.

        Raises :
            StockError : unknown component or invalid quantity.
        """

        component = self.__getComponent(name)
        quantity = self.__checkQuantity(quantity)

        component["quantity"] += quantity
        self.__write()

        return component["quantity"]

    def removeStock(self, name, quantity):
        """
        Description : Remove units from an existing component, then save.

        Args :
            name (str) : name of the component.
            quantity (int | str) : number of units to remove (>= 1, <= stock).

        Output :
            int : the new quantity in stock.

        Raises :
            StockError : unknown component, invalid quantity, or not enough stock.
        """

        component = self.__getComponent(name)
        quantity = self.__checkQuantity(quantity)

        if quantity > component["quantity"]:
            raise StockError(f"Not enough stock: only {component['quantity']} left")

        component["quantity"] -= quantity
        self.__write()

        return component["quantity"]

    # ---------- Internal helpers ----------

    def __getComponent(self, name):
        """
        Description : Like findComponent, but raise an error if the component does not exist.

        Args :
            name (str) : name of the component.

        Output :
            dict : the component.

        Raises :
            StockError : the component does not exist.
        """

        component = self.findComponent(name)

        if component is None:
            raise StockError(f'"{name}" does not exist')

        return component

    def __checkQuantity(self, quantity, minimum=1):
        """
        Description : Convert a quantity to an integer and check its minimum value.

        Args :
            quantity (int | str) : the quantity typed by the user.
            minimum (int) : smallest accepted value (1 by default).

        Output :
            int : the quantity as an integer.

        Raises :
            StockError : not a whole number, or smaller than the minimum.
        """

        try:
            quantity = int(quantity)
        except (TypeError, ValueError):
            raise StockError("Please enter a whole number")

        if quantity < minimum:
            raise StockError(f"The quantity must be at least {minimum}")

        return quantity

    def __normalize(self, text):
        """
        Description : Prepare a text for comparison (spaces removed at both ends, lowercase).

        Args :
            text (str | None) : the text.

        Output :
            str : the normalized text ("" if text is None).
        """
        return (text or "").strip().lower()

    def __write(self):
        """
        Description : Save the categories and the components through Save.

        Args :
            None

        Output :
            None
        """

        self.__save.saveData({
            "categories": self.__categories,
            "components": self.__components,
        })
