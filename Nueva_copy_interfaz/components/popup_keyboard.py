from tkinter import *
from customtkinter import *
import sys

class MathKeyboard(CTkToplevel):
    
    def __init__(self, attach, x=None, y=None, key_color=None,
                 text_color=None, hover_color=None, fg_color=None,
                 keywidth: int = 5, keyheight: int = 2, command=None,
                 alpha: float = 0.85, corner=20, **kwargs):
        
        super().__init__(takefocus=0)
        
        self.focus()
        self.corner = corner
        self.disable = True
        
        if sys.platform.startswith("win"):
            self.overrideredirect(True)
            self.transparent_color = '#333333'
            self.attributes("-transparentcolor", self.transparent_color)
        elif sys.platform.startswith("darwin"):
            self.overrideredirect(True)
            self.transparent_color = 'systemTransparent'
            self.attributes("-transparent", True)
        else:
            self.attributes("-type", "splash")
            self.transparent_color = '#000001'
            self.corner = 0
            self.withdraw()
            
        self.disable = False
        self.fg_color = "#2a2d2e" if fg_color is None else fg_color
        self.frame = CTkFrame(self, bg_color=self.transparent_color, fg_color=self.fg_color, corner_radius=self.corner, border_width=2)
        self.frame.pack(expand=True, fill="both")
        
        self.attach = attach
        self.keywidth = keywidth
        self.keyheight = keyheight
        self.keycolor = key_color if key_color else "#444444"
        self.textcolor = text_color if text_color else "#FFFFFF"
        self.hovercolor = hover_color if hover_color else "#555555"
        self.command = command
        self.resizable(width=False, height=False)
        self.transient(self.master)

        self.keys = [
            ['7', '8', '9', '/', 'π', 'e'],
            ['4', '5', '6', '*', 'sin', 'cos'],
            ['1', '2', '3', '-', 'tan', 'sqrt'],
            ['0', '.', '^', '+', '(', ')'],
            ['x', 'y', 'z', '=', 'Clear', 'Enter']
        ]

        self._init_keys()
        self.attributes('-alpha', alpha)
        
    def _init_keys(self):
        """Crea las teclas del teclado matemático."""
        for row_idx, row in enumerate(self.keys):
            frame = CTkFrame(self.frame)
            frame.pack(side=TOP, pady=5)
            for key in row:
                btn = CTkButton(frame, text=key, width=self.keywidth * 10 if key == 'Enter' else self.keywidth,
                                height=self.keyheight, fg_color=self.keycolor, text_color=self.textcolor,
                                hover_color=self.hovercolor, command=lambda k=key: self._on_key_press(k))
                btn.pack(side=LEFT, padx=2)

    def _on_key_press(self, key):
        """Define el comportamiento de cada tecla."""
        if key == 'Clear':
            self.attach.delete(0, END)
        elif key == 'Enter':
            self.attach.insert(END, ' = ')
        elif key in {'π', 'e', 'sin', 'cos', 'tan', 'sqrt'}:
            self.attach.insert(END, f"{key}(" if key not in {'π', 'e'} else key)
        elif key == '^':
            self.attach.insert(END, '**')
        else:
            self.attach.insert(END, key)

    def destroy_popup(self):
        """Destruye el teclado."""
        self.destroy()
        self.disable = True
