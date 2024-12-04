import ctypes
import os
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import time
import json
import threading


def getScreenResolution():
    user32 = ctypes.windll.user32
    user32.SetProcessDPIAware()
    screenWidth = user32.GetSystemMetrics(0)
    userScreenHeight = user32.GetSystemMetrics(1)
    return screenWidth, userScreenHeight


def setWallpaper(imagePath):
    ctypes.windll.user32.SystemParametersInfoW(20, 0, imagePath, 3)


def createImageWithText(text, imagePath, borderThickness=30):
    screenWidth, userScreenHeight = getScreenResolution()
    img = Image.new("RGB", (screenWidth, userScreenHeight), color=(0, 0, 0))
    drawerThing = ImageDraw.Draw(img)
    fontPath = "Minecraft.ttf"
    textFont = ImageFont.truetype(fontPath, 48)
    textBox = drawerThing.textbbox((0, 0), text, font=textFont)
    textWidth = textBox[2] - textBox[0]
    textHeight = textBox[3] - textBox[1]
    textPosition = ((screenWidth - textWidth) // 2, (userScreenHeight - textHeight) // 2)
    textColor = (250, 20, 90)
    drawerThing.text(textPosition, text, font=textFont, fill=textColor)
    for i in range(borderThickness):
        drawerThing.rectangle(
            [i, i, img.size[0] - i - 1, img.size[1] - i - 1],
            outline=(35, 25, 35)
        )
        drawerThing.rectangle(
            [i + 3, i + 3, img.size[0] - i - 4, img.size[1] - i - 4],
            outline=(255, 255, 255)
        )
    img.save(imagePath)


def readJson(filePath):
    with open(filePath, 'r') as file:
        dataThing = json.load(file)
    return dataThing


def updateWallpaper():
    global jsonData
    imagePath = os.path.join(os.getcwd(), "wallpaper.jpg")
    while True:
        userName = jsonData["user"]
        taskList = "\n".join(jsonData["tasks"])
        currentTime = datetime.now().strftime("%H:%M:%S")
        currentDate = datetime.now().strftime("%m/%d/%y")
        currentDay = datetime.now().strftime("%A")
        fancyText = (f"Welcome: {userName}\n\n\n"
                     f"-------------------------------\n"
                     f"\nTime = {currentTime}"
                     f"\nDate = {currentDate}"
                     f"\nDay = {currentDay}"
                     f"\n\n\nTo Do"
                     f"\n-------------------------------"
                     f"\n{taskList}")
        createImageWithText(fancyText, imagePath)
        setWallpaper(imagePath)
        time.sleep(1)


def listenForCommands():
    global jsonData
    while True:
        userCommand = input("Enter command: ")
        if userCommand.lower() == "new":
            jsonData = readJson("stuff.json")
            print("JSON data reloaded.")


if __name__ == "__main__":
    jsonData = readJson("stuff.json")
    wallpaperThread = threading.Thread(target=updateWallpaper)
    commandThread = threading.Thread(target=listenForCommands)
    wallpaperThread.start()
    commandThread.start()
    wallpaperThread.join()
    commandThread.join()
