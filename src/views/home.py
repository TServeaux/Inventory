"""
Author : Tao Serveaux
Date : 10/11/2026
"""

import flet as ft

class Home(ft.View):
    
    def __init__(self):
        
        self.__filter = "All"
        self.__lineFilters = ft.Row(wrap=True)
        self.__list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=True)
        
        super.__init__(
            route="/",
            controls=[
                ft.AppBar(title=ft.Text("Home")),
                self.__lineFilters,
                self.__list,
            ],
        )
        
        self.buildFilters()
        self.buildList()
    
    def  chooseCategorie(self, name):
        
        def handler(e):
            self.__filter = name
            self.buildFilters()
            self.buildList()
            self.update()
        
        return handler

    def buildFilters(self, CATEGORIES):
        
        self.__lineFilters.controls.clear()
        
        for name in ["Tout"] + CATEGORIES:
            
            bouton = ft.FilledButton if name == self.__filter else ft.OutlinedButton
            self.__lineFilters.controls.append(
                bouton(name, on_click=self.chooseCategorie(name))
            )
    
    def separator(self, category):
        
        return ft.Column(
            controls=[
                ft.Text(f"{category}", size=18, weight=ft.FontWeight.BOLD),
                ft.Divider(thickness=2),
            ],
            spacing=2,
        )
    
    def objLine(self, obj):
        
        if obj["photo"]:
            image = ft.Image(src=obj["photo"], width=60, height=60)
        
        else:
            image = ft.Icon(ft.Icons.IMAGE_NOT_SUPPORTED, size=40)
        
        return ft.ListTile(
            leading=image,
            title=ft.Text(f"{obj['name']} (x{obj['quantity']})"),
            subtitle=ft.Text(obj["description"])
        )
    
    def buildList(self, CATEGORIES, STOCK):
        
        self.__list.controls.clear()
        
        for category in CATEGORIES:
            
            if self.__filter != "All" and category != self.__filter:
                continue
            
            objs = sorted(
                [a for a in STOCK if a["category"] == category],
                key=lambda a: a["name"].lower(),
            )
            
            if not objs:
                continue
            
            self.__list.controls.append(self.separator(category))
            
            for obj in objs:
                self.__list.controls.append(self.objLine(obj))
        
        if not self.__list.controls:
            self.__list.controls.append(ft.Text("No object"))