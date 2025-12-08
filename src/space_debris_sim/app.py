"""
Application entrypoint: wires GUI components and simulation core.
"""

from tkinter import Tk
from .gui.login import LoginWindow

def main():
    root = Tk()
    LoginWindow(root)
    root.mainloop()
