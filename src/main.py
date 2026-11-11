"""
Date : 11/11/2026
Author : Tao Serveaux

Description :
    Entry point of the application. Starts Flet with the interface defined in
    src/core/userInterface.py.
    Run it from the project folder:  python main.py
"""

import flet as ft

from src.core.userInterface import interface

ft.run(interface)
