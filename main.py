iname="icon.ico"
ipath="C:\\tmp\\"
notifyPerc=84
showNotifications=True


from infi.systray import SysTrayIcon
from PIL import Image, ImageDraw,ImageFont
import time
import subprocess
import os
from win10toast import ToastNotifier
toast = ToastNotifier()
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW
def on_quit_callback(systray):
    os._exit(0)
image= ipath+iname
if not os.path.isdir(ipath):
    os.mkdir(ipath)
n=1
bat=0
rawbat=""
last=-1
noteA=0
noteB=0
try:
    while True:
        # create image
        img = Image.new('RGBA', (50, 50), color = (0, 0, 0, 0))  # color1 background =  white  with transparency
        d = ImageDraw.Draw(img)
        #d.rectangle([(0, 40), (50, 50)], fill=(255, 255, 255), outline=None)  #  color = blue
        #add text to the image
        font_type  = ImageFont.truetype("arial.ttf", 50)
        try:
            rawbat=subprocess.check_output(['adb', 'shell', 'dumpsys', 'battery'], startupinfo=si).decode("utf-8")
        except:
            rawbat=""
            noteA=0
            noteB=0

        try:
            #print(str(rawbat))
            for line in rawbat.split("\n"):
                if "level" in line:
                    last=bat
                    bat=line.split(":")[1].strip()
                    if int(bat)>=notifyPerc:
                        color=(0,255,0)
                        if noteA==0 and showNotifications:
                            toast.show_toast(
                                "Battery almost full",
                                "Your battery has reached "+bat+"%.",
                                duration = 3,
                                icon_path = image,
                                threaded = True,
                            )
                        noteA=1

                    else:
                        color=(255,255,255)
                        noteA=0
                    if last!=bat:
                        if bat=="100":
                            font_type  = ImageFont.truetype("arial.ttf", 30)
                            if noteB==0 and showNotifications:
                                toast.show_toast(
                                    "Battery full",
                                    "Your battery has reached 100%",
                                    duration = 5,
                                    icon_path = image,
                                    threaded = True,
                                )
                            noteB=1
                        else:
                            noteB=0
                            font_type  = ImageFont.truetype("arial.ttf", 45)
                        d.text((0,0), bat, fill=color, font = font_type)
                        img.save(image)
                        #print(bat)
                    break
            else:
                last=bat
                noteA=0
                noteB=0
                bat="N/A"
                if bat!=last:
                    font_type  = ImageFont.truetype("arial.ttf", 30)
                    d.text((0,0), bat, fill=(255,0,0), font = font_type)
                    img.save(image)
        except Exception as e:
            #print(e)
            time.sleep(10)
        # display image in systray
        if n==1:
            systray = SysTrayIcon(image, "Android battery percentage",on_quit=on_quit_callback)
            systray.start()
        else:
            systray.update(icon=image)
        time.sleep(10)
        n+=1
except KeyboardInterrupt:
    os._exit(0)