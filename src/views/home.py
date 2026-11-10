"""
Author : Tao Serveaux
Date : 10/11/2026
"""

import flet as ft

class Home(ft.View):
    
    def __init__(self):
        
        self.__choosenCategorie = "All"
        self.__lineFilters = ft.Row(wrap=True)
        
        super.__init__(
            route="/",
            controls=[
                ft.AppBar(title=ft.Text("Home")),
                self.__research,
                self.__categoriesLines,
                self.__list,
            ],
        )
        
        self.buildFilters()
        self.buildObjects()
    
    def onSearch(self, e):
        
        self.buildObjects()
        self.update()
    
    def  chooseCategorie(self, name):
        
        def handler(e):
            self.__choosenCategorie = name
            self.buildCategories()
            self.buildObjects()
            self.update()
        
        return handler

    def buildCategories(self, CATEGORIES):
        
        self.__categoriesLines.controls.clear()
        for name in CATEGORIES:
            
            bouton = ft.FilledButton if name == self.__choosenCategorie else ft.OutlinedButton
            self.__categoriesLines.controls.append(
                bouton(name, on_click=self.chooseCategorie(name))
            )
    
    def buildObjects(self, OBJECTS):
        
        text = (self.__research.value or "").lower()
        self.__list.controls.clear()
        
        for object in OBJECTS:
            goodCategory = self.__choosenCategorie == "All" or object["category"] == self.__choosenCategorie
            
            if goodCategory and text in object["name"].lower():
                self.__list.controls.append(
                    ft.ListTile(title=ft.Text(object['name']), subtitle=ft.Text['category'])
                )
            
            if not self.__list.controls:
                self.__list.controls.append(ft.Text("No result found"))