"""
Date : 10/11/2026
Author : Tao Serveaux
"""

import flet as ft
from views.generate import Ge
from views.home import Home

class UserInterface:
    
    def main(page: ft.Page):
        
        def routeChange(e=None):
            page.views.clear()
            page.views.append(Home)
            if page.route == "/generate":
                page.views.append()
            page.update()
        
        
        
        