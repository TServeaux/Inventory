"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    Builds the application: creates the Stock (with its Save) and handles the
    routing, i.e. which view is displayed for each route:
        /                   -> Home
        /newComponent       -> NewComponent (on top of Home)
        /component/<name>   -> ComponentDetail (on top of Home)
"""

import os
from urllib.parse import unquote

import flet as ft

from src.core.stock import Stock
from src.core.views.componentDetail import ComponentDetail
from src.core.views.home import Home
from src.core.views.newComponent import NewComponent
from src.utils.save import Save

# Project root = two folders above this file (src/core/ -> project).
PROJECT_FOLDER = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_FOLDER = os.path.join(PROJECT_FOLDER, "data")


def interface(page: ft.Page):
    """
    Description : Main function given to ft.run: sets up the page, the stock and the routing.

    Args :
        page (ft.Page) : the Flet page (window) of the application.

    Output :
        None
    """

    page.title = "Inventory"

    stock = Stock(Save("inventory.json", DATA_FOLDER))

    def routeChange(e=None):
        """
        Description : Rebuild the views for the current route. The views are rebuilt
            from the stock every time, so they always show up-to-date quantities.

        Args :
            e (ft.RouteChangeEvent | None) : the event (None for the first call).

        Output :
            None
        """

        page.views.clear()
        page.views.append(Home(stock))

        if page.route == "/newComponent":
            page.views.append(NewComponent(stock))

        elif page.route.startswith("/component/"):
            name = unquote(page.route.removeprefix("/component/"))
            component = stock.findComponent(name)

            if component:
                page.views.append(ComponentDetail(stock, component))

        page.update()

    async def viewPop(e):
        """
        Description : Called by the "back" arrow: removes the top view and goes
            back to the route of the view below.

        Args :
            e (ft.ViewPopEvent) : the event, e.view is the view being closed.

        Output :
            None
        """

        page.views.remove(e.view)
        await page.push_route(page.views[-1].route)

    page.on_route_change = routeChange
    page.on_view_pop = viewPop
    routeChange()
