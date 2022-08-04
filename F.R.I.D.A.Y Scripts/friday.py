import os
import sys
import subprocess
import win32com
import platform
import tkinter    
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox
from tkinter import scrolledtext
import numpy
import random
import json
import math
import datetime
import calendar
import speech_recognition
import pyttsx3
import time
import urllib.request
import webbrowser
import wikipedia
import wolframalpha
import ctypes
from tkinter import _tkinter
from PIL import ImageTk,Image

engine = pyttsx3.init()
engine.setProperty("rate", 150)
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)
window = Tk()

window.configure(bg = "black")
SET_WIDTH = 800
SET_HEIGHT = 600

global ques

ques = Entry(window,width=50,bg="black",fg="white",font = ("arial",18,"bold"))   
ques.pack(padx = 10,pady = 20)

current_datetime = datetime.datetime.now()
today = datetime.datetime.today().weekday()
today_name = calendar.day_name[today]
current_date = current_datetime.strftime("%m/%d/%y")
current_time = datetime.datetime.now().strftime("%H:%M:%S")

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def check_compatibility():
    system = str(platform.system()).lower()
    release = str(platform.release()).lower().split("-")[0]
    machine = str(platform.machine()).lower()
    if not machine in ("x64", "amd64"):
        try:
            speak("i'm sorry sir but i cannot help you now because your device's system is not supported. your computer's system must be 64-bit or amd-64")
        except:
            messagebox.showerror(title = "System Compatibility Error", message = "Your device's system is not supported. Your computer's system must be 64-bit or AMD-64.")
        sys.exit()       
    elif not system == "windows":
        if not release in ("8", "10", "11", "12"):
            try:
                speak("i'm sorry sir but i cannot help you now because your operating system is not supported. your computer's os must be windows 8 or higher versions")
            except:
                messagebox.showerror(title = "System Compatibility Error", message = "Your Operating System is not supported. Your computer's OS must be Windows 8 or higher versions.")
            sys.exit()
        else:
            try:
                speak("i'm sorry sir but i cannot help you now because your operating system is not supported. your computer's os must be windows operating system")
            except:
                messagebox.showerror(title = "System Compatibility Error", message = "Your Operating System is not supported. Your computer's OS must be Windows Operating System.")
            sys.exit()

with open("greetings.json") as g_dat:
    greetings = json.load(g_dat)

with open("conversations.json") as c_dat:
    conversations = json.load(c_dat)

def check_connection():
    try:
        urllib.request.urlopen("https://dns.google", timeout=10)
        return
    except:
        speak("i'm sorry sir but i cannot help you now because you are not connected to the internet or the connection is unstable which may cause some functions to be unavailable. please connect to the internet and try restarting")
        sys.exit()

def greeting():
    hour = int(current_datetime.hour)

    if hour > 0 and hour <= 12:
        speak("good morning sir, how can i help you?")

    elif hour > 12 and hour <= 18:
        speak("good afternoon sir, how can i help you?")

    else:
        speak("good evening sir, how can i help you?")

