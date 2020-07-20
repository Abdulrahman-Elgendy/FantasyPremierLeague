import numpy as np
import pandas as pd
import os
import matplotlib.pyplot as plt
import turtle

def drawPitch():
    GREEN="#149118"
    screen = turtle.Screen()
    screen.tracer(0)
    screen.bgcolor(GREEN)
  
    myBrush = turtle.Turtle()
    myBrush.width(1)
    myBrush.hideturtle()
  
    myBrush.speed(0)
    myBrush.color("#FFFFFF")
  
    #Outer lines
    myBrush.penup()
    myBrush.goto(-250,280)
    myBrush.pendown()
    myBrush.goto(250,280)
    myBrush.goto(250,-220)
    myBrush.goto(-250,-220)
    myBrush.goto(-250,280)
  
    #Penalty Box - Top
    myBrush.penup()
    myBrush.goto(0,190)
    myBrush.pendown()
    myBrush.circle(40)
    myBrush.penup()
    myBrush.goto(-100,280)
    myBrush.pendown()
    myBrush.fillcolor(GREEN)
    myBrush.begin_fill()
    myBrush.goto(100,280)
    myBrush.goto(100,215)
    myBrush.goto(-100,215)
    myBrush.goto(-100,280)  
    myBrush.end_fill()
 
    #Penalty Box - Bottom 
    myBrush.penup()
    myBrush.goto(0,-210)
    myBrush.pendown()
    myBrush.circle(40)
    myBrush.penup()
    myBrush.goto(-100,-220)
    myBrush.pendown()
    myBrush.fillcolor(GREEN)
    myBrush.begin_fill()
    myBrush.goto(100,-220)
    myBrush.goto(100,-155)
    myBrush.goto(-100,-155)
    myBrush.goto(-100,-220)  
    myBrush.end_fill()

    # Goal Box - Bottom
    myBrush.penup()
    myBrush.goto(40,-220)
    myBrush.pendown()
    myBrush.goto(40,-195)
    myBrush.goto(-40,-195)
    myBrush.goto(-40,-220)  

    # Goal Box - Top
    myBrush.penup()
    myBrush.goto(40,280)
    myBrush.pendown()
    myBrush.goto(40,255)
    myBrush.goto(-40,255)
    myBrush.goto(-40,280)     
  
    #Halfway Line
    myBrush.penup()
    myBrush.goto(-250,30)
    myBrush.pendown()
    myBrush.goto(250,30)
  
    #Central Circle
    myBrush.penup()
    myBrush.goto(0,-10)
    myBrush.pendown()
    myBrush.circle(40)
  
    screen.tracer(1)  




    #A Procedure to draw a player at the given position
def drawPlayer(color,x,y,label):
    screen = turtle.Screen()
    screen.tracer(0)
    myPen = turtle.Turtle()
    myPen.hideturtle()
    myPen.penup()
    myPen.goto(x,y)
    myPen.fillcolor(color)
    myPen.begin_fill()
    myPen.circle(10)
    myPen.end_fill()
    screen.tracer(1)  
    myPen.penup()
    x_offset = (len(label)/2) * 5
    myPen.goto(x-x_offset,y-20)
    myPen.write(label[4:])

def Draw_Bench(Formation, ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left):

    if Formation == 343:
        #Will have 2 defenders, 1 midfielder, 1 goalie on bench
        drawPlayer("red",-260,-270,ListOfGoalies[1]) 

        drawPlayer("red",-140,-270,ListOfDef[3]) 
        drawPlayer("red",-20,-270,ListOfDef[4]) 

        drawPlayer("red",100,-270, ListOfMid[4]) 
        
        #Add Cash Remaining:
        CashLeft = "Cash Remaining: " + str(Cash_Left)
        drawPlayer("white",300,-270,CashLeft)

    elif Formation == 442:
        #Will have 1 defenders, 1 midfielder, 1 striker, 1 goalie on bench
        drawPlayer("red",-260,-270,ListOfGoalies[1]) 

        drawPlayer("red",-140,-270,ListOfDef[4]) 

        drawPlayer("red",-20,-270,ListOfMid[4]) 
                
        drawPlayer("red",100,-270,ListOfStr[2]) 
        
        #Add Cash Remaining:
        CashLeft = "Cash Remaining: " + str(Cash_Left)
        drawPlayer("white",300,-270,CashLeft)

    elif Formation == 352:
        #Will have 2 defenders 1 striker, 1 goalie on bench
        drawPlayer("red",-260,-270,ListOfGoalies[1]) 

        drawPlayer("red",-140,-270,ListOfDef[3]) 

        drawPlayer("red",-20,-270,ListOfDef[4]) 
                
        drawPlayer("red",100,-270,ListOfStr[2]) 

        #Add Cash Remaining:
        CashLeft = "Cash Remaining: " + str(Cash_Left)
        drawPlayer("white",300,-270,CashLeft)
        
    else:
        print("Formation not programmed yet")



