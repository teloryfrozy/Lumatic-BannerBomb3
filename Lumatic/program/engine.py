##############################################
#   Script to hack 8th generation consoles   #
##############################################
from json import dump, load
from threading import Thread
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
from os import listdir, getlogin, mkdir, remove, path
from shutil import copy, copytree, move
from zipfile import ZipFile


class Language:
    """Access to text and translation for Lumatic"""
    def __init__(self):
        self.path = "settings/lang.json"

    def setPref(self, pref, value):
        """Changes the selected language
        
        Argument:
            - {string} pref: preference
            - {string} value: value of the preference 
        """
        lang = self.getDict()
        lang[pref] = value # modify the value
        with open(self.path, "w") as f:
            dump(lang, f, indent=4) # saves the modifications
    
    def getDict(self):
        """Returns only the translation of the selected language"""
        with open(self.path) as f:
            return load(f)
    
    def getMenuValue(self, menu: str, key: str) -> str:
        """Returns the word associated with the key for a menu
        
        Arguments:
            - {string} mengetDictu: menu on the toolbar
            - {string} key: menu name
        """
        selected = self.getDict()["selected"]
        return self.getDict()[selected][menu][key]
    
    def getSubMenuValue(self, menu: str, sub: str, key: str) -> str:
        """Returns the word associated with the key for a sub-menu
        
        Arguments:
            - {string} menu: menu on the toolbar
            - {string} sub : sub-menu on the toolbar
            - {string} key : option name
        """ 
        selected = self.getDict()["selected"]
        return self.getDict()[selected][menu][sub][key]

def resetPsw(gui):
    """Redirect to a website to reset the parental code of your console
    
    Arg:
        - {GUI} gui: GUI object
    """
    gui.driver = webdriver.Firefox()
    gui.driver.get("https://mkey.salthax.org/")
    gui.driver.maximize_window()

def play(gui, video: str):
    """Plays the video specified
    
    Arguments:
        - {GUI}     gui : object from class GUI
        - {string} video: name of the video + format
    """
    from tkVideoPlayer import TkinterVideo
    from tkinter import Button
    # Display the video
    gui.clear()
    # relative path to the video
    path = "videos/" + video
    def removeVideo():
        videoplayer.stop() # stop the video
        videoplayer.pack_forget() # remove the video widget from the parent window
        remove_button.destroy()
        gui.home()
    # Settings of the video
    videoplayer = TkinterVideo(gui.root, scaled=True)
    videoplayer.load(path)
    videoplayer.pack(expand=True, fill="both")    
    videoplayer.play() # play the video
    # Add a "Remove Video" button
    remove_button = Button(gui.root, text="Remove Video", command=lambda:removeVideo())
    remove_button.pack(pady=10)

def waitDownload(file: str, os_name):
    """Function to verify if files are downloading

    Argument:
        - {string} file: file that is supposed to be downloaded

    Method:
        1) Wait time seconds
        2) Check if the file is downloaded
        3) Continue until it is downloaded
    """
    # Verification of OS
    if os_name == "Linux":
        file_path = "/home/" + getlogin() + "/Downloads/" + file
    elif os_name == "Windows":
        file_path = "C:\\Users\\" + getlogin() + "\\Downloads\\" + file
    
    while True:
        if path.exists(file_path) and not file_path.endswith(".part"):
            return
        sleep(1)

