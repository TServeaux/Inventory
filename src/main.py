"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    Entry point of the application. Starts Flet with the interface defined in
    core/userInterface.py.
    Run it from the project folder:  python src/main.py
    The same file is used by "flet build apk" to package the Android app.
"""

import os

import flet as ft

from core.userInterface import interface

# Flet looks for a relative assets folder from the folder where the command is
# run, not from this file: the full path makes "python src/main.py" work too.
ASSETS_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")

ft.run(interface, assets_dir=ASSETS_FOLDER)
