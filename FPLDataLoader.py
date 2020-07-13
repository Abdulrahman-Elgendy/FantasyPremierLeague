import numpy as np
import pandas as pd
import os
import json
import requests

def Load_JSON_Data_From_URL(url):
    Server_Response = requests.get(url) #get the data from the API and save it as a response object
    return json.loads(Server_Response.content) #extract data in JSON format
    #The response from the FPL API should be a dict with 8 attributes:
    # elements, element_stats, element_types, events, game_settings, phases, teams, total_players

    #The most valuable info are in :elements, events, and teams
    #elements: Player summary data such as total points and costs
    #events: gameweek data such as id, deadline time, and highest scoring player
    #Teams: Data for each team such as name, and id as well as scores for the team attack, defence, overall when home and away

def ParseMainAPI(JSON_Data):
    players = JSON_Data['elements']
    teams = JSON_Data['teams']
    events = JSON_Data['events']

    Players_df = pd.DataFrame(players)
    teams_df = pd.DataFrame(teams)
    events_df = pd.DataFrame(events)

    return Players_df, teams_df, events_df

def ParseElementSummary(JSON_Data):
    Player_fixtures = JSON_Data['fixtures']

    Player_Future_Games_df = pd.DataFrame(Player_fixtures)

    return Player_Future_Games_df
