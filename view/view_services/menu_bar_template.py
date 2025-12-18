from PyQt5.QtWidgets import QMenuBar ,QMenu ,QAction
from PyQt5.QtWidgets import  QWidget

from typing import *

class QMenuBarTemplate():
    def __init__(self,parent:QWidget):
        self.parent:QWidget=parent
        self.menus:List[QMenu] = []
        self.actions:List[QAction]=[]

    def addMenu(self,menu_name:str ,parent:QWidget =None)->QMenu:
        prnt= self.parent if parent is None else parent
        new_menu=QMenu(title = menu_name, parent=prnt)
        self.menus.append(new_menu)
        return new_menu
    
    def addAction(self,title:str , func:Callable ,parent:QWidget =None):
        prnt= self.parent if parent is None else parent
        new_action = QAction(text=title,parent=prnt)
        new_action.triggered.connect(func)
        self.actions.append(new_action)
        return new_action
    
    def generate_menu_bar(self ,parent:QWidget=None)->QMenuBar:
        prnt= self.parent if parent is None else parent
        menuBar =  QMenuBar(prnt)
        for mn in self.menus: 
            menuBar.addMenu(mn)
        for ac in self.actions : 
            menuBar.addAction(ac)

        return menuBar
    
    @staticmethod
    def add_template_to_a_menu(target_menu:QMenu,menubar_template:'QMenuBarTemplate'):
        for mn in menubar_template.menus: 
            target_menu.addMenu(mn)

        for ac in menubar_template.actions : 
            target_menu.addAction(ac)

    def append(self,menubar_template:'QMenuBarTemplate'):
        for mn in menubar_template.menus: 
            self.menus.append(mn)

        for ac in menubar_template.actions : 
            self.actions.append(ac)
















