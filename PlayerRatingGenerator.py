import numpy as np
import pandas as pd
from FPLPlayerAnalysis import Get_Players_ROI
from FPLPlayerAnalysis import Get_Players_Future_Games_Scores
from PlayerMetricsRangeSetting import SetRange_One_To_Ten

#Need 11 main players and 4 subs
# 2 Goalies, 5 Defenders, 5 midefielders, 3 attackers

def Split_Categories(Players_Info):
    GoalKeepers = Players_Info[Players_Info['element_type'] == 1]
    Defenders = Players_Info[Players_Info['element_type'] == 2]
    Midfielders = Players_Info[Players_Info['element_type'] == 3]
    Strikers = Players_Info[Players_Info['element_type'] == 4]

    return GoalKeepers, Defenders, Midfielders, Strikers

def Calculate_Players_Scores_Regular(Players_Info, Weights):

    Players_Filtered = Players_Info[Players_Info['minutes'] > 270]
    Player_Info_Add_ROI = Get_Players_ROI(Players_Filtered)
    #only returns ROI for Players who played more than 9 games this season
    #Midfielder_Final_Filter = Defender_Initial_Filter[Goalies_Initial_Filter['chance_of_playing_next_round'] == 100] 

    print(Player_Info_Add_ROI['form'])
    Players_Info_Add_Future_Games_Score = Get_Players_Future_Games_Scores(Player_Info_Add_ROI)
    print (Players_Info_Add_Future_Games_Score['form'])
    
    Players_Info_Adjusted1 = SetRange_One_To_Ten(Players_Info_Add_Future_Games_Score,'form')
    Players_Info_Adjusted2 = SetRange_One_To_Ten(Players_Info_Adjusted1,'points_per_game')
    Players_Info_Adjusted3 = SetRange_One_To_Ten(Players_Info_Adjusted2,'ict_index')
    Players_Info_Adjusted4 = SetRange_One_To_Ten(Players_Info_Adjusted3,'influence')
    Players_Info_Adjusted5 = SetRange_One_To_Ten(Players_Info_Adjusted4,'ep_next')
    Players_Info_Adjusted6 = SetRange_One_To_Ten(Players_Info_Adjusted5,'ROI')
    Players_Final_df = SetRange_One_To_Ten(Players_Info_Adjusted6,'Future Games Score')


    Weighted_Sum = ((Players_Final_df['form'].multiply(Weights[0])) 
                           + (Players_Final_df['ROI'].multiply(Weights[1])) 
                           + (Players_Final_df['points_per_game'].multiply(Weights[2]))
                           + (Players_Final_df['ict_index'].multiply(Weights[3]))
                           + (Players_Final_df['ep_next'].multiply(Weights[4]))                          
                           + (Players_Final_df['Future Games Score'].multiply(Weights[5])))

    Denominator = Weights[0] + Weights[1] + Weights[2] + Weights[3] +Weights[4]
    
    Weighted_Avg_Sum = Weighted_Sum / Denominator

    Players_Info_Final = pd.concat([Players_Final_df, Weighted_Avg_Sum], axis = 1)
    Players_Info_Final.rename(columns={0:'Algorithm Score'}, inplace=True)
    Players_Info_Final.sort_values(by='Algorithm Score', inplace = True, ascending=False)

    return Players_Info_Final[['first_name','second_name','ep_next'
                                ,'element_type','now_cost','form','ict_index'
                                ,'points_per_game','ROI','Future Games Score'
                                ,'Algorithm Score']]

def Calculate_Players_Scores_Superstars(Player_Info, Weights):
    
    Players_Filtered = Player_Info[Player_Info['minutes'] > 810] #only returns ROI for Players who played more than 9 games this season
    Player_Info_With_ROI = Get_Players_ROI(Players_Filtered)
    Players_Info_With_Future_Games_Score = Get_Players_Future_Games_Scores(Player_Info_With_ROI)
    
    Players_Info_Adjusted1 = SetRange_One_To_Ten(Players_Info_With_Future_Games_Score,'form')
    Players_Final_df = SetRange_One_To_Ten(Players_Info_Adjusted1,'total_points')

    Weighted_Sum = ((Players_Final_df['form'].multiply(Weights[0])) 
                    + (Players_Final_df['total_points'].multiply(Weights[1])))

    Denominator = Weights[0] + Weights[1]
    
    Weighted_Avg_Sum = Weighted_Sum / Denominator

    Players_Info_Final = pd.concat([Players_Final_df, Weighted_Avg_Sum], axis = 1)
    Players_Info_Final.rename(columns={0:'Algorithm Score'}, inplace=True)
    Players_Info_Final.sort_values(by='Algorithm Score', inplace = True, ascending=False)

    return Players_Info_Final[['first_name','second_name','element_type'
                                ,'now_cost','form' ,'total_points'
                                ,'Future Games Score','Algorithm Score']]