def command():

    if not ques.get():
        return

    if "launch" in ques.get().lower() or "run" in ques.get().lower() or "start" in ques.get().lower() or "open" in ques.get().lower():
        if "file" in ques.get().lower() or "files" in ques.get().lower():
            speak("which file do you want to open sir?")
            d = Toplevel(bg = "black")
            d.title("Open File")
            l = Label(d, bg = "black", fg = "white", text = "Enter file name (including path)")
            l.pack()
            e = Entry(d ,bg = "black", fg = "white", width = 100)
            e.pack()
            def open_file():
                if not e.get():
                    return
                speak("ok sir i will open it for you")
                try:
                    os.startfile(e.get())
                except:
                    speak(f"sorry sir i could not find it")
            def explorer():
                docs = os.path.join(os.environ["userprofile"], "documents")
                filename = filedialog.askopenfilename(initialdir = docs)
                if not filename:
                    return
                e.insert(0, filename)
                try:
                    os.startfile(filename)
                except:
                    messagebox.showerror(title = "File Open Error", message = f"An error occured while opening {filename}.")
            s = Button(d,bg = "black", fg  = "white",activeforeground = "grey",activebackground = "white",text = "Open",command=open_file)
            s.pack()
            b = Button(d,bg = "black", fg  = "white",activeforeground = "grey",activebackground = "white",text = "Browse files",command=explorer)
            b.pack()
        elif "program" in ques.get().lower() or "programs" in ques.get().lower() or "app" in ques.get().lower() or "apps" in ques.get().lower() or "application" in ques.get().lower() or "applications" in ques.get().lower():
            speak("which program do you want to launch sir?")
            d = Toplevel(bg = "black")
            d.title("Open Program")
            l = Label(d, bg = "black", fg = "white", text = "Enter program (app) name")
            l.pack()
            e = Entry(d, bg = "black", fg = "white", width = 100)
            e.pack()
            def open_program():
                if not e.get():
                    return
                speak(f"ok sir i will open {e.get()} for you")
                try:
                    appname = subprocess.getoutput(f"powershell -Command get-StartApps {e.get()}").split()[-1]
                    subprocess.run(f"explorer Shell:AppsFolder\{appname}", shell=True)
                except:
                    speak(f"sorry sir i could not find {e.get()}")
            def programsfolder():
                startmenu = os.path.join(os.environ["programdata"], "microsoft", "windows", "start menu", "programs")
                filename = filedialog.askopenfilename(initialdir = startmenu)
                if not filename:
                    return
                e.insert(0, filename)
                try:
                    os.startfile(filename)
                except:
                    messagebox.showerror(title = "Program Open Error", message = f"An error occured while opening {filename}.")
            def appsfolder():
                subprocess.run("explorer Shell:AppsFolder", shell=True)
            s = Button(d,bg = "black", fg  = "white", activeforeground = "grey",activebackground = "white",text = "Open",command=open_program)
            s.pack()
            b = Button(d,bg = "black", fg  = "white", activeforeground = "grey",activebackground = "white",text = "Browse Programs in Programs Folder",command=programsfolder)
            b.pack()
            b = Button(d,bg = "black", fg  = "white", activeforeground = "grey",activebackground = "white",text = "Apps Folder",command=appsfolder)
            b.pack()
        else:
            speak("what do you want to open sir, a file or a program? can you please specify the object you want to open in your next command?")
       
    elif "cmd" in ques.get().lower() or "command prompt" in ques.get().lower():
        speak("ok sir i will open command prompt")
        subprocess.run("start cmd.exe", shell=True)

    elif "powershell" in ques.get().lower():
        speak("ok sir i will open windows powershell")
        subprocess.run("start powershell.exe", shell=True)

    elif "control panel" in ques.get().lower():
        speak("ok sir i will open control panel")
        subprocess.run("start control.exe", shell=True)

    elif "settings" in ques.get().lower():
        speak("ok sir i will open settings")
        subprocess.run("start ms-settings:", shell=True)

    elif "file explorer" in ques.get().lower() or "windows explorer" in ques.get().lower():
        speak("ok sir i will open file explorer")
        subprocess.run("start explorer.exe", shell=True)

    elif "date" in ques.get().lower() or "time" in ques.get().lower():
        speak("ok sir i will show you the current date and time")
        d = Toplevel(bg = "black")
        d.title("Current Date & Time")
        l1 = Label(d, bg = "black", fg = "white", font=200, text = today_name)
        l1.pack()
        l2 = Label(d, bg = "black", fg = "white", font=200, text = current_date)
        l2.pack()
        l3 = Label(d, bg = "black", fg = "white", font=200, text = current_time)
        l3.pack()

    elif "shutdown" in ques.get().lower():
        subprocess.run("shutdown -s -t 10", shell=True)
        speak("ok sir i will shutdown the computer in 10 seconds. make sure you have saved all your data and work")

    elif "google" in ques.get().lower() and "search" in ques.get().lower():
        speak("what do you want to search on google sir?")
        d = Toplevel(bg = "black")
        d.title("Google Search")
        l = Label(d, bg = "black", fg = "white", text = "Enter queries or key words")
        l.pack()
        e = Entry(d,bg = "black", fg = "white", width = 100)
        e.pack()
        def open_web():
            speak("ok sir i will search for "+e.get())
            if not e.get():
                return
            try:
                webbrowser.open(f"https://www.google.com/search?q={e.get()}")
            except:
                speak(f"sorry sir i could not search for {e.get()}")
        s = Button(d,bg = "black",fg  = "white",activeforeground = "grey",activebackground = "white",text = "Search",command=open_web)
        s.pack()

    elif "google" in ques.get().lower():
        speak("ok sir i will open google")
        try:
            webbrowser.open("https://wwww.google.com")
        except:
            speak("sorry sir i could not open google")

    elif "bing" in ques.get().lower() and "search" in ques.get().lower():
        speak("what do you want to search on bing sir?")
        d = Toplevel(bg = "black")
        d.title("Bing Search")
        l = Label(d, bg = "black", fg = "white", text = "Enter queries or key words")
        l.pack()
        e = Entry(d,bg = "black", fg = "white", width = 100)
        e.pack()
        def open_web():
            speak("ok sir i will search for "+e.get())
            if not e.get():
                return
            try:
                webbrowser.open(f"https://www.bing.com/search?q={e.get()}")
            except:
                speak(f"sorry sir i could not search for {e.get()}")
        s = Button(d,bg = "black",fg  = "white",activeforeground = "grey",activebackground = "white",text = "Search",command=open_web)
        s.pack()

    elif "bing" in ques.get().lower():
        speak("ok sir i will open bing")
        try:
            webbrowser.open("https://wwww.bing.com")
        except:
            speak("sorry sir i could not open bing")

    elif "wiki" in ques.get().lower() or "wikipedia" in ques.get().lower():
        speak("what do you want to search for sir?")
        d = Toplevel(bg = "black")
        d.title("Wikipedia")
        l = Label(d, bg = "black", fg = "white", text = "Enter queries or key words")
        l.pack()
        e = Entry(d,bg = "black", fg = "white", width = 100)
        e.pack()
        txt = scrolledtext.ScrolledText(d, bg="black", fg="white")
        txt.pack()
        txt.config(state=DISABLED)
        def search():            
            if not e.get():
                return
            try:
                ans = wikipedia.summary(e.get())
                txt.config(state=NORMAL)
                txt.delete("1.0", END)
                txt.insert(END, ans)
                txt.config(state=DISABLED)
            except:
                speak("sorry i could not find it from wikipedia sir")
        s = Button(d,bg = "black",fg  = "white",activeforeground = "grey",activebackground = "white",text = "Search",command=search)
        s.pack()

    elif "wolf" in ques.get().lower() or "wolfram" in ques.get().lower() or "wolframalpha" in ques.get().lower():
        speak("what do you want to solve sir?")
        d = Toplevel(bg = "black")
        d.title("Wolfram Alpha")
        l = Label(d, bg = "black", fg = "white", text = "Enter problems or questions")
        l.pack()
        e = Entry(d,bg = "black", fg = "white", width = 100)
        e.pack()
        txt = scrolledtext.ScrolledText(d, bg="black", fg="white")
        txt.pack()
        txt.config(state=DISABLED)
        def solve():            
            if not e.get():
                return
            try:
                app_id="8442YL-RHPH7JGJPY"
                client = wolframalpha.Client(app_id)
                res = client.query(e.get())
                sol = next(res.results).text
                txt.config(state=NORMAL)
                txt.delete("1.0", END)
                txt.insert(END, sol)
                txt.config(state=DISABLED)
            except:
                speak("sorry i could not find it from wolfram alpha sir")
        s = Button(d,bg = "black",fg  = "white",activeforeground = "grey",activebackground = "white",text = "Solve",command=solve)
        s.pack()

    elif "wolfram" in ques.get().lower() and "alpha" in ques.get().lower():
        speak("what do you want to solve sir?")
        d = Toplevel(bg = "black")
        d.title("Wolfram Alpha")
        l = Label(d, bg = "black", fg = "white", text = "Enter problems or questions")
        l.pack()
        e = Entry(d,bg = "black", fg = "white", width = 100)
        e.pack()
        txt = scrolledtext.ScrolledText(d, bg="black", fg="white")
        txt.pack()
        txt.config(state=DISABLED)
        def solve():            
            if not e.get():
                return
            try:
                app_id="8442YL-RHPH7JGJPY"
                client = wolframalpha.Client(app_id)
                res = client.query(e.get())
                sol = next(res.results).text
                txt.config(state=NORMAL)
                txt.delete("1.0", END)
                txt.insert(END, sol)
                txt.config(state=DISABLED)
            except:
                speak("sorry i could not find it from wolfram alpha sir")
        s = Button(d,bg = "black",fg  = "white",activeforeground = "grey",activebackground = "white",text = "Solve",command=solve)
        s.pack()

    elif "website" in ques.get().lower() or "domain" in ques.get().lower():
        speak("which website sir?")
        d = Toplevel(bg = "black")
        d.title("Open Website")
        l = Label(d, bg = "black", fg = "white", text = "Enter website (domain) name")
        l.pack()
        e = Entry(d,bg = "black", fg = "white", width = 100)
        e.pack()
        def open_web():
            speak("ok sir i will open "+e.get())
            if not e.get():
                return
            try:
                webbrowser.open(f"https://{e.get()}")
            except:
                speak("sorry sir i could not open that website")
        s = Button(d,bg = "black",fg  = "white",activeforeground = "grey",activebackground = "white",text = "Open",command=open_web)
        s.pack()

    elif "calculator" in ques.get().lower():
        speak("ok sir i will open calculator")
        try:
            cal = subprocess.getoutput("powershell -Command get-StartApps Calculator").split()[-1]
            subprocess.run(f"explorer Shell:AppsFolder\{cal}", shell=True)
        except:
            try:
                speak("failed to open calculator app, i will try launching calc.exe")
                subprocess.run("start calc.exe", shell=True)
            except:
                speak("sorry sir i could not open calculator")

    elif "mail" in ques.get().lower():
        speak("ok sir i will open the mail app")
        try:
            mail = subprocess.getoutput("powershell -Command get-StartApps Mail").split()[-1]
            subprocess.run(f"explorer Shell:AppsFolder\{mail}", shell=True)
        except:
            try:
                speak("failed to open mail app, i will try launching mailto from the web browser")
                webbrowser.open("mailto:", new=1)
            except:
                speak("sorry sir i could not open the mail app")
            
    elif "news" in ques.get().lower() or "msn" in ques.get().lower():
        speak("ok sir i will open the latest news from msn")
        try:
            webbrowser.open("https://wwww.msn.com/news")
        except:
            speak("sorry sir i could not open msn website")

    elif "cia" in ques.get().lower() or "central intelligence agency" in ques.get().lower():
        speak("ok sir i will go to cia official website")
        try:
            webbrowser.open("https://www.cia.gov")
        except:
            speak("sorry sir i could not open cia website")

    elif "fbi" in ques.get().lower() or "federal bureau of investigation" in ques.get().lower():
        speak("ok sir i will go to fbi official website")
        try:
            webbrowser.open("https://www.fbi.gov")
        except:
            speak("sorry sir i could not open fbi website")

    elif "exit" in ques.get().lower() or "quit" in ques.get().lower():
        speak("good bye sir, have a good day")
        window.destroy()
        
    else:
        try:
            ans1 = list(kwd1 for kwd1 in conversations if kwd1 in ques.get().lower())
            speak(conversations[ans1[-1]])
        except:
            try:
                ans2 = list(kwd2 for kwd2 in greetings if kwd2 in ques.get().lower())
                speak(greetings[ans2[-1]])
            except:
                speak("i'm sorry sir but i was not programmed to answer that")

