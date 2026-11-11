"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    Detail page of a component (route "/component/<name>"). Shows its category icon,
    category, description and quantity, with a quantity field and two buttons
    to add or remove stock. The checks are done by Stock: this page only shows
    the result (green) or the error message (red).
"""

from urllib.parse import quote

import flet as ft

from core.icons import iconImage
from core.stock import StockError


class ComponentDetail(ft.View):
    """
    Description : View showing one component and managing its stock.
    """

    def __init__(self, stock, component):
        """
        Description : Create the controls of the page.

        Args :
            stock (Stock) : the stock containing the component.
            component (dict) : the component to display.

        Output :
            None
        """

        self.__stock = stock
        self.__name = component["name"]

        icon, color = stock.categoryStyle(component["category"])
        image = iconImage(icon, color, 120)

        self.__quantityText = ft.Text(
            self.__quantityLabel(component["quantity"]),
            size=24,
            weight=ft.FontWeight.BOLD,
        )
        self.__amount = ft.TextField(
            label="Quantity",
            value="1",
            width=150,
            keyboard_type=ft.KeyboardType.NUMBER,
            input_filter=ft.NumbersOnlyInputFilter(),
        )
        self.__message = ft.Text()

        super().__init__(
            route=f"/component/{quote(self.__name, safe='')}",
            controls=[
                ft.AppBar(title=ft.Text(self.__name)),
                image,
                ft.Text(f"Category: {component['category']}"),
                ft.Text(component["description"] or "No description", italic=True),
                self.__quantityText,
                ft.Row([
                    self.__amount,
                    ft.Button("Add", icon=ft.Icons.ADD, on_click=self.add),
                    ft.OutlinedButton("Remove", icon=ft.Icons.REMOVE, on_click=self.remove),
                ]),
                self.__message,
            ],
            scroll=ft.ScrollMode.AUTO,
        )

    def add(self, e):
        """
        Description : Add the typed quantity to the stock.

        Args :
            e (ft.Event) : click event of the "Add" button.

        Output :
            None
        """
        self.__change(self.__stock.addStock, "Added")

    def remove(self, e):
        """
        Description : Remove the typed quantity from the stock.

        Args :
            e (ft.Event) : click event of the "Remove" button.

        Output :
            None
        """
        self.__change(self.__stock.removeStock, "Removed")

    def __change(self, operation, verb):
        """
        Description : Shared code for Add and Remove (only the Stock method differs):
            call the operation, then show the new quantity or the error message.

        Args :
            operation (function) : stock.addStock or stock.removeStock.
            verb (str) : word shown in the success message ("Added" / "Removed").

        Output :
            None
        """

        try:
            newQuantity = operation(self.__name, self.__amount.value)
        except StockError as error:
            self.__message.value = str(error)
            self.__message.color = ft.Colors.RED
        else:
            self.__quantityText.value = self.__quantityLabel(newQuantity)
            self.__message.value = f"{verb} {self.__amount.value}"
            self.__message.color = ft.Colors.GREEN

        self.update()

    def __quantityLabel(self, quantity):
        """
        Description : Text shown for the quantity in stock.

        Args :
            quantity (int) : quantity in stock.

        Output :
            str : e.g. "In stock: 12".
        """
        return f"In stock: {quantity}"
