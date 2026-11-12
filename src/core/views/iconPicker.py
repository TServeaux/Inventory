"""
Date : 12/11/2026
Author : Tao Serveaux

Description :
    Reusable icon + color picker, used by the "add a component" form and by the
    detail page of a component. It only remembers the selected icon and color
    and warns its owner (callback onChange) when they change: it never touches
    the stock itself.
"""

import flet as ft

from core.icons import COLORS, DEFAULT_COLOR, DEFAULT_ICON, ICONS, iconImage


class IconPicker(ft.Column):
    """
    Description : Grid of icons (drawn in the selected color) + row of color dots.
        The selected icon and color are surrounded by a border.
    """

    def __init__(self, icon=DEFAULT_ICON, color=DEFAULT_COLOR, onChange=None):
        """
        Description : Create the two pickers with a starting selection.

        Args :
            icon (str) : icon selected at the start (a key of ICONS).
            color (str) : color selected at the start (a key of COLORS).
            onChange (function | None) : called as onChange(icon, color) after
                each click on an icon or a color.

        Output :
            None
        """

        self.icon = icon if icon in ICONS else DEFAULT_ICON
        self.color = color if color in COLORS else DEFAULT_COLOR
        self.__onChange = onChange

        self.__iconChoices = ft.Row(wrap=True, spacing=4, run_spacing=4)
        self.__colorChoices = ft.Row(wrap=True, spacing=8, run_spacing=8)

        super().__init__(
            controls=[
                ft.Text("Icon"),
                self.__iconChoices,
                ft.Text("Color"),
                self.__colorChoices,
            ],
        )

        self.__fill()

    def __fill(self):
        """
        Description : (Re)build the icon and color buttons from the current selection.

        Args :
            None

        Output :
            None
        """

        selected = ft.Border.all(2, ft.Colors.PRIMARY)
        unselected = ft.Border.all(2, ft.Colors.TRANSPARENT)

        self.__iconChoices.controls = [
            ft.Container(
                content=iconImage(name, self.color, 28),
                padding=6,
                border_radius=8,
                border=selected if name == self.icon else unselected,
                tooltip=label,
                on_click=self.__select(icon=name),
            )
            for name, label in ICONS.items()
        ]

        self.__colorChoices.controls = [
            ft.Container(
                width=32,
                height=32,
                border_radius=16,
                bgcolor=value,
                border=ft.Border.all(3, ft.Colors.PRIMARY) if name == self.color else None,
                tooltip=name,
                on_click=self.__select(color=name),
            )
            for name, value in COLORS.items()
        ]

    def __select(self, icon=None, color=None):
        """
        Description : Factory: give the click handler that selects an icon or a color.
            (A factory is needed so that each button remembers its own value.)

        Args :
            icon (str | None) : icon selected by this button (None = unchanged).
            color (str | None) : color selected by this button (None = unchanged).

        Output :
            function : the click handler.
        """

        def handler(e):
            if icon is not None:
                self.icon = icon
            if color is not None:
                self.color = color

            self.__fill()
            self.update()

            if self.__onChange:
                self.__onChange(self.icon, self.color)

        return handler
