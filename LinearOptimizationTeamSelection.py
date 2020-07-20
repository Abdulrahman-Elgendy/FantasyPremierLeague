import pulp as p 
import pandas as pd
import numpy as np
from PlayerRatingGenerator import Split_Based_On_Categories

Num_Of_Prem_Teams = 20
Num_Of_Playing_Positions = 4

def Add_Players_Full_Name(Players): 
    PlayersFullName = Players['first_name'] + '_' + Players ['second_name']
    Players_Final = pd.concat([Players,PlayersFullName], axis = 1)
    Players_Final.rename(columns={0:'full_name'}, inplace=True)

    return Players_Final

def Score_And_Cost_Dict_Creator(Players):
    Players_Names_List = pd.Series.tolist(Players['full_name'])
    Players_Scores = pd.Series.tolist(Players['Algorithm Score'])
    Players_Costs = pd.Series.tolist(Players['now_cost'])
    Players_Score_Dict = dict(zip(Players_Names_List, Players_Scores))
    Players_Cost_Dict = dict(zip(Players_Names_List, Players_Costs))

    return Players_Names_List, Players_Score_Dict, Players_Cost_Dict

def Team_Selection_Linear_Optimization(Players):

    """
    Goalies, Defenders, Midfielders, Strikers = Split_Based_On_Categories(Players)
    
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

    # Create problem Variables  
    Goalies_Variables = p.LpVariable.dict("Gol", Goalie_List, lowBound = 0, cat='Binary')   # Create a variable x >= 0 
    Defenders_Variables = p.LpVariable.dict("Def", Def_List, lowBound = 0, cat='Binary')   # Create a variable x >= 0 
    Midfielders_Variables = p.LpVariable.dict("Mid", Mid_List, lowBound = 0, cat='Binary')   # Create a variable x >= 0 
    Strikers_Variables = p.LpVariable.dict("Str", Str_List, lowBound = 0, cat='Binary')   # Create a variable x >= 0 
    
    
    # Objective Function 
    Objective_Func_Segment_One = p.lpSum([Goalies_Score_Dict[i] * Goalies_Variables[i] for i in Goalie_List])
    Objective_Func_Segment_Two = p.lpSum([Def_Score_Dict[i] * Defenders_Variables[i] for i in Def_List])
    Objective_Func_Segment_Three = p.lpSum([Mid_Score_Dict[i] * Midfielders_Variables[i] for i in Mid_List])
    Objective_Func_Segment_Four = p.lpSum([Str_Score_Dict[i] * Strikers_Variables[i] for i in Str_List])
      
    Lp_prob += Objective_Func_Segment_One + Objective_Func_Segment_Two + Objective_Func_Segment_Three + Objective_Func_Segment_Four
    
    #Constraints:
    Cost_Constraint_Segment_One = p.lpSum([Goalies_Cost_Dict[i] * Goalies_Variables[i] for i in Goalie_List])
    Cost_Constraint_Segment_Two = p.lpSum([Def_Cost_Dict[i] * Defenders_Variables[i] for i in Def_List])
    Cost_Constraint_Segment_Three = p.lpSum([Mid_Cost_Dict[i] * Midfielders_Variables[i] for i in Mid_List])
    Cost_Constraint_Segment_Four = p.lpSum([Str_Cost_Dict[i] * Strikers_Variables[i] for i in Str_List])

    Lp_prob += (Cost_Constraint_Segment_One 
                + Cost_Constraint_Segment_Two
                + Cost_Constraint_Segment_Three 
                + Cost_Constraint_Segment_Four) <= 1000
    """

    Players_With_Full_Names = Add_Players_Full_Name(Players)

    Player_Info_List_Of_DataFrames = Split_Based_On_Categories(Players_With_Full_Names, Category_Type='TeamsANDPositions')

    List_Of_Teams = []
    for i in range(Num_Of_Prem_Teams):
        List_Of_Positions = []
        for j in range(Num_Of_Playing_Positions):
            List_Of_Dictionaries = []
            Players_Names_List, Players_Score_Dict, Players_Cost_Dict = Score_And_Cost_Dict_Creator(Player_Info_List_Of_DataFrames[i][j])
            List_Of_Dictionaries.extend([Players_Names_List, Players_Score_Dict, Players_Cost_Dict])
            List_Of_Positions.append(List_Of_Dictionaries)

        List_Of_Teams.append(List_Of_Positions)

    # Create a LP Maximization problem 
    Lp_prob = p.LpProblem('Select Team of 15 with highest expected returns', p.LpMaximize)  

    #Create problem variables
    Team_Variables = []
    for i in range(Num_Of_Prem_Teams):
        Positions_Variables = []
        Goalies_Variables = p.LpVariable.dict("Gol", List_Of_Teams[i][0][0], lowBound = 0, cat='Binary')   # Create a variable x >= 0 
        Defenders_Variables = p.LpVariable.dict("Def",List_Of_Teams[i][1][0], lowBound = 0, cat='Binary')   # Create a variable x >= 0 
        Midfielders_Variables = p.LpVariable.dict("Mid", List_Of_Teams[i][2][0], lowBound = 0, cat='Binary')   # Create a variable x >= 0 
        Strikers_Variables = p.LpVariable.dict("Str", List_Of_Teams[i][3][0], lowBound = 0, cat='Binary')   # Create a variable x >= 0 
        Positions_Variables.extend([Goalies_Variables, Defenders_Variables, Midfielders_Variables, Strikers_Variables])
        Team_Variables.append(Positions_Variables)

    # Objective Function
    Sum_Of_Segments = 0
    for i in range(Num_Of_Prem_Teams):
        Objective_Func_Segment_One = p.lpSum([List_Of_Teams[i][0][1][j] * Team_Variables[i][0][j] for j in List_Of_Teams[i][0][0]])
        Objective_Func_Segment_Two = p.lpSum([List_Of_Teams[i][1][1][j] * Team_Variables[i][1][j] for j in List_Of_Teams[i][1][0]])
        Objective_Func_Segment_Three = p.lpSum([List_Of_Teams[i][2][1][j] * Team_Variables[i][2][j] for j in List_Of_Teams[i][2][0]])
        Objective_Func_Segment_Four = p.lpSum([List_Of_Teams[i][3][1][j] * Team_Variables[i][3][j] for j in List_Of_Teams[i][3][0]])
        Sum_Of_Segments = (Sum_Of_Segments + Objective_Func_Segment_One 
                          + Objective_Func_Segment_Two + Objective_Func_Segment_Three
                          + Objective_Func_Segment_Four)

    Lp_prob += Sum_Of_Segments

    # Constraints: We will have 25 constraints for this optimization problem
    # Cost constraint:
    Sum_Of_Segments = 0
    for i in range(Num_Of_Prem_Teams):
        Const_Segment_One = p.lpSum([List_Of_Teams[i][0][2][j] * Team_Variables[i][0][j] for j in List_Of_Teams[i][0][0]])
        Const_Segment_Two = p.lpSum([List_Of_Teams[i][1][2][j] * Team_Variables[i][1][j] for j in List_Of_Teams[i][1][0]])
        Const_Segment_Three = p.lpSum([List_Of_Teams[i][2][2][j] * Team_Variables[i][2][j] for j in List_Of_Teams[i][2][0]])
        Const_Segment_Four = p.lpSum([List_Of_Teams[i][3][2][j] * Team_Variables[i][3][j] for j in List_Of_Teams[i][3][0]])
        Sum_Of_Segments = (Sum_Of_Segments + Const_Segment_One 
                          + Const_Segment_Two + Const_Segment_Three
                          + Const_Segment_Four)

    Lp_prob += (Sum_Of_Segments) <= 1000

    #Number Of Players in each position constraints:
    Sum_Of_Goalie_Segments = 0
    Sum_Of_Def_Segments = 0
    Sum_Of_Mid_Segments = 0
    Sum_Of_Str_Segments = 0

    for i in range(Num_Of_Prem_Teams):
        Goalie_Segment = p.lpSum([Team_Variables[i][0][j] for j in List_Of_Teams[i][0][0]])
        Def_Segment = p.lpSum([Team_Variables[i][1][j] for j in List_Of_Teams[i][1][0]])
        Mid_Segment = p.lpSum([Team_Variables[i][2][j] for j in List_Of_Teams[i][2][0]])
        Str_Segment = p.lpSum([Team_Variables[i][3][j] for j in List_Of_Teams[i][3][0]])
        Sum_Of_Goalie_Segments = Sum_Of_Goalie_Segments + Goalie_Segment
        Sum_Of_Def_Segments = Sum_Of_Def_Segments + Def_Segment
        Sum_Of_Mid_Segments = Sum_Of_Mid_Segments + Mid_Segment
        Sum_Of_Str_Segments = Sum_Of_Str_Segments + Str_Segment

    Lp_prob += (Sum_Of_Goalie_Segments) == 2
    Lp_prob += (Sum_Of_Def_Segments) == 5
    Lp_prob += (Sum_Of_Mid_Segments) == 5
    Lp_prob += (Sum_Of_Str_Segments) == 3

    #Max of 3 Players from each Team Constraint. This will be 20 different constraints 
    for i in range(Num_Of_Prem_Teams):
        Goalie_Segment = p.lpSum([Team_Variables[i][0][j] for j in List_Of_Teams[i][0][0]])
        Def_Segment = p.lpSum([Team_Variables[i][1][j] for j in List_Of_Teams[i][1][0]])
        Mid_Segment = p.lpSum([Team_Variables[i][2][j] for j in List_Of_Teams[i][2][0]])
        Str_Segment = p.lpSum([Team_Variables[i][3][j] for j in List_Of_Teams[i][3][0]])
        Team_Members_Segments = Goalie_Segment + Def_Segment + Mid_Segment + Str_Segment
        Lp_prob += (Team_Members_Segments) <= 3

    # Display the problem 
    #print(Lp_prob) 
  
    Lp_prob.solve()   # Solver 
    #print(p.LpStatus[Lp_prob.status])   # The solution status 
  
    # Printing the final solution 
    # print(p.value(Lp_prob.objective)) 
     
    ListOfDef = []
    ListOfMid = []
    ListOfStr = []
    ListOfGoalies = []
    Cash_Left = 1000

    for constraint in Lp_prob.constraints:
        Constraint_Name = Lp_prob.constraints[constraint].name
        Constraint_Value = Lp_prob.constraints[constraint].value() - Lp_prob.constraints[constraint].constant

        if(Constraint_Value > 800):
            Cash_Left = (1000 - Constraint_Value) / 10

        print("///////////////////////////////////")
        print(Constraint_Name, Constraint_Value)
        print("///////////////////////////////////")


    for PlayerSelection in Lp_prob.variables():
        if PlayerSelection.varValue > 0:
            
            #print(PlayerSelection.name)
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


