import numpy as np
import pandas as pd

def GetPlayerDetails(PlayerName, Players_Info):
    Player_Row = Players_Info[Players_Info['second_name'].str.match(PlayerName)]
    if Player_Row.empty:
        print("The inserted Player does not exist: Make sure only the first letter is capital")
        return 0
    else:
        return Player_Row

def SelectReplacement(PlayerRow, MoneyAvailable, Goalies_Scores
                     , Defenders_Scores, Midfielders_Scores, Strikers_Scores):

    PlayerPosition = PlayerRow['element_type'].values[0]
    PlayerCost = PlayerRow['now_cost'].values[0]
    MoneyToSpend = PlayerCost + (MoneyAvailable * 10)

    Goalie_Selection_Index = 0
    Def_Selection_Index = 0
    Mid_Selection_Index = 0
    Str_Selection_Index = 0

    if PlayerPosition == 1:
        Num_Of_Goalie_Options = len(Goalies_Scores.index)
        Finding_Selection = True
        while Finding_Selection:
            Possible_Selection_Name = Goalies_Scores['second_name'].values[Goalie_Selection_Index]
            Possible_Selection_Cost = Goalies_Scores['now_cost'].values[Goalie_Selection_Index]  
            if Possible_Selection_Cost > MoneyToSpend:
                Goalie_Selection_Index = Goalie_Selection_Index + 1
                if Goalie_Selection_Index == Num_Of_Goalie_Options:
                    Finding_Selection = False
                    return "Cant Afford Goalie"
            else:    
                Finding_Selection = False
                return Possible_Selection_Name


    elif PlayerPosition == 2:
        Num_Of_Defender_Options = len(Defenders_Scores.index)
        Finding_Selection = True
        while Finding_Selection:
            Possible_Selection_Name = Defenders_Scores['second_name'].values[Def_Selection_Index]
            Possible_Selection_Cost = Defenders_Scores['now_cost'].values[Def_Selection_Index]  
            if Possible_Selection_Cost > MoneyToSpend:
                Def_Selection_Index = Def_Selection_Index + 1
                if Def_Selection_Index == Num_Of_Defender_Options:
                    Finding_Selection = False
                    return "Cant Afford Defender"
            else:    
                Finding_Selection = False
                return Possible_Selection_Name

    elif PlayerPosition == 3:
        Num_Of_Midfielder_Options = len(Midfielders_Scores.index)
        Finding_Selection = True
        while Finding_Selection:
            Possible_Selection_Name = Midfielders_Scores['second_name'].values[Mid_Selection_Index]
            Possible_Selection_Cost = Midfielders_Scores['now_cost'].values[Mid_Selection_Index]  
            if Possible_Selection_Cost > MoneyToSpend:
                Mid_Selection_Index = Mid_Selection_Index + 1
                if Mid_Selection_Index == Num_Of_Midfielder_Options:
                    Finding_Selection = False
                    return "Cant Afford Midfielder"
            else:    
                Finding_Selection = False
                return Possible_Selection_Name

    elif PlayerPosition == 4:
        Num_Of_Striker_Options = len(Strikers_Scores.index)
        Finding_Selection = True
        while Finding_Selection:
            Possible_Selection_Name = Strikers_Scores['second_name'].values[Str_Selection_Index]
            Possible_Selection_Cost = Strikers_Scores['now_cost'].values[Str_Selection_Index]  
            if Possible_Selection_Cost > MoneyToSpend:
                Str_Selection_Index = Str_Selection_Index + 1
                if Str_Selection_Index == Num_Of_Striker_Options:
                    Finding_Selection = False
                    return "Cant Afford Striker"
            else:    
                Finding_Selection = False
                return Possible_Selection_Name
        
    else:
        print("Problem with Player row")
        return 0