def hack(mode: int, fc: str, gui, lang_file):
    """Function to hack 8th generation consoles
    
    Arguments:
        - {integer} mode: 0 (simple hack) OR 1 (hack + applications)
        - {string} fc: Friend code of the console user
        - {GUI} gui: object from class GUI
        - {Json File} lang_file: file of all translation and preferences

    Method:
        1) Install required files on the root of the SD card
        2) Generate the injectables files
        3) Install the injectables files
    """
    # --- Paths --- #
    # Manjaro KDE Plasma
    if gui.os_name == "Linux":
        from psutil import disk_partitions
        # Algorithm to get the path of the USB Key
        for partition in disk_partitions():
            if partition.device == '/dev/sdc1':
                sd_path = partition.mountpoint + "/"
    # Windows 10
    elif gui.os_name == "Windows":
        # /!\ only works on Windows /!\
        from string import ascii_uppercase
        from psutil import disk_partitions
        # Algorithm to get the path of the USB Key
        for partition in disk_partitions():
            if 'removable' in partition.opts:
                drive_letter = partition.device.split(':\\')[0]
                drive_name = ascii_uppercase[ascii_uppercase.index(drive_letter):ascii_uppercase.index(drive_letter)+1]
                sd_path = drive_name + ":\\"
    try:
        # Test if the sd card is inserted in the computer
        listdir(sd_path)
    except:
        gui.msg(lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "ntFound"), lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "insertSD"))
    nin3DS_dir_path = sd_path + "Nintendo 3DS/"
    # Find id0
    for i in range(len(listdir(nin3DS_dir_path))):
        if len(listdir(nin3DS_dir_path)[i]) > 30: # property of id0
            id0 = listdir(nin3DS_dir_path)[i]
            break
    
    # --- Seedminer --- #
    # Web related variables
    browser = webdriver.Firefox()
    adresses = {
        "seedminer": "https://seedminer.hacks.guide/",
        "bb3"      : "https://3dstools.nhnarwhal.com/#/bb3gen"
    }
    browser.get(adresses["seedminer"])
    # Fill required sections
    browser.find_element(By.ID, "friendCode").send_keys(fc)
    browser.find_element(By.ID, "id0").send_keys(id0)

    # Start the process
    browser.find_element(By.ID, "beginButton").click()
    # Display a message to add the bot
    if lang_file.getDict()["pop-ups"] == "True":
        wait = True
        while wait:
            # case where the friend code has already been used
            if browser.find_element(By.ID, "downloadMovable2").get_attribute("href") != "https://seedminer.hacks.guide/#":
                wait = False
            # check if the friend code of the bot is visible
            if "show" in browser.find_element(By.ID, "collapseTwo").get_attribute("class"):
                wait = False
                gui.msg(lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "fb"), lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "addBot") + browser.find_element(By.XPATH, "/html/body/main/div/div[4]/div[2]/div[2]/div[1]/div[1]/b[2]/span").text)
        
    def preparation():
        """Thread to prepare the SD card and copy all required files"""
        # Create Nintendo DSiWare directory
        mkdir(nin3DS_dir_path + id0 + "/" + listdir(nin3DS_dir_path + id0)[0] + "/Nintendo DSiWare")
        # Copy/Paste SD files on the root
        for file in listdir("ressources/SD"):
            if path.isfile("ressources/SD/" + file):
                copy("ressources/SD/" + file, sd_path + file)
            else:
                copytree("ressources/SD/" + file, sd_path + file)    

        # Hack + applications
        if mode == 1:
            # Copy/Paste themes and games
            mkdir(sd_path + "roms/")
            copytree("ressources/Themes/", sd_path + "Themes")
            for game in listdir("ressources/games/"):
                copy("ressources/games/" + game, sd_path + "archives/" + game)
            for folder in listdir("ressources/roms/"):
                copytree("ressources/roms/" + folder, sd_path + "roms/" + folder)
            
            # Show that the process is finished
            gui.progress_bar["value"] = 100
            # Display a message to eject SD
            if lang_file.getDict()["pop-ups"] == "True":
                gui.msg(lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "sd"), lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "ejectSD"))
                gui.progress_bar["value"] = 0 # reset the progress bar

    def injection():
        """Thread to get the hacked files"""
        # --- Reset the progress bar --- #
        gui.progress_bar["value"] = 0
        # Wait for the link
        wait = True
        while wait:
            if browser.find_element(By.ID, "downloadMovable2").get_attribute("href") != "https://seedminer.hacks.guide/#": # link enabled
                wait = False

        # Download movable.sed
        browser.find_element(By.ID, "downloadMovable2").click()
        # Wait until download is finished
        waitDownload("movable.sed", gui.os_name)
        
        # --- BannerBomb3 --- #
        # Estimated time : ~10 sec #
        browser.get(adresses["bb3"])
        # Import movable.sed
        if gui.os_name == "Linux":
            downloads_path = "/home/" + getlogin() + "/Downloads/"
        elif gui.os_name == "Windows":
           downloads_path = "C:\\Users\\" + getlogin() + "\\Downloads\\"
        browser.find_element(By.ID, "movable").send_keys(downloads_path + "movable.sed")
        # Download bb3
        browser.find_element(By.ID, "build").click()
        waitDownload("DSIWARE_EXPLOIT.zip", gui.os_name)

        # Extract bb3 directory
        zip_file_path = downloads_path + "DSIWARE_EXPLOIT.zip"
        # Wait until zip file is completely downloaded
        while True:
            try:
                with ZipFile(zip_file_path) as zip_file:
                    zip_file.extractall(sd_path)
                break
            except:
                pass
        # Clear the Downloads directory        
        try:
            remove(downloads_path + "movable.sed")
            remove(zip_file_path)
        except:
            pass

        # Copy/Paste bb3 files
        move(sd_path + "F00D43D5.bin", nin3DS_dir_path + id0 + "/" + listdir(nin3DS_dir_path + id0)[0] + "/Nintendo DSiWare/")

        # --- Finish properly --- #
        browser.close()

        # Display a message to eject SD card if the user clicked on Hack only        
        if mode == 0:
            # Show that the process is finished
            gui.progress_bar["value"] = 100
            if lang_file.getDict()["pop-ups"] == "True":
                gui.msg(lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "sd"), lang_file.getSubMenuValue("tutorialsMenu", "hackMenu", "ejectSD"))
                gui.progress_bar["value"] = 0 # reset the progress bar

    def progression():
        """Thread to run and update the progress bar during the hack"""
        if mode == 1:
            sleep(150)
        else:
            sleep(30)
        gui.progress_bar["value"] += 5
        if gui.progress_bar["value"] < 100:
            progression()

    # Start Threads
    Thread(target=progression).start()
    Thread(target=injection).start()
    Thread(target=preparation).start()

    # --- Final time --- #
    # Mode = 0 : 10 min
    # Mode = 1 : 50 min