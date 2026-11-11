"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    Home page (route "/"). Shows the components grouped by category (with a
    separator for each category), sorted by name, with filter buttons on top.
    Clicking a component opens its detail page; the "+" button opens the form
    to add a new component.
"""

from urllib.parse import quote

import flet as ft

from core.icons import iconImage


class Home(ft.View):
    """
    Description : View listing the stock.
    """

    def __init__(self, stock):
        """
        Description : Create the controls and fill the filter line and the list.

        Args :
            stock (Stock) : the stock to display.

        Output :
            None
        """

        self.__stock = stock
        self.__filter = "All"
        self.__filterLine = ft.Row(wrap=True)
        self.__list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)

        super().__init__(
            route="/",
            controls=[
                ft.AppBar(title=ft.Text("Stock")),
                self.__filterLine,
                self.__list,
            ],
            floating_action_button=ft.FloatingActionButton(
                icon=ft.Icons.ADD, on_click=self.goToNewComponent
            ),
        )

        self.buildFilter()
        self.buildList()

    async def goToNewComponent(self, e):
        """
        Description : Open the "add a component" page.

        Args :
            e (ft.Event) : click event of the "+" button.

        Output :
            None
        """
        await self.page.push_route("/newComponent")

    def openComponent(self, name):
        """
        Description : Create the click handler that opens the detail page of a component.
            The name can contain spaces or "/": quote() makes it safe inside a route.

        Args :
            name (str) : name of the component to open.

        Output :
            async function : handler to give to on_click.
        """

        async def handler(e):
            """Open the detail page of the component (e : click event)."""
            await self.page.push_route(f"/component/{quote(name, safe='')}")

        return handler

    def chooseFilter(self, name):
        """
        Description : Create the click handler of a filter button.

        Args :
            name (str) : category to filter on ("All" = no filter).

        Output :
            function : handler to give to on_click.
        """

        def handler(e):
            """Apply the filter and refresh the page (e : click event)."""
            self.__filter = name
            self.buildFilter()
            self.buildList()
            self.update()

        return handler

    def buildFilter(self):
        """
        Description : (Re)build the filter buttons; the selected one is filled.

        Args :
            None

        Output :
            None
        """

        self.__filterLine.controls.clear()

        for name in ["All"] + self.__stock.categories:
            button = ft.FilledButton if name == self.__filter else ft.OutlinedButton
            self.__filterLine.controls.append(button(name, on_click=self.chooseFilter(name)))

    def separator(self, category, quantity):
        """
        Description : Build the title + line shown above each category.

        Args :
            category (str) : name of the category.
            quantity (int) : number of components in this category.

        Output :
            ft.Column : the separator control.
        """

        icon, color = self.__stock.categoryStyle(category)

        return ft.Column(
            controls=[
                ft.Row([
                    iconImage(icon, color, 24),
                    ft.Text(f"{category} ({quantity})", size=18, weight=ft.FontWeight.BOLD),
                ]),
                ft.Divider(thickness=2),
            ],
            spacing=2,
        )

    def componentLine(self, component):
        """
        Description : Build the line of one component (category icon, name,
            quantity, description).

        Args :
            component (dict) : the component to display.

        Output :
            ft.ListTile : the clickable line.
        """

        icon, color = self.__stock.categoryStyle(component["category"])

        return ft.ListTile(
            leading=iconImage(icon, color, 40),
            title=ft.Text(f"{component['name']} (x{component['quantity']})"),
            subtitle=ft.Text(component["description"]),
            trailing=ft.Icon(ft.Icons.CHEVRON_RIGHT),
            on_click=self.openComponent(component["name"]),
        )

    def buildList(self):
        """
        Description : (Re)build the list: for each category kept by the filter,
            a separator then its components sorted by name. Shows "No component"
            if nothing is displayed.

        Args :
            None

        Output :
            None
        """

        self.__list.controls.clear()

        for category in self.__stock.categories:
            if self.__filter != "All" and category != self.__filter:
                continue

            components = sorted(
                [c for c in self.__stock.components if c["category"] == category],
                key=lambda c: c["name"].lower(),
            )

            if not components:
                continue

            self.__list.controls.append(self.separator(category, len(components)))

            for component in components:
                self.__list.controls.append(self.componentLine(component))

        # Checked once, after the loop: was anything displayed at all?
        if not self.__list.controls:
            self.__list.controls.append(ft.Text("No component"))
