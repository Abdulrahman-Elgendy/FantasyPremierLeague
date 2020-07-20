import pandas as pd
import tkinter as tk
import sys
import threading
import pdb
from FPLDataLoader import Load_JSON_Data_From_URL
from FPLDataLoader import ParseMainAPI
from FPLTeamsAnalysis import Team_Analysis_Results
from PlayerRatingGenerator import Split_Based_On_Categories
from PlayerRatingGenerator import Calculate_Players_Scores_Regular
from PlayerRatingGenerator import Calculate_Players_Scores_Superstars
from FPLDataVisualization import drawPitch
from FPLDataVisualization import Draw_Four_Four_Two
from FPLDataVisualization import Draw_Three_Four_Three
from FPLDataVisualization import Draw_Three_Five_Two
from ChoosePlayerReplacement import SelectReplacement
from ChoosePlayerReplacement import GetPlayerDetails
from LinearOptimizationTeamSelection import Team_Selection_Linear_Optimization
from tkinter import ttk
import time


class GUI_FPL():
    def __init__(self,MasterWindow):
        self.Master = MasterWindow
        self.Master.title("Fantasy Premier League")
        self.Master.geometry('600x600')

        #Create notebook that will have multiple tabs
        self.My_Notebook = ttk.Notebook(self.Master, width=600, height=600)
        self.My_Notebook.pack(pady=15)

        #Create the frames that will make up each tab and add them to the notebook
        self.Frame1 = tk.Frame(self.My_Notebook, width=600, height=600)
        self.Frame2 = tk.Frame(self.My_Notebook, width=600, height=600)
        self.Frame1.pack(fill="both", expand=1)
        self.Frame2.pack(fill="both", expand=1)
        self.My_Notebook.add(self.Frame1, text="Select Team of 15")
        self.My_Notebook.add(self.Frame2, text="Select Player Replacement")
        self.My_Notebook.pack()

        #add the Widgets that will go on each frame
        #Widgets for "Select Team of fifteen" frame: /////////////////////////////////////////////////////////////////////
        Label1 = tk.Label(self.Frame1, text="Weights", font=("arial", 11, "bold"), pady=15)
        Label1.pack()

        Label2 = tk.Label(self.Frame1, text="Note: Make sure all your weights sum up to one")
        Label2.pack()

        tk.Label(self.Frame1, text="form: ", font=("arial", 10, "bold")).place(x=10, y=100)
        tk.Label(self.Frame1, text="ROI: ", font=("arial", 10, "bold")).place(x=10, y=135)
        tk.Label(self.Frame1, text="PtsPerGame: ", font=("arial", 10, "bold")).place(x=10, y=170)
        tk.Label(self.Frame1, text="ICT Index: ", font=("arial", 10, "bold")).place(x=270, y=100)
        tk.Label(self.Frame1, text="expected point next round: ", font=("arial", 10, "bold")).place(x=270, y=135)
        tk.Label(self.Frame1, text="Future three games analysis: ", font=("arial", 10, "bold")).place(x=270, y=170)

        self.Form_Weight = tk.Entry(self.Frame1, width=10)
        self.Form_Weight.place(x=150, y=100)
        self.ROI_Weight = tk.Entry(self.Frame1,width=10)
        self.ROI_Weight.place(x=150, y=135)
        self.PtsPerGame_Weight = tk.Entry(self.Frame1, width=10)
        self.PtsPerGame_Weight.place(x=150, y=170)
        self.ICTIndex_Weight = tk.Entry(self.Frame1, width=10)
        self.ICTIndex_Weight.place(x=500, y=100)
        self.EpNext_Weight = tk.Entry(self.Frame1, width=10)
        self.EpNext_Weight.place(x=500, y=135)
        self.FutureGames_Weight = tk.Entry(self.Frame1, width=10)
        self.FutureGames_Weight.place(x=500, y=170)

        Label7 = tk.Label(self.Frame1, text="Formation Selection", font=("arial", 11, "bold"), pady=0)
        Label7.place(x=220, y=220)

        Label8 = tk.Label(self.Frame1, text="Note: This is only for illustration purposes. It does not affect the algorithms selection")
        Label8.place(x=80, y=250)

        self.Formation_Number = tk.IntVar()
        Formation1 = tk.Radiobutton(self.Frame1, text="3-4-3", value=1, variable=self.Formation_Number)
        Formation2 = tk.Radiobutton(self.Frame1, text="3-5-2", value=2, variable=self.Formation_Number)
        Formation3 = tk.Radiobutton(self.Frame1, text="4-4-2", value=3, variable=self.Formation_Number)
        Formation1.place(x=100, y=290)
        Formation2.place(x=250, y=290)
        Formation3.place(x=400, y=290)

        #Exit buttons for the frames
        ExitButton1 = tk.Button(self.Frame1, text="Exit", command=self.quit)
        ExitButton1.pack(side=tk.BOTTOM)

        #Select Team button
        self.Select_Team_Button = tk.Button(self.Frame1, text='Select Team of 15', width=20, height=3, command=self.Select_Team_Button_Clicked)
        self.Select_Team_Button.pack(side=tk.BOTTOM)
        self.Status_Label = tk.Label(self.Frame1, text="Algorithm is currently selecting your team, this process takes about 2 minutes")

        #Widgets for "Select Player Replacement" frame: ///////////////////////////////////////////////////////////////////////////////
        Label3 = tk.Label(self.Frame2, text="Player Details", font=("arial", 11, "bold"), pady=25)
        Label3.pack()

        tk.Label(self.Frame2, text="Player Name: ", font=("arial", 10, "bold")).place(x=10, y=70)
        self.Player_Name = tk.Entry(self.Frame2, width=20)
        self.Player_Name.place(x=120, y=70)

        tk.Label(self.Frame2, text="Purchase Price: ", font=("arial", 10, "bold")).place(x=300, y=70)
        self.Purchase_Price = tk.Entry(self.Frame2, width=10)
        self.Purchase_Price.place(x=425, y=70)

        Label4 = tk.Label(self.Frame2, text="Weights", font=("arial", 11, "bold"), pady=0)
        Label4.pack(pady=50)

        Label5 = tk.Label(self.Frame2, text="Note: Make sure all your weights sum up to one")
        Label5.place(x=170, y=150)
        
        tk.Label(self.Frame2, text="form: ", font=("arial", 10, "bold")).place(x=10, y=200)
        tk.Label(self.Frame2, text="ROI: ", font=("arial", 10, "bold")).place(x=10, y=235)
        tk.Label(self.Frame2, text="PtsPerGame: ", font=("arial", 10, "bold")).place(x=10, y=270)
        tk.Label(self.Frame2, text="ICT Index: ", font=("arial", 10, "bold")).place(x=270, y=200)
        tk.Label(self.Frame2, text="expected point next round: ", font=("arial", 10, "bold")).place(x=270, y=235)
        tk.Label(self.Frame2, text="Future three games analysis: ", font=("arial", 10, "bold")).place(x=270, y=270)

        self.Form_Weight2 = tk.Entry(self.Frame2, width=10)
        self.Form_Weight2.place(x=150, y=200)
        self.ROI_Weight2 = tk.Entry(self.Frame2,width=10)
        self.ROI_Weight2.place(x=150, y=235)
        self.PtsPerGame_Weight2 = tk.Entry(self.Frame2, width=10)
        self.PtsPerGame_Weight2.place(x=150, y=270)
        self.ICTIndex_Weight2 = tk.Entry(self.Frame2, width=10)
        self.ICTIndex_Weight2.place(x=500, y=200)
        self.EpNext_Weight2 = tk.Entry(self.Frame2, width=10)
        self.EpNext_Weight2.place(x=500, y=235)
        self.FutureGames_Weight2 = tk.Entry(self.Frame2, width=10)
        self.FutureGames_Weight2.place(x=500, y=270)

        Label6 = tk.Label(self.Frame2, text="Budget", font=("arial", 11, "bold"), pady=0)
        Label6.place(x=270, y=320)

        tk.Label(self.Frame2, text="Extra Money Available: ", font=("arial", 10, "bold")).place(x=10, y=370)
        self.Purchase_Price = tk.Entry(self.Frame2, width=10)
        self.Purchase_Price.place(x=200, y=370)

        #Exit buttons for the frames
        ExitButton2 = tk.Button(self.Frame2, text="Exit", command=self.quit)
        ExitButton2.pack(side=tk.BOTTOM)

        #Select Team button
        self.Select_Replacement_Button = tk.Button(self.Frame2, text='Select Player Replacement', width=20, height=3, command=self.Select_Player_Replacement_Clicked)
        self.Select_Replacement_Button.pack(side=tk.BOTTOM)
        self.Status_Label2 = tk.Label(self.Frame2, text="Algorithm is currently looking for a potential replacement, this process takes about 2 minutes")
     

    def quit(self):
        sys.exit()

    def Algorithm_Team_Selection(self):
        FPL_API_Url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
        JSON_Data = Load_JSON_Data_From_URL(FPL_API_Url)
        players, teams, events = ParseMainAPI(JSON_Data)

        #form, ROI, ptsPerGame, ICT index, ep_next, Future Games Score
        Regular_Scoring_Weights = [float(self.Form_Weight.get()), float(self.ROI_Weight.get())
                                   ,float(self.PtsPerGame_Weight.get()), float(self.ICTIndex_Weight.get())
                                   ,float(self.EpNext_Weight.get()), float(self.FutureGames_Weight.get())] 

        Players_Scores = Calculate_Players_Scores_Regular(players, Regular_Scoring_Weights)

        ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left = Team_Selection_Linear_Optimization(Players_Scores)

        Draw_Three_Four_Three(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)

    
    def Select_Team_Button_Clicked(self):

        self.Select_Team_Button['state'] = tk.DISABLED
        self.Select_Team_Button.update()

        self.Select_Replacement_Button['state'] = tk.DISABLED
        self.Select_Replacement_Button.update()

        self.Status_Label.pack(side=tk.BOTTOM)
        self.Frame1.update()

        time.sleep(6)

        print("The weight are", self.Form_Weight.get(), self.ROI_Weight.get()
              ,self.PtsPerGame_Weight.get(), self.ICTIndex_Weight.get()
              ,self.EpNext_Weight.get(), self.FutureGames_Weight.get())

        print("Formation selected is: ", self.Formation_Number.get())    
        
        #threading.Thread(target=self.Algorithm_Team_Selection).start()

        self.Status_Label.forget()
        self.Frame1.update()

        self.Select_Team_Button['state'] = tk.NORMAL
        self.Select_Team_Button.update()

        self.Select_Replacement_Button['state'] = tk.NORMAL
        self.Select_Replacement_Button.update()

    def Select_Player_Replacement_Clicked(self):

        self.Select_Replacement_Button['state'] = tk.DISABLED
        self.Select_Replacement_Button.update()

        self.Select_Team_Button['state'] = tk.DISABLED
        self.Select_Team_Button.update()

        self.Status_Label2.pack(side=tk.BOTTOM)
        self.Frame2.update()

        time.sleep(6)

        print("The weight are", self.Form_Weight2.get(), self.ROI_Weight2.get()
              ,self.PtsPerGame_Weight2.get(), self.ICTIndex_Weight2.get()
              ,self.EpNext_Weight2.get(), self.FutureGames_Weight2.get())
        
        #threading.Thread(target=self.Algorithm_Team_Selection).start()

        self.Status_Label2.forget()
        self.Frame2.update()

        self.Select_Replacement_Button['state'] = tk.NORMAL
        self.Select_Replacement_Button.update()

        self.Select_Team_Button['state'] = tk.NORMAL
        self.Select_Team_Button.update()




masterWindow = tk.Tk()
GUI_FPL(masterWindow)
tk.mainloop()
#Algo_Options = ["Select Player Replacement","Select Team of 15"]
#Defaultvariable = tk.StringVar(masterWindow)
#Defaultvariable.set(Algo_Options[0]) # default value

#w = tk.OptionMenu(masterWindow, Defaultvariable, Algo_Options)
#w.pack()










