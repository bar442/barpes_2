from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import  QWidget
from PyQt5.QtWidgets import QMenuBar ,QMenu
import sys
import threading
from .menu_bar_template import QMenuBarTemplate

app = QtWidgets.QApplication(sys.argv)

_widget_root_keeper=[]
def show_widget(widget:QWidget,title:str=None)->QtWidgets.QApplication:
    _instance = QtWidgets.QApplication.instance()
    if not _instance:
        _instance = QtWidgets.QApplication([])
    
    app = _instance
    main_window = QtWidgets.QMainWindow()
    _widget_root_keeper.append(main_window)
    # === Wrap in a scroll area ===
    scroll = QtWidgets.QScrollArea()
    scroll.setWidgetResizable(True)   # important!
    main_window.setCentralWidget(scroll)
    # === add the widget ===
    scroll.setWidget(widget)
    main_window.show()


    if title:
        main_window.setWindowTitle(title)

    #--------------------------------  adding menubar mechanism
    if hasattr(widget,"menuBarTemplate") and isinstance(widget.menuBarTemplate , QMenuBarTemplate):
        menuBar =  widget.menuBarTemplate.generate_menu_bar(parent=main_window)
        main_window.setMenuBar(menuBar)

    #--------------------------------
    app.exec_()
    return app



def show_aa(widget:QWidget,title:str=None):
    MainWindow = QtWidgets.QMainWindow()
    MainWindow.setCentralWidget(widget)
    MainWindow.show()
    if title:
        MainWindow.setWindowTitle(title)
    app.exec_()