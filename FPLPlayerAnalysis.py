import numpy as np
import pandas as pd
from FPLDataLoader import Load_JSON_Data_From_URL
from FPLDataLoader import ParseElementSummary

def Get_Players_ROI(Players_Info):
    
    Float_form = pd.to_numeric(Players_Info['form'])
    Players_Info.drop(columns=['form'], axis=1, inplace=True)
    Players_Info_Numeric = pd.concat([Players_Info, Float_form], axis=1)

    Players_form = Players_Info_Numeric['form']
    Players_Info_Numeric.astype({'now_cost': 'float'})
    Players_Cost = Players_Info_Numeric['now_cost'] / 10
    PlayersROI = Players_form/Players_Cost 
   
    #Now need to move back to the original dataframe
    Players_Info_With_ROI = pd.concat([Players_Info_Numeric,PlayersROI], axis = 1)
    Players_Info_With_ROI.rename(columns={0:'ROI'}, inplace=True)
     
    return Players_Info_With_ROI

def Get_Players_Future_Games_Info(PlayerID):

    FPL_Player_API_Url = 'https://fantasy.premierleague.com/api/element-summary/'
    Player_id_string = str(PlayerID) + '/'
    Complete_Player_url = FPL_Player_API_Url + Player_id_string
    JSON_Data = Load_JSON_Data_From_URL(Complete_Player_url)
    player_fixtures = ParseElementSummary(JSON_Data)

    return player_fixtures


def Get_Players_Future_Games_Scores(Players_Info):

    Players_Info['Future Games Score'] = 0
    Num_Players = len(Players_Info.index)
    Num_Future_Games_To_Analyze = 3
    for i in range(Num_Players):
        Player_id = Players_Info['id'].iloc[i]
        Player_Fixtures = Get_Players_Future_Games_Info(Player_id)
        Difficulty_Mean = Player_Fixtures['difficulty'].iloc[0:Num_Future_Games_To_Analyze].mean(axis=0)
        Players_Info['Future Games Score'].iloc[i] = (4-Difficulty_Mean)

    return Players_Info




    
