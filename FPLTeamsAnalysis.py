import numpy as np
import pandas as pd
import os
import matplotlib

Num_Of_PremTeams = 20

def Get_TotalPts_For_All_Teams(Players_Info):
    #This returns a Series containing the total points accumulated by players at a club
    Player_Names_And_TotPoints = Players_Info[['second_name','total_points']]
    #Only list the players that belong to one club before summing the column
    
    TotPts_Per_Team_List= []
    for i in range(1,Num_Of_PremTeams + 1):
        Selected_Team_Players = Player_Names_And_TotPoints[Players_Info['team'] == i]
        TotalPts_For_Selected_Team = Selected_Team_Players['total_points'].sum()
        TotPts_Per_Team_List.append(TotalPts_For_Selected_Team)

    return pd.Series(TotPts_Per_Team_List)

def Get_TotalCost_For_All_Teams(Players_Info):
    #This returns a Series containing the total cost of players at a club (FPL costs)
    Player_Names_And_Costs = Players_Info[['second_name','now_cost']]
    
    TotCosts_Per_Team_List= []
    for i in range(1,Num_Of_PremTeams + 1):
        #Only list the players that belong to one club before summing the column
        Selected_Team_Players = Player_Names_And_Costs[Players_Info['team'] == i]
        TotalCosts_For_Selected_Team = Selected_Team_Players['now_cost'].sum()
        TotalCosts_For_Selected_Team = float(TotalCosts_For_Selected_Team) / 10
        TotCosts_Per_Team_List.append(TotalCosts_For_Selected_Team)

    return pd.Series(TotCosts_Per_Team_List)

def Get_NumOf_Players(Players_Info):
    #This returns a series that shows the number of players per team that played more than 9 games)

    Player_Names_And_Minutes = Players_Info[['second_name','minutes']]

    Num_Of_Players = []
    for i in range(1,Num_Of_PremTeams + 1):
        #Only list the players that belong to one club before summing the column
        Selected_Team_Players = Player_Names_And_Minutes[Players_Info['team'] == i]
        Filtered_Team_Players = Selected_Team_Players[Selected_Team_Players['minutes'] > 810]
        index = Filtered_Team_Players.index
        Num_Of_Rows = len(index)
        Num_Of_Players.append(Num_Of_Rows)

    return pd.Series(Num_Of_Players)    

def Get_Teams_ROI(TotalCosts, TotalPts):
    Teams_ROI = TotalPts/TotalCosts
    return Teams_ROI

def Get_ROI_Over_NumOfPlayers(Teams_ROI, Num_Of_Players):
    #This calculation divides the ROI by the number of players that played more than 9 games (810 minutes) this season
    #We want a high ROI/NumOfPlayers as this can mean 2 things:
    #1) That the manager selects the same lineup every week and barely makes any changes, and these selected players have high returns
    #2) That the manager has a frequent squad rotation but all the players still have heavy returns, or 1 player has exceptional returns
    return Teams_ROI/Num_Of_Players


def Team_Analysis_Results(Players_Info, TeamInfo):
    #Get ANalysis Information
    Team_Names = TeamInfo['name']
    Total_Costs = Get_TotalCost_For_All_Teams(Players_Info)
    Total_Pts = Get_TotalPts_For_All_Teams(Players_Info)
    Teams_ROI = Get_Teams_ROI(Total_Costs, Total_Pts)
    Num_Of_Players = Get_NumOf_Players(Players_Info)
    ROI_Over_NumPlys = Get_ROI_Over_NumOfPlayers(Teams_ROI,Num_Of_Players)

    #Combine the Serieses into a dataFrame
    Analysis_Df = pd.concat([Team_Names,Total_Costs,Total_Pts,Teams_ROI, Num_Of_Players, ROI_Over_NumPlys], axis = 1)
    Analysis_Df.rename(columns={0:'Tot Costs',1:'Tot Pts',2:'Teams ROI',3:'Num Of Players', 4:'ROI/NumofPlys'}, inplace=True)
    Analysis_Df.sort_values(by='Tot Costs', inplace = True, ascending=False)
    return Analysis_Df