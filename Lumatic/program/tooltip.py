"""
Classe provide from crxguy52 (https://stackoverflow.com/users/6106104/crxguy52)
Source: https://askcodez.com/comment-puis-je-afficher-les-info-bulles-dans-tkinter.html (#29)
- Tested with Python27 and Python34  by  vegaseat  09sep2014:
https://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter
- Modified to include a delay time by Victor Zaccardo, 25mar16
"""
import tkinter as tk


class CreateToolTip(object):
    """Gives a Tkinter widget a tooltip as the mouse is above the widget."""
    def __init__(self, widget, text='widget info'):
        self.waittime = 500     #miliseconds
        self.wraplength = 180   #pixels
        self.widget = widget
        self.text = text
        self.widget.bind("<Enter>", self.enter)
        self.widget.bind("<Leave>", self.leave)
        self.widget.bind("<ButtonPress>", self.leave)
        self.id = None
        self.tw = None
    def enter(self, event=None):
        self.schedule()
    def leave(self, event=None):
        self.unschedule()
        self.hidetip()
    def schedule(self):
        self.unschedule()
        self.id = self.widget.after(self.waittime, self.showtip)
    def unschedule(self):
        id = self.id
        self.id = None
        if id:
            self.widget.after_cancel(id)
    def showtip(self, event=None):
        x = self.widget.winfo_rootx() + self.widget.winfo_width()
        y = self.widget.winfo_rooty() + self.widget.winfo_height()/2
        # creates a toplevel window
        self.tw = tk.Toplevel(self.widget)
        # Leaves only the label and removes the app window
        self.tw.wm_overrideredirect(True)
        self.tw.wm_geometry("+%d+%d" % (x, y))
        label = tk.Label(self.tw, text=self.text, justify='left',
        background="white", relief='solid', borderwidth=1,
        wraplength = self.wraplength)
        label.pack(ipadx=1)
    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()