# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 16:00:15 2022

@author: Afonso Araújo
"""

from random import randint
import time
from tkinter import filedialog as fd

from graphics import *
from Harve import *
from Tree import *
from Charger import *
from Obstacle import *
from Button import *
from math import *
from Findpath import *


# Global Lists
Obstacles = []
Goal = []
Buttons = []
Chargers = []
bars = []
Path = []
global win2
win2 = Point(0,0)
global win3
win3 = Point(0,0)

# Global Variables
GameMode = 0  # 0 mean no gamemode
WindowWidth = 800
WindowHeight = 600
TabSize = 100
ButtonsVerticalSpacement = 50
ButtonsHeight = 30
ObstaclesSize = 5  # Radius

# Global Objects
win = GraphWin("GAME", WindowWidth, WindowHeight, autoflush=False)
LeftTab = Rectangle(Point(0, WindowHeight), Point(TabSize, 0))
RightTab = Rectangle(Point(WindowWidth - TabSize, WindowHeight), Point(WindowWidth, 0))
LeftTab.setFill("light grey")
RightTab.setFill("light grey")

rec1 = Rectangle(Point(WindowWidth-TabSize/2-15, ButtonsVerticalSpacement-5), Point(WindowWidth-TabSize/2+14, ButtonsVerticalSpacement-6))
rec2 = Rectangle(Point(WindowWidth-TabSize/2-15, ButtonsVerticalSpacement+6), Point(WindowWidth-TabSize/2+14, ButtonsVerticalSpacement+5))
rec3 = Rectangle(Point(WindowWidth-TabSize/2-15, ButtonsVerticalSpacement+6), Point(WindowWidth-TabSize/2-14, ButtonsVerticalSpacement-6))
rec4 = Rectangle(Point(WindowWidth-TabSize/2+14, ButtonsVerticalSpacement+6), Point(WindowWidth-TabSize/2+13, ButtonsVerticalSpacement-6))
rec5 = Rectangle(Point(WindowWidth-TabSize/2+17, ButtonsVerticalSpacement+5), Point(WindowWidth-TabSize/2+16, ButtonsVerticalSpacement-5))
rec1.setFill('black')
rec2.setFill('black')
rec3.setFill('black')
rec4.setFill('black')
rec5.setFill('black')

infolabel3 = Text(Point(WindowWidth/2, WindowHeight/2), "Click to Reset")
infolabel3.setFace('courier')
infolabel3.setSize(10)
infolabel4 = Text(Point(WindowWidth-TabSize/2, ButtonsVerticalSpacement*4), "Trees:")
infolabel4.setFace('courier')
infolabel4.setSize(10)
infolabel5 = Text(Point(WindowWidth- TabSize/2 + 30, ButtonsVerticalSpacement*4), "0")
infolabel5.setFace('courier')
infolabel5.setSize(10)

def main():
    global play1_button
    global play2_button
    global play3_button
    global reset_button
    global quit_button
    global run_button
    global reset_button
    
    LeftTab.draw(win)
    RightTab.draw(win)
    play1_button = Button(win, Point(TabSize/2, ButtonsVerticalSpacement*4), (2/3)*TabSize, ButtonsHeight, "Mode 1", Playmode1)
    play2_button = Button(win, Point(TabSize/2, ButtonsVerticalSpacement*5), (2/3)*TabSize, ButtonsHeight, "Mode 2", Playmode2)
    play3_button = Button(win, Point(TabSize/2, ButtonsVerticalSpacement*6), (2/3)*TabSize, ButtonsHeight, "Mode 3", Playmode3)
    reset_button = Button(win, Point(TabSize/2, ButtonsVerticalSpacement), (2/3)*TabSize, ButtonsHeight, "Reset", Reset)
    quit_button = Button(win, Point(TabSize/2, ButtonsVerticalSpacement*2), (2/3)*TabSize, ButtonsHeight, "Quit", Quit)
    run_button = Button(win, Point(TabSize/2, ButtonsVerticalSpacement*3), (2/3)*TabSize, ButtonsHeight, "Run", Run1)
    reset_button.deactivate()
    run_button.deactivate()

    Buttons.append(quit_button)
    Buttons.append(reset_button)
    Buttons.append(play1_button)
    Buttons.append(play2_button)
    Buttons.append(play3_button)
    Buttons.append(run_button)

    while True:
        CheckButtons(win)
        
def Quit():
    win.close()
        
def CheckButtons(win):
    mouse = win.checkMouse()
    if mouse != None:
        for Button in Buttons:
            if Button.clicked(mouse):
                Button.onClick()
                Button.deactivate()
                return True        

def IsInside(x,y,):
    return (TabSize < x < (WindowWidth - TabSize))

def Generatefield():
    Obstacles.append(Obstacle(randint(TabSize+20, 780-TabSize), randint(TabSize+20, 580-TabSize), 0, win))
    Obstacles.append(Obstacle(randint(TabSize+20, 780-TabSize), randint(TabSize+20, 580-TabSize), 0, win))
    Obstacles.append(Obstacle(randint(TabSize+20, 780-TabSize), randint(TabSize+20, 580-TabSize), 1, win))
    Obstacles.append(Obstacle(randint(TabSize+20, 780-TabSize), randint(TabSize+20, 580-TabSize), 2, win))
    Obstacles.append(Obstacle(randint(TabSize+20, 780-TabSize), randint(TabSize+20, 580-TabSize), 2, win))  

def Filereader():
    Lines = []
    filename = fd.askopenfilename()
    f = open(filename, "r")
    for i in f:
        Lines.append(i)
    width, height = Lines[1].split(" ")
    f.close()
    return int(width), int(height), filename

def Playmode1():
    GameMode = 1
    run_button.changehandler(Run1)
    print('GameMode is now ', GameMode)
    init(win)
    play1_button.deactivate()
    play2_button.deactivate()
    play3_button.deactivate()
    reset_button.deactivate()
    CheckButtons(win)
    infolabel1 = Text(Point(WindowWidth/2, WindowHeight/2-ButtonsVerticalSpacement*0.5), "Click to place ")
    infolabel1.setFace('courier')
    infolabel1.setSize(10)
    infolabel1.draw(win)
    infolabel2 = Text(Point(WindowWidth/2, WindowHeight/2+ButtonsVerticalSpacement*0.5), "a Tree and hit Run")
    infolabel2.setFace('courier')
    infolabel2.setSize(10)
    infolabel2.draw(win)
    while True:
        click1 = win.checkMouse()
        if click1 != None:
            if IsInside(click1.getX(), click1.getY()):
                Goal.append(Tree(click1.getX(), click1.getY(), win))
                infolabel1.undraw()
                infolabel2.undraw()
                run_button.activate()
                CheckButtons(win)
                break

def Run1():
    print('-----------Run1-------------')
    run_button.deactivate()
    reset_button.deactivate()
    while True:
        CheckButtons(win)
        Clock(myrobot.Sonar(Goal).getX(), myrobot.Sonar(Goal).getY(),myrobot,win)
        if myrobot.Stop(Goal) == 1:
            myrobot.Grab(myrobot.Sonar(Goal))
            break
    while True:
        CheckButtons(win)
        Clock(myrobot.Sonar(Chargers).getX(), myrobot.Sonar(Chargers).getY(), myrobot, win)
        if myrobot.getX() - myrobot.Sonar(Chargers).getX() < 1 and myrobot.getY() - myrobot.Sonar(Chargers).getY() < 1:
            reset_button.activate()
            break
    print('-----------done-------------')
    infolabel3.draw(win)
    clicktoreset = win.getMouse()
    infolabel3.undraw()
    Reset()

def Playmode2():
    GameMode = 2
    run_button.changehandler(Run2)
    print('GameMode is now ', GameMode)
    init(win)
    play1_button.deactivate()
    play2_button.deactivate()
    play3_button.deactivate()

    Generatefield()
    
    infolabel4.draw(win)
    infolabel5.draw(win)
    
    while True:
        click = win.checkMouse()
        if click != None:
            a = True
            for i in Obstacles:
                if distance(Point(i.PosX,i.PosY), Point(click.getX(), click.getY())) < 20:
                    a = False
            if IsInside(click.getX(), click.getY()) and a:
                Goal.append(Tree(click.getX(), click.getY(), win))
                infolabel5.setText(str(len(Goal)))
                run_button.activate()
            if run_button.clicked(click):
                break
    run_button.deactivate()
    Run2()

def Run2():
    print('-----------Run2-------------')
    print(len(Obstacles), 'Obstacles')
    print(len(Goal), 'Goals')
    print(len(Path), 'Points')
    # Lucas
    for point in Path:
        point.draw(win)


    for i in Path:
        while distance(i, myrobot.Pos) > 2:
            update(30)
            Clock(i.getX(), i.getY())
        Path.remove(i)

    print('-----------done-------------')
    clicktoreset = win.getMouse()
    Reset()


def Playmode3():
    GameMode = 3
    print('GameMode is now ', GameMode)
    play2_button.deactivate()
    play1_button.deactivate()
    play3_button.deactivate()
    win2 = GraphWin("Choose", WindowWidth/2, WindowHeight/2, autoflush=False)
    button_file = Button(win2, Point(WindowWidth/4, WindowHeight*(1/6)), 2*TabSize, 2*ButtonsHeight, "Read from a file", Playmode3file)
    button_random = Button(win2, Point(WindowWidth/4, WindowHeight*(2/6)), 2*TabSize, 2*ButtonsHeight, "Random map", Playmode3random)
    Buttons.append(button_file)
    Buttons.append(button_random)
    while win2 != 0:
        CheckButtons(win2)

def Playmode3file():
    #win2.close()        tratar depois
    print('-----------Playmode3file-------------')
    Buttons.clear()
    width, height, filename = Filereader()
    global win3
    win3 = GraphWin("Mode 3", width, height, autoflush=False)
    init2(width, height, win3)
    global run_button_2
    run_button_2 = Button(win3, Point(TabSize/2, ButtonsVerticalSpacement*2), (2/3)*TabSize, ButtonsHeight, "Run", Run3file)
    #quit_button_2 = Button(win2, Point(TabSize/2, ButtonsVerticalSpacement), (2/3)*TabSize, ButtonsHeight, "Quit", Quit2)
    run_button_2.deactivate()
    Lines = []
    f = open(filename, "r")
    for i in f:
        Lines.append(i)
    for i in range(3, len(Lines)):
        Type, PosX, PosY = Lines[i].split(" ")
        Obstacles.append(Obstacle(TabSize + (float(PosX)/100)*(width-2*TabSize), (float(PosY)/100)*height, int(Type), win3))
    f.close()
    
    while True:
        click = win3.checkMouse()
        if click != None:
            a = True
            for i in Obstacles:
                if distance(Point(i.PosX,i.PosY), Point(click.getX(), click.getY())) < 20:
                    a = False
            if TabSize<click.getX()<width-TabSize and a:
                Goal.append(Tree(click.getX(), click.getY(), win3))
                run_button_2.activate()
            if run_button_2.clicked(click):
                break
    Run3file(width,height)

def Run3file(width,height):
    print('-----------Run3file-------------')
    infolabel6 = Text(Point(width/2, height/2), "Click to Quit")
    infolabel6.setFace('courier')
    infolabel6.setSize(10)
    run_button_2.deactivate()
    Findpath(Obstacles, myrobot2.getPos(), Goal[0], win3, Path)
    for point in Path:
        while distance(point, myrobot2.Pos) > 1:
            update(200)
            Clock(point.getX(), point.getY(),myrobot2,win3)
            if myrobot2.Stop(Goal) == 1:
                myrobot2.Grab(myrobot2.Sonar(Goal))
                Goal.remove(myrobot2.Sonar(Goal))
                break
    while len(Goal) > 0:
        Path.clear()
        Findpath(Obstacles, myrobot2.getPos(), myrobot2.Sonar(Goal), win3, Path)
        for point in Path:
            while distance(point, myrobot2.Pos) > 1:
                update(200)
                Clock(point.getX(), point.getY(), myrobot2,win3)
                if myrobot2.Stop(Goal) == 1:
                    myrobot2.Grab(myrobot2.Sonar(Goal))
                    Goal.remove(myrobot2.Sonar(Goal))
                    break
    
    print('-----------done-------------')
    infolabel6.draw(win3)
    clicktoclose = win3.getMouse()
    infolabel6.undraw()
    win3.close()
    
def Playmode3random():
    #win2.close()
    print('-----------Playmode3random-------------')
    width = WindowWidth
    height = WindowHeight

    global win4
    win4 = GraphWin("Mode 3", width, height, autoflush=False)
    init2(width, height, win4)
    
    for i in range(4): 
        Obstacles.append(Obstacle(TabSize + (randint(0,100)/100)*(width-2*TabSize), (randint(0,100)/100)*height, randint(0,3), win4))
    print(len(Obstacles))

    global run_button_3
    run_button_3 = Button(win4, Point(TabSize/2, ButtonsVerticalSpacement*2), (2/3)*TabSize, ButtonsHeight, "Run", Run3random)
    #quit_button_2 = Button(win2, Point(TabSize/2, ButtonsVerticalSpacement), (2/3)*TabSize, ButtonsHeight, "Quit", Quit2)
    run_button_3.deactivate()
    
    while True:
        click = win4.checkMouse()
        if click != None:
            a = True
            for i in Obstacles:
                if distance(Point(i.PosX,i.PosY), Point(click.getX(), click.getY())) < 20:
                    a = False
            if TabSize<click.getX()<width-TabSize and a:
                Goal.append(Tree(click.getX(), click.getY(), win4))
                run_button_3.activate()
            if run_button_3.clicked(click):
                break
    Run3random(width,height)
    
def Run3random(width,height):
    print('-----------Run3random-------------')
    infolabel7 = Text(Point(width/2, height/2), "Click to Quit")
    infolabel7.setFace('courier')
    infolabel7.setSize(10)
    
    run_button_3.deactivate()
    Findpath(Obstacles, myrobot2.getPos(), Goal[0], win4, Path)
    for point in Path:
        while distance(point, myrobot2.Pos) > 1:
            update(200)
            Clock(point.getX(), point.getY(),myrobot2,win4)
            if myrobot2.Stop(Goal) == 1:
                myrobot2.Grab(myrobot2.Sonar(Goal))
                Goal.remove(myrobot2.Sonar(Goal))
                break
    while len(Goal) > 0:
        Path.clear()
        Findpath(Obstacles, myrobot2.getPos(), myrobot2.Sonar(Goal), win4, Path)
        for point in Path:
            while distance(point, myrobot2.Pos) > 1:
                update(200)
                Clock(point.getX(), point.getY(), myrobot2,win4)
                if myrobot2.Stop(Goal) == 1:
                    myrobot2.Grab(myrobot2.Sonar(Goal))
                    Goal.remove(myrobot2.Sonar(Goal))
                    break
    
    print('-----------done-------------')
    infolabel7.draw(win4)
    clicktoclose = win4.getMouse()
    infolabel7.undraw()
    win4.close()
      
def init2(w, h, win):
    
    b = (50/WindowWidth) #ratio for ButtonsVerticalSpacement

    LeftTab = Rectangle(Point(0, w), Point(TabSize, 0))
    RightTab = Rectangle(Point(w - TabSize, h), Point(w, 0))
    LeftTab.setFill("light grey")
    RightTab.setFill("light grey")
    
    LeftTab.draw(win)
    RightTab.draw(win)
    
    rec6 = Rectangle(Point(w-TabSize/2-15, ButtonsVerticalSpacement-5), Point(w-TabSize/2+14, ButtonsVerticalSpacement-6))
    rec7 = Rectangle(Point(w-TabSize/2-15, ButtonsVerticalSpacement+6), Point(w-TabSize/2+14, ButtonsVerticalSpacement+5))
    rec8 = Rectangle(Point(w-TabSize/2-15, ButtonsVerticalSpacement+6), Point(w-TabSize/2-14, ButtonsVerticalSpacement-6))
    rec9 = Rectangle(Point(w-TabSize/2+14, ButtonsVerticalSpacement+6), Point(w-TabSize/2+13, ButtonsVerticalSpacement-6))
    rec10 = Rectangle(Point(w-TabSize/2+17, ButtonsVerticalSpacement+5), Point(w-TabSize/2+16, ButtonsVerticalSpacement-5))
    
    rec6.draw(win)
    rec7.draw(win)
    rec8.draw(win)
    rec9.draw(win)
    rec10.draw(win)
    
    global bar1
    bar1 = Rectangle(Point(w-TabSize/2-12,ButtonsVerticalSpacement+4),Point(w-TabSize/2-7,ButtonsVerticalSpacement-3))
    bar1.setFill('green3')
    bar1.setWidth(0)
    bar1.draw(win)
    
    global bar2
    bar2 = Rectangle(Point(w-TabSize/2-6,ButtonsVerticalSpacement+4),Point(w-TabSize/2-1,ButtonsVerticalSpacement-3))
    bar2.setFill('green3')
    bar2.setWidth(0)
    bar2.draw(win)
    
    global bar3
    bar3 = Rectangle(Point(w-TabSize/2,ButtonsVerticalSpacement+4),Point(w-TabSize/2+5,ButtonsVerticalSpacement-3))
    bar3.setFill('green3')
    bar3.setWidth(0)
    bar3.draw(win)
    
    global bar4
    bar4 = Rectangle(Point(w-TabSize/2+6,ButtonsVerticalSpacement+4),Point(w-TabSize/2+11,ButtonsVerticalSpacement-3))
    bar4.setFill('green3')
    bar4.setWidth(0)
    bar4.draw(win)
    
    global Dock
    Dock = Circle(Point(w/2,h), 50)
    Dock.setFill("light grey")
    Dock.draw(win)
    
    bars.append(bar1)
    bars.append(bar2)
    bars.append(bar3)
    bars.append(bar4)
    
    RightCharger = Charger(w - TabSize - 20, 20, win, 1, 1)
    LeftCharger = Charger(TabSize + 20, 20, win, 1, 1)
    Chargers.append(RightCharger)
    Chargers.append(LeftCharger)
    
    global batteryinfo
    batteryinfo = Text(Point(w - TabSize/2, 100), '100 %')
    batteryinfo.setFace('courier')
    batteryinfo.setSize(10)
    batteryinfo.draw(win)
    
    global batterylabel
    batterylabel = Text(Point(w - TabSize/2, 80), 'Battery')
    batterylabel.setFace('courier')
    batterylabel.setSize(10)
    batterylabel.draw(win)
    
    global myrobot2
    myrobot2 = Harve(w/2, h, 100, 1, win, Chargers)
    
def init(win):
    rec1.draw(win)
    rec2.draw(win)
    rec3.draw(win)
    rec4.draw(win)
    rec5.draw(win)
    
    global bar1
    bar1 = Rectangle(Point(WindowWidth-TabSize/2-12,ButtonsVerticalSpacement+4),Point(WindowWidth-TabSize/2-7,ButtonsVerticalSpacement-3))
    bar1.setFill('green3')
    bar1.setWidth(0)
    bar1.draw(win)
    
    global bar2
    bar2 = Rectangle(Point(WindowWidth-TabSize/2-6,ButtonsVerticalSpacement+4),Point(WindowWidth-TabSize/2-1,ButtonsVerticalSpacement-3))
    bar2.setFill('green3')
    bar2.setWidth(0)
    bar2.draw(win)
    
    global bar3
    bar3 = Rectangle(Point(WindowWidth-TabSize/2,ButtonsVerticalSpacement+4),Point(WindowWidth-TabSize/2+5,ButtonsVerticalSpacement-3))
    bar3.setFill('green3')
    bar3.setWidth(0)
    bar3.draw(win)
    
    global bar4
    bar4 = Rectangle(Point(WindowWidth-TabSize/2+6,ButtonsVerticalSpacement+4),Point(WindowWidth-TabSize/2+11,ButtonsVerticalSpacement-3))
    bar4.setFill('green3')
    bar4.setWidth(0)
    bar4.draw(win)
    
    global Dock
    Dock = Circle(Point(WindowWidth/2,WindowHeight), 50)
    Dock.setFill("light grey")
    Dock.draw(win)
    
    bars.append(bar1)
    bars.append(bar2)
    bars.append(bar3)
    bars.append(bar4)
    
    RightCharger = Charger(WindowWidth - TabSize - 20, 20, win, 1, 1)
    LeftCharger = Charger(TabSize + 20, 20, win, 1, 1)
    Chargers.append(RightCharger)
    Chargers.append(LeftCharger)
    
    global batteryinfo
    batteryinfo = Text(Point(WindowWidth - TabSize/2, 100), '100 %')
    batteryinfo.setFace('courier')
    batteryinfo.setSize(10)
    batteryinfo.draw(win)
    
    global batterylabel
    batterylabel = Text(Point(WindowWidth - TabSize/2, 80), 'Battery')
    batterylabel.setFace('courier')
    batterylabel.setSize(10)
    batterylabel.draw(win)
    
    global myrobot
    myrobot = Harve(WindowWidth/2, WindowHeight, 100, 1, win, Chargers)
 
def Reset():
    '''
    if type(win2) != "Point":
        win2.close()
    if type(win2) != "Point":
        win3.close()'''
        
    reset_button.deactivate()
    play1_button.activate()
    play2_button.activate()
    play3_button.activate()
    run_button.deactivate()
    rec1.undraw()
    rec2.undraw()
    rec3.undraw()
    rec4.undraw()
    rec5.undraw()
    batteryinfo.undraw()
    batterylabel.undraw()
    infolabel4.undraw()
    infolabel5.undraw()
    Dock.undraw()
    myrobot.undraw()
    myrobot.delete()
    for i in Path:
        i.undraw()
    Path.clear()
    for i in bars:
        i.undraw()
    bars.clear()
    for i in Chargers:
        i.undraw()
        i.delete()
    Chargers.clear()
    for i in Obstacles:
        i.undraw()
        i.delete()
    Obstacles.clear()
    for i in Goal:
        i.undraw()
        i.delete()
    Goal.clear()

def Clock(obsX, obsY, myrobot, win):       #Harve module after this
    for i in bars:
        i.undraw()
    if myrobot.Batterylevel == 4:
        for i in bars:
            i.setFill('green3')
            i.draw(win)
    elif myrobot.Batterylevel == 3:
        for i in bars:
            i.setFill('yellow')
        bar1.draw(win)
        bar2.draw(win)
        bar3.draw(win)
    elif myrobot.Batterylevel == 2:
        for i in bars:
            i.setFill('dark orange')
        bar1.draw(win)
        bar2.draw(win)
    else:
        for i in bars:
            i.setFill('red')
        bar1.draw(win)
        
    myrobot.Charge()
    batteryinfo.setText(str(myrobot.getBattery()) +' %')
    
    time.sleep(0.01)
    myrobot.Seek(obsX, obsY)

if __name__ == "__main__":  
    main()