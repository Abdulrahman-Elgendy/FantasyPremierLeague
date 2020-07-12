"""
import numpy as np
import pandas as pd
from PlayerRatingGenerator import Split_Categories

Starting_Money = 1000

def Select_Super_Star_Players(Goalies_SuperstarList, Defenders_SuperstarList, Midfielders_SuperstarList, Strikers_SuperstarList):

    Selected_Superstars = []
    Total_SuperStars_Cost = (Goalies_SuperstarList['now_cost'].values[0] 
                            + Defenders_SuperstarList['now_cost'].values[0]
                            + Midfielders_SuperstarList['now_cost'].values[0]
                            + Strikers_SuperstarList['now_cost'].values[0])

    Selected_Superstars.append(Goalies_SuperstarList[['second_name','element_type']].values[0])
    Selected_Superstars.append(Defenders_SuperstarList[['second_name','element_type']].values[0])
    Selected_Superstars.append(Midfielders_SuperstarList[['second_name','element_type']].values[0])
    Selected_Superstars.append(Strikers_SuperstarList[['second_name','element_type']].values[0])

    SuperStars_Info_Final = pd.DataFrame(Selected_Superstars)
    SuperStars_Info_Final.rename(columns={0:'second_name',1:'element_type'}, inplace=True)

    Remaining_Money = Starting_Money - Total_SuperStars_Cost

    return SuperStars_Info_Final , Remaining_Money

def Select_Remaining_Players(Selected_Superstars,Goalies_Scores, Defenders_Scores,
                               Midfielders_Scores, Strikers_Scores, Remaining_Money):

    #Need 4 more Defenders, 4 more midfielders, 1 goalie, 2 strikers
    Num_Of_Remaining_Players = 11
    Num_Of_Remaining_Goalies = 1
    Num_Of_Remaining_Defenders = 4
    Num_Of_Remaining_Midfielders = 4
    Num_Of_Remaining_Strikers = 2
    
    Goalie_Selection_Index = 0
    Def_Selection_Index = 0
    Mid_Selection_Index = 0
    Str_Selection_Index = 0

    Num_Of_Goalie_Options = len(Goalies_Scores.index)
    Num_Of_Defender_Options = len(Defenders_Scores.index)
    Num_Of_Midfielder_Options = len(Midfielders_Scores.index)
    Num_Of_Striker_Options = len(Strikers_Scores.index)

    Cash_To_Spend = Remaining_Money 

    List_Of_Defenders = []
    List_Of_Midfielders = []
    List_Of_Strikers = []
    List_Of_Goalies = []

    Superstar_Goalie = Selected_Superstars[Selected_Superstars['element_type'] == 1]
    List_Of_Goalies.append(Superstar_Goalie['second_name'].values[0])
    
    Superstar_Defender = Selected_Superstars[Selected_Superstars['element_type'] == 2]
    List_Of_Defenders.append(Superstar_Defender['second_name'].values[0])
    
    Superstar_Midfielder = Selected_Superstars[Selected_Superstars['element_type'] == 3]
    List_Of_Midfielders.append(Superstar_Midfielder['second_name'].values[0])

    Superstar_Striker = Selected_Superstars[Selected_Superstars['element_type'] == 4]
    List_Of_Strikers.append(Superstar_Striker['second_name'].values[0])

    for i in range(10): #Pick all players except the goalie
            
        flag = i % 3

        if flag == 0:
            #Add a midfielder to list
            if Num_Of_Remaining_Midfielders != 0:
                #######################################################
                if Num_Of_Remaining_Midfielders == 1:
                    #Add a goalie to list
                    if Num_Of_Remaining_Goalies != 0:
                        Finding_Selection = True
                        while Finding_Selection:
                            Possible_Selection_Name = Goalies_Scores['second_name'].values[Goalie_Selection_Index]
                            Possible_Selection_Cost = Goalies_Scores['now_cost'].values[Goalie_Selection_Index]
                            if Possible_Selection_Name in List_Of_Goalies:
                                Goalie_Selection_Index = Goalie_Selection_Index + 1
                            elif Possible_Selection_Cost > 47:
                                Goalie_Selection_Index = Goalie_Selection_Index + 1
                                if Goalie_Selection_Index == Num_Of_Goalie_Options:
                                    List_Of_Goalies.append("Cant Afford Goalie")
                                    Num_Of_Remaining_Goalies = Num_Of_Remaining_Goalies - 1
                                    Finding_Selection = False
                            else:    
                                List_Of_Goalies.append(Goalies_Scores['second_name'].values[Goalie_Selection_Index])
                                Num_Of_Remaining_Goalies = Num_Of_Remaining_Goalies - 1
                                Cash_To_Spend = Cash_To_Spend - Possible_Selection_Cost
                                Finding_Selection = False
                                
                        Num_Of_Remaining_Players = Num_Of_Remaining_Players - 1
                    ###########################################################################3 
                
                Finding_Selection = True
                while Finding_Selection:
                    Possible_Selection_Name = Midfielders_Scores['second_name'].values[Mid_Selection_Index]
                    Possible_Selection_Cost = Midfielders_Scores['now_cost'].values[Mid_Selection_Index]
                    if Possible_Selection_Name in List_Of_Midfielders:
                        Mid_Selection_Index = Mid_Selection_Index + 1
                    elif Possible_Selection_Cost > Cash_To_Spend:
                        Mid_Selection_Index = Mid_Selection_Index + 1
                        if Mid_Selection_Index == Num_Of_Midfielder_Options:
                            List_Of_Midfielders.append("Cant Afford Midfielder")
                            Num_Of_Remaining_Midfielders = Num_Of_Remaining_Midfielders - 1
                            Finding_Selection = False
                    elif Num_Of_Remaining_Players <= 7:
                        if (Cash_To_Spend-Possible_Selection_Cost) >= ((Num_Of_Remaining_Players-1) * 50):
                            List_Of_Midfielders.append(Midfielders_Scores['second_name'].values[Mid_Selection_Index])
                            Num_Of_Remaining_Midfielders = Num_Of_Remaining_Midfielders - 1
                            Cash_To_Spend = Cash_To_Spend - Possible_Selection_Cost
                            Finding_Selection = False
                        else:
                            Mid_Selection_Index = Mid_Selection_Index + 1
                            if Mid_Selection_Index == Num_Of_Midfielder_Options:
                                List_Of_Midfielders.append("Allocation Not Enough")
                                Num_Of_Remaining_Midfielders = Num_Of_Remaining_Midfielders - 1
                                Finding_Selection = False
                    else:    
                        List_Of_Midfielders.append(Midfielders_Scores['second_name'].values[Mid_Selection_Index])
                        Num_Of_Remaining_Midfielders = Num_Of_Remaining_Midfielders - 1
                        Cash_To_Spend = Cash_To_Spend - Possible_Selection_Cost
                        Finding_Selection = False
                
            else:
                flag = 1

        if flag == 1: 
            #Add a Striker to list
            if Num_Of_Remaining_Strikers != 0:
                Finding_Selection = True
                while Finding_Selection:
                    Possible_Selection_Name = Strikers_Scores['second_name'].values[Str_Selection_Index]
                    Possible_Selection_Cost = Strikers_Scores['now_cost'].values[Str_Selection_Index]
                    if Possible_Selection_Name in List_Of_Strikers:
                        Str_Selection_Index = Str_Selection_Index + 1
                    elif Possible_Selection_Cost > Cash_To_Spend:
                        Str_Selection_Index = Str_Selection_Index + 1
                        if Str_Selection_Index == Num_Of_Striker_Options:
                            List_Of_Strikers.append("Cant Afford Striker")
                            Num_Of_Remaining_Strikers = Num_Of_Remaining_Strikers - 1
                            Finding_Selection = False
                    elif Num_Of_Remaining_Players <= 7:
                        if (Cash_To_Spend-Possible_Selection_Cost) >= ((Num_Of_Remaining_Players-1) * 50):
                            List_Of_Strikers.append(Strikers_Scores['second_name'].values[Str_Selection_Index])
                            Num_Of_Remaining_Strikers = Num_Of_Remaining_Strikers - 1
                            Cash_To_Spend = Cash_To_Spend - Possible_Selection_Cost
                            Finding_Selection = False
                        else:
                            Str_Selection_Index = Str_Selection_Index + 1
                            if Str_Selection_Index == Num_Of_Striker_Options:
                                List_Of_Strikers.append("Allocation Not Enough")
                                Num_Of_Remaining_Strikers = Num_Of_Remaining_Strikers - 1
                                Finding_Selection = False
                    else:    
                        List_Of_Strikers.append(Strikers_Scores['second_name'].values[Str_Selection_Index])
                        Num_Of_Remaining_Strikers = Num_Of_Remaining_Strikers - 1
                        Cash_To_Spend = Cash_To_Spend - Possible_Selection_Cost
                        Finding_Selection = False
            else:
                flag = 2

        if flag == 2: 
            #Add a defender to list
            if Num_Of_Remaining_Defenders != 0:
                Finding_Selection = True
                while Finding_Selection:
                    Possible_Selection_Name = Defenders_Scores['second_name'].values[Def_Selection_Index]
                    Possible_Selection_Cost = Defenders_Scores['now_cost'].values[Def_Selection_Index]
                    if Possible_Selection_Name in List_Of_Defenders:
                        Def_Selection_Index = Def_Selection_Index + 1
                        if Def_Selection_Index == Num_Of_Defender_Options:
                            List_Of_Defenders.append("Cant Afford Defender")
                            Num_Of_Remaining_Defenders = Num_Of_Remaining_Defenders - 1
                            Finding_Selection = False
                    elif Possible_Selection_Cost > Cash_To_Spend:
                        Def_Selection_Index = Def_Selection_Index + 1
                        if Def_Selection_Index == Num_Of_Defender_Options:
                            List_Of_Defenders.append("Cant Afford Defender")
                            Num_Of_Remaining_Defenders = Num_Of_Remaining_Defenders - 1
                            Finding_Selection = False
                    elif Num_Of_Remaining_Players <= 7:
                        if (Cash_To_Spend-Possible_Selection_Cost) >= ((Num_Of_Remaining_Players-1) * 50):
                            List_Of_Defenders.append(Defenders_Scores['second_name'].values[Def_Selection_Index])
                            Num_Of_Remaining_Defenders = Num_Of_Remaining_Defenders - 1
                            Cash_To_Spend = Cash_To_Spend - Possible_Selection_Cost
                            Finding_Selection = False
                        else:
                            Def_Selection_Index = Def_Selection_Index + 1
                            if Def_Selection_Index == Num_Of_Defender_Options:
                                List_Of_Defenders.append("Allocation Not Enough")
                                Num_Of_Remaining_Defenders = Num_Of_Remaining_Defenders - 1
                                Finding_Selection = False
            
                    else:    
                        List_Of_Defenders.append(Defenders_Scores['second_name'].values[Def_Selection_Index])
                        Num_Of_Remaining_Defenders = Num_Of_Remaining_Defenders - 1
                        Cash_To_Spend = Cash_To_Spend - Possible_Selection_Cost
                        Finding_Selection = False
            else:
                flag = 0


        Num_Of_Remaining_Players = Num_Of_Remaining_Players - 1


    #Add a goalie to list
    

    Final_Selection = pd.DataFrame({'Goalies':pd.Series(List_Of_Goalies), 'Defenders':pd.Series(List_Of_Defenders)
                                    ,'Midfielders':pd.Series(List_Of_Midfielders), 'Strikers':pd.Series(List_Of_Strikers)
                                    ,'CashLeft':pd.Series(Cash_To_Spend)})

    return Final_Selection


    """