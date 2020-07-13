import pulp as p 
import pandas as pd
import numpy as np
from PlayerRatingGenerator import Split_Categories


def Team_Selection_Linear_Optimization(Players):
    
    #Need 11 main players and 4 subs
    # 2 Goalies, 5 Defenders, 5 midefielders, 3 attackers

    Goalies, Defenders, Midfielders, Strikers = Split_Categories(Players)

    Goalie_List = pd.Series.tolist(Goalies['second_name'])
    Def_List = pd.Series.tolist(Defenders['second_name'])
    Mid_List = pd.Series.tolist(Midfielders['second_name'])
    Str_List = pd.Series.tolist(Strikers['second_name'])

    Goalie_Scores = pd.Series.tolist(Goalies['Algorithm Score'])
    Def_Scores = pd.Series.tolist(Defenders['Algorithm Score'])
    Mid_Scores = pd.Series.tolist(Midfielders['Algorithm Score'])
    Str_Scores = pd.Series.tolist(Strikers['Algorithm Score'])

    Goalie_Costs = pd.Series.tolist(Goalies['now_cost'])
    Def_Costs = pd.Series.tolist(Defenders['now_cost'])
    Mid_Costs = pd.Series.tolist(Midfielders['now_cost'])
    Str_Costs = pd.Series.tolist(Strikers['now_cost'])
    
    Goalies_Score_Dict = dict(zip(Goalie_List, Goalie_Scores))
    Goalies_Cost_Dict = dict(zip(Goalie_List, Goalie_Costs))
    
    Def_Score_Dict = dict(zip(Def_List, Def_Scores))
    Def_Cost_Dict = dict(zip(Def_List, Def_Costs))
    
    Mid_Score_Dict = dict(zip(Mid_List, Mid_Scores))
    Mid_Cost_Dict = dict(zip(Mid_List, Mid_Costs))
    
    Str_Score_Dict = dict(zip(Str_List, Str_Scores))
    Str_Cost_Dict = dict(zip(Str_List, Str_Costs))

    # Create a LP Maximization problem 
    Lp_prob = p.LpProblem('Select Team of 15 with highest expected returns', p.LpMaximize)  
  
    # Create problem Variables  
    Goalies_Variables = p.LpVariable.dict("Gol", Goalie_List, lowBound = 0, cat='Binary')   # Create a variable x >= 0 
    Defenders_Variables = p.LpVariable.dict("Def", Def_List, lowBound = 0, cat='Binary')   # Create a variable x >= 0 
    Midfielders_Variables = p.LpVariable.dict("Mid", Mid_List, lowBound = 0, cat='Binary')   # Create a variable x >= 0 
    Strikers_Variables = p.LpVariable.dict("Str", Str_List, lowBound = 0, cat='Binary')   # Create a variable x >= 0 
    
    # Objective Function 
    # The objective function is to select 15 players that provide the largest possible
    # score given the constraints
    
    Objective_Func_Segment_One = p.lpSum([Goalies_Score_Dict[i] * Goalies_Variables[i] for i in Goalie_List])
    Objective_Func_Segment_Two = p.lpSum([Def_Score_Dict[i] * Defenders_Variables[i] for i in Def_List])
    Objective_Func_Segment_Three = p.lpSum([Mid_Score_Dict[i] * Midfielders_Variables[i] for i in Mid_List])
    Objective_Func_Segment_Four = p.lpSum([Str_Score_Dict[i] * Strikers_Variables[i] for i in Str_List])
      
    Lp_prob += Objective_Func_Segment_One + Objective_Func_Segment_Two + Objective_Func_Segment_Three + Objective_Func_Segment_Four
    
    # Cost Constraint: 
    Cost_Constraint_Segment_One = p.lpSum([Goalies_Cost_Dict[i] * Goalies_Variables[i] for i in Goalie_List])
    Cost_Constraint_Segment_Two = p.lpSum([Def_Cost_Dict[i] * Defenders_Variables[i] for i in Def_List])
    Cost_Constraint_Segment_Three = p.lpSum([Mid_Cost_Dict[i] * Midfielders_Variables[i] for i in Mid_List])
    Cost_Constraint_Segment_Four = p.lpSum([Str_Cost_Dict[i] * Strikers_Variables[i] for i in Str_List])

    Lp_prob += (Cost_Constraint_Segment_One 
                + Cost_Constraint_Segment_Two
                + Cost_Constraint_Segment_Three 
                + Cost_Constraint_Segment_Four) <= 1000
    
    # Player Count Constraints:
    # 2 goalies, 5 defenders, 5 midfielders, 2 strikers
    Lp_prob += p.lpSum([Goalies_Variables[i] for i in Goalie_List]) == 2
    Lp_prob += p.lpSum([Defenders_Variables[i] for i in Def_List]) == 5
    Lp_prob += p.lpSum([Midfielders_Variables[i] for i in Mid_List]) == 5
    Lp_prob += p.lpSum([Strikers_Variables[i] for i in Str_List]) == 3

    Lp_prob.solve()   # Solver 
     
    ListOfDef = []
    ListOfMid = []
    ListOfStr = []
    ListOfGoalies = []
    Cash_Left = 1000

    for constraint in Lp_prob.constraints:
        Constraint_Value = Lp_prob.constraints[constraint].value() - Lp_prob.constraints[constraint].constant

        if(Constraint_Value > 800):
            Cash_Left = (1000 - Constraint_Value) / 10

    for PlayerSelection in Lp_prob.variables():
        if PlayerSelection.varValue > 0:            
            if PlayerSelection.name[0] == 'G':
                ListOfGoalies.append(PlayerSelection.name)

            elif PlayerSelection.name[0] == 'D':   
                ListOfDef.append(PlayerSelection.name)

            elif PlayerSelection.name[0] == 'M':
                ListOfMid.append(PlayerSelection.name)
 
            elif PlayerSelection.name[0] == 'S': 
                ListOfStr.append(PlayerSelection.name)
            
            else:
                print("Unknown Variable Name")


    return ListOfGoalies, ListOfDef, ListOfMid, ListOfStr, Cash_Left