def listen(): 
    recognizer = speech_recognition.Recognizer()
    microphone = speech_recognition.Microphone()
    with microphone as source:
        try:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source, timeout = 10)
            command = recognizer.recognize_google(audio)
            ques.insert(END, command)
        except:
            try:
                command = recognizer.recognize_sphinx(audio)
                ques.insert(END, command)
            except:                
                speak("sorry sir i could not hear that")
            
def speech_input():
    listen()
    command()
    
def cmd():
    speak("ok sir i will open command prompt")
    subprocess.run("start cmd.exe", shell=True)

def psh():
    speak("ok sir i will open windows powershell")
    subprocess.run("start powershell.exe", shell=True)

def ctrl():
    speak("ok sir i will open control panel")
    subprocess.run("start control.exe", shell=True)

def settings():
    speak("ok sir i will open settings")
    subprocess.run("start ms-settings:", shell=True)

def explorer():
    speak("ok sir i will open file explorer")
    subprocess.run("start explorer.exe", shell=True)

def main():
    # screen

    bgImg = Image.open(os.path.join(os.getcwd(), "tk", "images", "background.png"))
    window.title("F.R.I.D.A.Y")
    window.iconbitmap(os.path.join(os.getcwd(), "tk", "images", "appicon.ico"))
    canvas = tkinter.Canvas(window,width = SET_WIDTH,height = SET_HEIGHT)

    image=ImageTk.PhotoImage(bgImg)
    canvas.create_image(0,0,anchor=NW,image=image)

    # entry

    btn = Button(text = "Command Prompt" ,bg = "black",fg = "white" ,activeforeground  = "grey" ,activebackground = "black", width = 20, command = cmd)
    btn.pack(side = TOP)

    btn = Button(text = "Windows PowerShell" ,bg = "black",fg = "white" ,activeforeground  = "grey" ,activebackground = "black", width = 20, command = psh)
    btn.pack(side = TOP)

    btn = Button(text = "Control Panel" ,bg = "black",fg = "white" ,activeforeground  = "grey" ,activebackground = "black", width = 20, command = ctrl)
    btn.pack(side = TOP)

    btn = Button(text = "Settings" ,bg = "black",fg = "white" ,activeforeground  = "grey" ,activebackground = "black", width = 20, command = settings)
    btn.pack(side = TOP)

    btn = Button(text = "File Explorer" ,bg = "black",fg = "white" ,activeforeground  = "grey" ,activebackground = "black", width = 20, command = explorer)
    btn.pack(side = TOP)
    
    btn = Button(text = "Microphone", bg = "black" ,fg = "white",activeforeground = "grey",activebackground = "black", width = 20, command = speech_input)
    btn.pack(side = BOTTOM)
    
    btn = Button(text = "Enter Command", bg = "black" ,fg = "white",activeforeground = "grey",activebackground = "black", width = 20, command = command)
    btn.pack(side = BOTTOM)
    canvas.configure(bg="black")

    
    
    shape = canvas.create_oval(10,10,100,100,fill = "orange")
    xspeed = random.randrange(1,20)
    yspeed = random.randrange(1, 20)

    shape2 = canvas.create_oval(10,10,100,100,fill = "orange")
    xspeed2 = random.randrange(1,20)
    yspeed2 = random.randrange(1,20)

    canvas.pack()
    
    while True:
        canvas.move(shape,xspeed,yspeed)
        pos = canvas.coords(shape)
        if pos[3]>= 600 or pos[1] <=0:
            yspeed = -yspeed
        if pos[2] >= 800 or pos[0] <=0:
            xspeed= -xspeed

        canvas.move(shape2,xspeed2,yspeed2)
        pos = canvas.coords(shape2)
        if pos[3]>= 600 or pos[1] <=0:
            yspeed2 = -yspeed2
        if pos[2] >= 800 or pos[0] <=0:
            xspeed2= -xspeed2                                
        window.update()
        time.sleep(0.01)
    
def ball():
    canvas = Canvas()



if __name__ == "__main__":
    try:
        check_compatibility()
        check_connection()
        greeting()
        main()
        
        window.mainloop()
    except:
        sys.exit()






















































































































