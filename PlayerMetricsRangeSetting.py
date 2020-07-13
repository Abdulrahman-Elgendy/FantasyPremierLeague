import numpy as np
import pandas as pd

def SetRange_One_To_Ten(Player_Info, ColumnToAdjust):
    
    #Takes all the numbers in a column and sets their range to be from one to 10
    
    Float_Column = pd.to_numeric(Player_Info[ColumnToAdjust])
    Player_Info.drop(columns=[ColumnToAdjust], axis=1, inplace=True)
    Player_Info_Numeric = pd.concat([Player_Info, Float_Column], axis=1)
    Player_Info_Numeric.sort_values(by=ColumnToAdjust, inplace = True, ascending=False)
    Highest_Value_In_Col = Player_Info_Numeric[ColumnToAdjust].values[0]
    Player_Info_Numeric[ColumnToAdjust] = (Player_Info_Numeric[ColumnToAdjust]/Highest_Value_In_Col) * 10 #form now between 1-10

    return Player_Info_Numeric