def Draw_Four_Four_Two(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left):

    #Draw Pitch
    drawPitch()

    #Draw Gk
    drawPlayer("blue",-0,-190,ListOfGoalies[0]) 

    #Draw 4 defenders
    drawPlayer("yellow",175,-120,ListOfDef[0]) 
    drawPlayer("yellow",-60,-120,ListOfDef[1]) 
    drawPlayer("yellow",60,-120,ListOfDef[2]) 
    drawPlayer("yellow",-175,-120,ListOfDef[3]) 

    #Draw 4 Midfielders
    drawPlayer("yellow",225,20,ListOfMid[0]) 
    drawPlayer("yellow",-75,20,ListOfMid[1]) 
    drawPlayer("yellow",75,20,ListOfMid[2]) 
    drawPlayer("yellow",-225,20,ListOfMid[3]) 

    #Draw 2 Strikers
    drawPlayer("yellow",-60,150,ListOfStr[0]) 
    drawPlayer("yellow",60,150,ListOfStr[1]) 

    Draw_Bench(442,ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    turtle.mainloop()


def Draw_Three_Four_Three(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left):
    
    #Draw Pitch
    drawPitch()

    #Draw Gk
    drawPlayer("blue",-0,-190,ListOfGoalies[0]) 

    #Draw 3 defenders
    drawPlayer("yellow",-150,-130, ListOfDef[0]) 
    drawPlayer("yellow",0,-130, ListOfDef[1]) 
    drawPlayer("yellow",150,-130, ListOfDef[2]) 

    #Draw 4 Midfielders
    drawPlayer("yellow",225,20,ListOfMid[0]) 
    drawPlayer("yellow",-75,20,ListOfMid[1]) 
    drawPlayer("yellow",75,20,ListOfMid[2]) 
    drawPlayer("yellow",-225,20,ListOfMid[3]) 

    #Draw 3 Strikers
    drawPlayer("yellow",-150,150,ListOfStr[0]) 
    drawPlayer("yellow",0,150,ListOfStr[1]) 
    drawPlayer("yellow",150,150,ListOfStr[2]) 

    Draw_Bench(343, ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    turtle.mainloop()


def Draw_Three_Five_Two(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left):
   
    #Draw Pitch
    drawPitch()

    #Draw Gk
    drawPlayer("blue",-0,-190,ListOfGoalies[0]) 

    #Draw 3 defenders
    drawPlayer("yellow",-150,-130,ListOfDef[0]) 
    drawPlayer("yellow",0,-130,ListOfDef[1]) 
    drawPlayer("yellow",150,-130,ListOfDef[2]) 

    #Draw 5 Midfielders
    drawPlayer("yellow",220,20,ListOfMid[0]) 
    drawPlayer("yellow",110,20,ListOfMid[1]) 
    drawPlayer("yellow",0,20,ListOfMid[2]) 
    drawPlayer("yellow",-110,20,ListOfMid[3]) 
    drawPlayer("yellow",-220,20,ListOfMid[4]) 

    #Draw 2 Strikers
    drawPlayer("yellow",-75,150,ListOfStr[0]) 
    drawPlayer("yellow",75,150,ListOfStr[1])  

    Draw_Bench(352, ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
    turtle.mainloop()



