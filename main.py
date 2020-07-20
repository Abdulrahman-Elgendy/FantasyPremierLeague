#Testing git repo
import pandas as pd
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
import pdb

FPL_API_Url = 'https://fantasy.premierleague.com/api/bootstrap-static/'
JSON_Data = Load_JSON_Data_From_URL(FPL_API_Url)
players, teams, events = ParseMainAPI(JSON_Data)

#form, ROI, ptsPerGame, ICT index, ep_next, Future Games Score
Regular_Scoring_Weights = [0.3, 0.1 , 0.15, 0.1, 0.1, 0.25] 

#form, totalPts, Future Games Score
Superstar_Scoring_Weights = [0.4, 0.4, 0.2]

Players_Scores = Calculate_Players_Scores_Regular(players, Regular_Scoring_Weights)

#pdb.set_trace()
#List = Split_Based_On_Categories(Players_Scores, Category_Type='TeamsANDPositions')

ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left = Team_Selection_Linear_Optimization(Players_Scores)

Draw_Three_Four_Three(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)
#Draw_Four_Four_Two(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)

#Draw_Three_Five_Two(ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left)

"""
PlayerName = 'Romeu'
ExtraMoney = 0.2

MyPlayerDetails = GetPlayerDetails(PlayerName,players)

MyReplacement = SelectReplacement(MyPlayerDetails, ExtraMoney, Goalies_Scores, Defenders_Scores, Midfielders_Scores, Strikers_Scores)

print("///////////////////////////////////////////////////////////////////////////////")
print(MyReplacement)


#Draw_Four_Four_Two(Final_Team)

#Draw_Three_Five_Two(Final_Team)
"""
