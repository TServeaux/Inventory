"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    Icons and colors that can be given to a category. The icons come from
    Tabler Icons (MIT license, https://tabler.io/icons): they are SVG files
    stored in src/assets/icons/. An icon is identified by its file name
    without ".svg" (e.g. "circuit-resistor"), which is what is saved in the JSON.
"""

import flet as ft

# Icon used when a category has no (or an unknown) icon.
DEFAULT_ICON = "box"

# Icons offered in the form, in display order: file name -> label (tooltip).
ICONS = {
    "box": "Other",
    "circuit-resistor": "Resistor",
    "circuit-capacitor": "Capacitor",
    "circuit-capacitor-polarized": "Polarized capacitor",
    "circuit-inductor": "Inductor",
    "circuit-diode": "Diode",
    "circuit-diode-zener": "Zener diode",
    "circuit-bulb": "Lamp",
    "bulb": "LED / light",
    "circuit-battery": "Battery (symbol)",
    "circuit-cell": "Cell",
    "battery-2": "Battery",
    "circuit-motor": "Motor (symbol)",
    "engine": "Motor",
    "propeller": "Fan",
    "circuit-switch-open": "Switch",
    "circuit-pushbutton": "Push button",
    "circuit-ground": "Ground",
    "cpu": "Integrated circuit",
    "cpu-2": "Microcontroller",
    "device-desktop": "Display",
    "bolt": "Power",
    "plug": "Connector",
    "usb": "USB",
    "antenna": "Antenna / RF",
    "wifi": "Wi-Fi",
    "bluetooth": "Bluetooth",
    "wave-sine": "Signal / oscillator",
    "temperature": "Temperature sensor",
    "volume": "Speaker / buzzer",
    "microphone": "Microphone",
    "magnet": "Magnet / relay",
    "tool": "Tool",
    "settings": "Mechanical",
}


# Color used when a category has no (or an unknown) color: the text color of the
# theme, so the icon stays visible in light and dark mode.
DEFAULT_COLOR = "default"

# Colors offered in the form, in display order: name saved in the JSON -> Flet color.
COLORS = {
    "default": ft.Colors.ON_SURFACE,
    "red": ft.Colors.RED,
    "orange": ft.Colors.ORANGE,
    "amber": ft.Colors.AMBER,
    "green": ft.Colors.GREEN,
    "teal": ft.Colors.TEAL,
    "blue": ft.Colors.BLUE,
    "indigo": ft.Colors.INDIGO,
    "purple": ft.Colors.PURPLE,
    "pink": ft.Colors.PINK,
    "brown": ft.Colors.BROWN,
    "grey": ft.Colors.BLUE_GREY,
}


def iconImage(name, color, size):
    """
    Description : Build the image of an icon in the given color. The SVG files are
        drawn in black: "color" repaints every visible line of the icon.

    Args :
        name (str | None) : icon name (a key of ICONS). Unknown -> DEFAULT_ICON.
        color (str | None) : color name (a key of COLORS). Unknown -> DEFAULT_COLOR.
        size (int) : width and height in pixels.

    Output :
        ft.Image : the icon.
    """

    if name not in ICONS:
        name = DEFAULT_ICON

    return ft.Image(
        src=f"icons/{name}.svg",
        width=size,
        height=size,
        color=COLORS.get(color, COLORS[DEFAULT_COLOR]),
    )
