"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    "Add a component" page (route "/newComponent"). Form with name, category,
    quantity and description. A new category can be created from the same page,
    with its icon and its color (shown for every component of the category).
    The checks are done by Stock: this page only shows its error messages.
"""

import flet as ft

from core.icons import COLORS, DEFAULT_COLOR, DEFAULT_ICON, ICONS, iconImage
from core.stock import StockError


class NewComponent(ft.View):
    """
    Description : View with the form to create a component.
    """

    def __init__(self, stock):
        """
        Description : Create the form controls.

        Args :
            stock (Stock) : the stock where the component will be added.

        Output :
            None
        """

        self.__stock = stock

        # Icon and color selected for the next category to create.
        self.__icon = DEFAULT_ICON
        self.__color = DEFAULT_COLOR

        self.__name = ft.TextField(label="Component name")
        self.__category = ft.Dropdown(
            label="Category",
            options=[self.__categoryOption(c) for c in self.__stock.categories],
        )
        self.__newCategory = ft.TextField(label="New category", expand=True)
        self.__iconChoices = ft.Row(wrap=True, spacing=4, run_spacing=4)
        self.__colorChoices = ft.Row(wrap=True, spacing=8, run_spacing=8)
        self.__quantity = ft.TextField(
            label="Quantity",
            value="0",
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.__description = ft.TextField(
            label="Description",
            multiline=True,
            min_lines=1,
            max_lines=3,
        )
        self.__message = ft.Text(color=ft.Colors.RED)

        self.__fillChoices()

        super().__init__(
            route="/newComponent",
            controls=[
                ft.AppBar(title=ft.Text("Add a component")),
                self.__name,
                self.__category,
                ft.ExpansionTile(
                    title=ft.Text("Create a category"),
                    expanded_cross_axis_alignment=ft.CrossAxisAlignment.START,
                    controls=[
                        ft.Row([
                            self.__newCategory,
                            ft.IconButton(icon=ft.Icons.ADD, on_click=self.addCategory),
                        ]),
                        ft.Text("Icon"),
                        self.__iconChoices,
                        ft.Text("Color"),
                        self.__colorChoices,
                    ],
                ),
                self.__quantity,
                self.__description,
                self.__message,
                ft.Button("Save", icon=ft.Icons.SAVE, on_click=self.save),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def __categoryOption(self, name):
        """
        Description : Build the dropdown option of a category, with its icon.

        Args :
            name (str) : name of the category.

        Output :
            ft.DropdownOption : the option.
        """

        icon, color = self.__stock.categoryStyle(name)
        return ft.DropdownOption(key=name, text=name, leading_icon=iconImage(icon, color, 24))

    def __fillChoices(self):
        """
        Description : (Re)build the icon and color pickers. The selected icon and
            color are surrounded by a border, and the icons are drawn in the
            selected color to preview the result.

        Args :
            None

        Output :
            None
        """

        selected = ft.Border.all(2, ft.Colors.PRIMARY)
        unselected = ft.Border.all(2, ft.Colors.TRANSPARENT)

        self.__iconChoices.controls = [
            ft.Container(
                content=iconImage(name, self.__color, 28),
                padding=6,
                border_radius=8,
                border=selected if name == self.__icon else unselected,
                tooltip=label,
                on_click=self.selectIcon(name),
            )
            for name, label in ICONS.items()
        ]

        self.__colorChoices.controls = [
            ft.Container(
                width=32,
                height=32,
                border_radius=16,
                bgcolor=value,
                border=ft.Border.all(3, ft.Colors.PRIMARY) if name == self.__color else None,
                tooltip=name,
                on_click=self.selectColor(name),
            )
            for name, value in COLORS.items()
        ]

    def selectIcon(self, name):
        """
        Description : Factory: give the click handler that selects an icon.
            (A factory is needed so that each button remembers its own icon.)

        Args :
            name (str) : the icon selected by this button.

        Output :
            function : the click handler.
        """

        def handler(e):
            self.__icon = name
            self.__fillChoices()
            self.update()

        return handler

    def selectColor(self, name):
        """
        Description : Factory: give the click handler that selects a color.

        Args :
            name (str) : the color selected by this button.

        Output :
            function : the click handler.
        """

        def handler(e):
            self.__color = name
            self.__fillChoices()
            self.update()

        return handler

    def addCategory(self, e):
        """
        Description : Create the category typed in "New category" with the selected
            icon and color, and select it. Otherwise show the error message.

        Args :
            e (ft.Event) : click event of the "+" button.

        Output :
            None
        """

        try:
            name = self.__stock.addCategory(self.__newCategory.value, self.__icon, self.__color)
        except StockError as error:
            self.__message.value = str(error)
        else:
            self.__category.options.append(self.__categoryOption(name))
            self.__category.value = name
            self.__newCategory.value = ""
            self.__message.value = ""

        self.update()

    async def save(self, e):
        """
        Description : Ask Stock to create the component, then go back to Home.
            If a rule is broken, show the message and stay on the page.

        Args :
            e (ft.Event) : click event of the "Save" button.

        Output :
            None
        """

        try:
            self.__stock.addComponent(
                name=self.__name.value,
                category=self.__category.value,
                quantity=self.__quantity.value,
                description=self.__description.value,
            )
        except StockError as error:
            self.__message.value = str(error)
            self.update()
            return

        await self.page.push_route("/")
