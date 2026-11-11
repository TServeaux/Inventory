"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    "Add a component" page (route "/newComponent"). Form with name, category
    (with the possibility to create a new one), picture, quantity and description.
    The checks are done by Stock: this page only shows its error messages.
"""

import flet as ft

from src.core.stock import StockError


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
        self.__pathToPicture = None

        self.__name = ft.TextField(label="Component name")
        self.__category = ft.Dropdown(
            label="Category",
            options=[ft.DropdownOption(c) for c in self.__stock.categories],
        )
        self.__newCategory = ft.TextField(label="New category", expand=True)
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
        self.__preview = ft.Image(src="", width=150, height=150, visible=False)
        self.__message = ft.Text(color=ft.Colors.RED)

        super().__init__(
            route="/newComponent",
            controls=[
                ft.AppBar(title=ft.Text("Add a component")),
                self.__name,
                self.__category,
                ft.Row([
                    self.__newCategory,
                    ft.IconButton(icon=ft.Icons.ADD, on_click=self.addCategory),
                ]),
                ft.Button("Choose a picture", icon=ft.Icons.PHOTO, on_click=self.choosePicture),
                self.__preview,
                self.__quantity,
                self.__description,
                self.__message,
                ft.Button("Save", icon=ft.Icons.SAVE, on_click=self.save),
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def addCategory(self, e):
        """
        Description : Create the category typed in "New category" and select it,
            or show the error message.

        Args :
            e (ft.Event) : click event of the "+" button.

        Output :
            None
        """

        try:
            name = self.__stock.addCategory(self.__newCategory.value)
        except StockError as error:
            self.__message.value = str(error)
        else:
            self.__category.options.append(ft.DropdownOption(name))
            self.__category.value = name
            self.__newCategory.value = ""
            self.__message.value = ""

        self.update()

    async def choosePicture(self, e):
        """
        Description : Open the file picker and show a preview of the chosen picture.

        Args :
            e (ft.Event) : click event of the "Choose a picture" button.

        Output :
            None
        """

        files = await ft.FilePicker().pick_files(
            allow_multiple=False,
            file_type=ft.FilePickerFileType.IMAGE,
        )

        if files:
            self.__pathToPicture = files[0].path
            self.__preview.src = self.__pathToPicture
            self.__preview.visible = True
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
                picture=self.__pathToPicture,
                quantity=self.__quantity.value,
                description=self.__description.value,
            )
        except StockError as error:
            self.__message.value = str(error)
            self.update()
            return

        await self.page.push_route("/")
