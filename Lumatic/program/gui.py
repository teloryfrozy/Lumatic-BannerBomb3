###############################################
#               GUI of Lumatic                #
#   Runs for Manjaro KDE PLasma, Windows 10   #
###############################################
from threading import Thread
from tkinter import Button, Entry, Frame, Label, Menu, PhotoImage, Tk, messagebox
from tkinter.ttk import Progressbar
from tooltip import CreateToolTip
from engine import Language, hack, resetPsw


class GUI:
    """Management of the GUI for Lumatic"""

    def __init__(self, os_name: str):
        """Template of Lumatic

        Argument:
            - {str} os_name: common name of the OS
        """
        # Generate a new object Tk
        self.root = Tk()
        self.os_name = os_name

        # === Default parameters === #
        # --- Load config file --- #
        self.lang = Language()
        # --- Prepare window --- #
        self.root.title("Lumatic")
        # Icon extension depends on the OS
        if os_name == "Linux":
            self.root.iconbitmap("@photos/luma.xbm")
        if os_name == "Windows":
            self.root.iconbitmap("photos/luma.ico")

        # --- Window preparation --- #
        width = int(0.5*self.root.winfo_screenwidth())
        height = int(0.5*self.root.winfo_screenheight())        
        # set the window position
        x_pos = (self.root.winfo_screenwidth() - width) // 2
        y_pos = (self.root.winfo_screenheight() - height) // 2
        self.root.geometry(f"{width}x{height}+{x_pos}+{y_pos}")
        self.root.minsize(width, height)
        self.root.resizable(False, False)
        self.home()
        # Run the application
        self.root.mainloop()
    
    def home(self):
        """Home page of Lumatic"""
        self.clear()
        # =============== #
        # === Toolbar === #
        # =============== #
        
        # === Main menu === #
        self.toolbar = Menu(self.root)
        self.root.config(menu=self.toolbar)

        # === (toolbar) Settings menu === #
        self.settingsMenu = Menu(self.toolbar, tearoff=0)
        self.toolbar.add_cascade(label=self.lang.getMenuValue("settingsMenu", "sett"), menu=self.settingsMenu)
        # --- (toolbar>settingsMenu) Languages --- #
        self.languagesMenu = Menu(self.settingsMenu, tearoff=0)
        self.settingsMenu.add_cascade(label=self.lang.getSubMenuValue("settingsMenu", "languagesMenu", "lang"), menu=self.languagesMenu)
        # (toolbar>settingsMenu>languagesMenu) options
        self.languagesMenu.add_command(label=self.lang.getSubMenuValue("settingsMenu", "languagesMenu", "en"), command=lambda:self.setPref("selected", "english"))
        self.languagesMenu.add_command(label=self.lang.getSubMenuValue("settingsMenu", "languagesMenu", "fr"), command=lambda:self.setPref("selected", "french"))
        self.languagesMenu.add_command(label=self.lang.getSubMenuValue("settingsMenu", "languagesMenu", "de"), command=lambda:self.setPref("selected", "german"))
        # --- (toolbar>settingsMenu) Preferences --- #
        self.preferencesMenu = Menu(self.settingsMenu, tearoff=0)
        self.settingsMenu.add_cascade(label=self.lang.getSubMenuValue("settingsMenu", "preferencesMenu", "prefs"), menu=self.preferencesMenu)
        # (toolbar>settingsMenu>preferencesMenu) options
        if self.lang.getDict()["pop-ups"] == "False":
            self.preferencesMenu.add_command(label=self.lang.getSubMenuValue("settingsMenu", "preferencesMenu", "pops-enable"), command=lambda:self.setPref("pop-ups", "True"))
        else:
            self.preferencesMenu.add_command(label=self.lang.getSubMenuValue("settingsMenu", "preferencesMenu", "pops-disable"), command=lambda:self.setPref("pop-ups", "False"))

        # === (toolbar) Tutorials menu === #
        self.tutorialsMenu = Menu(self.toolbar, tearoff=0)
        self.toolbar.add_cascade(label=self.lang.getMenuValue("tutorialsMenu", "tuto"), menu=self.tutorialsMenu)
        # --- (toolbar>tutorialsMenu) Hack menu --- #
        self.hackMenu = Menu(self.tutorialsMenu, tearoff=0)
        self.tutorialsMenu.add_cascade(label=self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "hack"), menu=self.hackMenu)
        # (toolbar>tutorialsMenu>hackMenu) options
        self.hackMenu.add_command(label="Reset Parental Code", command=lambda:resetPsw(self))

        # ======================== #
        # === Buttons & Labels === #
        # ======================== #

        # === Hack ONLY === #
        # Progress bar to display the advancement of the process
        try:
            # check if the progress bar has already been generated
            self.progress_label.configure(text=self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "progress")) 
        except:
            # Create the progress label
            self.progress_label = Label(self.root, text=self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "progress"))
            self.progress_label.pack()
            # Create the progress bar
            self.progress_bar = Progressbar(self.root, length=int(0.5*self.root.winfo_screenwidth()))
            self.progress_bar.pack()
        # Frame to display entry + button on the same row
        frame = Frame(self.root)
        frame.pack()
        # --- Entry --- #
        self.entry = Entry(frame, bg="white", width=50, borderwidth=2)        
        self.entry.insert(0, self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "entry"))
        self.entry.grid(row=0, column=0, pady=0.1*self.root.winfo_screenmmheight())
        # --- Clear Entry --- #
        self.clear_button = Button(frame, text=self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "clear"), command=self.clearEntry)
        self.clear_button.grid(row=0, column=1)

        # --- Button --- #
        self.hack0 = PhotoImage(file="photos/buttons/hack_only.png")
        b = Button(self.root, image=self.hack0, cursor="hand2", borderwidth=0, command=lambda:self.warn())
        b.pack(pady=0.1*self.root.winfo_screenmmheight())
        CreateToolTip(b, self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "tip1"))
        
        # === Hack + Apps === #
        # --- Button --- #
        self.hack1 = PhotoImage(file="photos/buttons/hack_apps.png")
        b = Button(self.root, image=self.hack1, cursor="hand2", borderwidth=0, command=lambda:self.warn(1))
        b.pack(pady=0.1*self.root.winfo_screenmmheight())
        CreateToolTip(b, self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "tip2"))

    def clearEntry(self):
        self.entry.delete(0, "end")

    def msg(self, title: str, message: str):
        """Display a message to the user
        
        Arguments:
            - {str} title  : title of the pop-up
            - {str} message: pop-up informations
        """
        return messagebox.showinfo(title, message)

    def warn(self, mode=None):
        """Warn the user of prerequisites
        
        Argument:
            - {integer} mode: None (simple hack) OR 1 (hack + applications)
        """
        pop_ups = self.lang.getDict()["pop-ups"]
        if pop_ups == "True":            
            messagebox.showwarning(self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "warn"), self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "steps"))
        # Create a new thread to perform the hack function
        def hackThread():
            if mode == 1:
                if pop_ups == "True":                    
                    if messagebox.askquestion(self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "sdCapacity"), self.lang.getSubMenuValue("tutorialsMenu", "hackMenu", "askStorage")) == "no":
                        return
                hack(1, self.entry.get(), self, self.lang) # hack the console and install the games
            else:            
                hack(0, self.entry.get(), self, self.lang) # hack the console only
        Thread(target=hackThread).start()
       
    def clear(self):
        """Deletes all widgets on the window"""
        for w in self.root.slaves(): # list of the widgets of the window
            #if w != self.progress_label and w != self.progress_bar: # exept the progress label and the progressbar
                w.destroy()

    def setPref(self, pref, value):
        self.lang.setPref(pref, value)
        self.home()