import requests
import json
import pandas as pd
import numpy as np



def getSeasonDataFromAPI(url, season, per_page=100):
    '''
    Args
        - url = games url
        - page = page number
        - per_page = numer of results per page
        - seasons = array of seasons
    Returns dataframe
    '''

    # First, make initial API request to get total number of pages
    # Set up parameters
    parameters={'page':1, 'per_page':per_page, 'seasons[]':season}
    # Make request
    initialRequest = requests.get(url, params=parameters).json()
    # Find total pages
    totalPages = initialRequest['meta']['total_pages']

    # Initialize dataframe
    seasonDF = pd.DataFrame()

    # Iterate through each page
    for pageNum in range(1, totalPages+1):
        
        # Make request for page
        parameters={'page':pageNum, 'per_page':per_page, 'seasons[]':season}
        resp = requests.get(url, params=parameters).json()
        
        # Create dataframe
        df = pd.DataFrame.from_records(resp['data'])

        # Concatenate
        seasonDF = pd.concat([seasonDF, df])

    return seasonDF


def convertDictColumns(dataframe, columnList):
    '''
    Args
        - dataframe
        - columnList = list of dictionary-like columns
    Returns dataframe with added columns = keys of dictionary
    '''

    # Iterate through columns
    for column in columnList:

        # Iterate through keys
        for k in dataframe.loc[0, column].values[0].keys():
            # Create a column named [column name]_[key value]
            # Ex. 'home_team' has a key called 'full_name'
            # So a column called 'home_team_full_name' will be created
            dataframe[column+"_"+k] = dataframe[column].apply(lambda x: x[k])

    return dataframe
    


def makeEastWestDF(dataframe, homeTeamNameCol='home_team_full_name', visitorTeamNameCol='visitor_team_full_name', homeTeamConferenceCol='home_team_conference', visitorTeamConferenceCol='visitor_team_conference', homeTeamScoreCol='home_team_score', visitorTeamScoreCol='visitor_team_score'):
    """
    Filters the original DataFrames to only display games
    of an East conference team playing against a West conference team.
    The resulting DataFrame is used for a hypothesis test
    comparing the scores of the two difference conferences.

    Parameters
    ----------    
    data: Original DataFrame name

    Returns
    -------
    DataFrame

    """
    # Filter to only include games where East team plays West team
    data = dataframe.loc[((dataframe[homeTeamConferenceCol] == "East")
                     & (dataframe[visitorTeamConferenceCol] == "West"))
                    | ((dataframe[homeTeamConferenceCol] == "West")
                       & (dataframe[visitorTeamConferenceCol] == "East"))]
    # Creating East columns
    data['east_team'] = np.where(data[homeTeamConferenceCol] == "East",
                                 data[homeTeamNameCol],
                                 data[visitorTeamNameCol])
    data['east_score'] = np.where(data[homeTeamConferenceCol] == "East",
                                  data[homeTeamScoreCol],
                                  data[visitorTeamScoreCol])
    # Creating West columns
    data['west_team'] = np.where(data[homeTeamConferenceCol] == "West",
                                 data[homeTeamNameCol],
                                 data[visitorTeamNameCol])
    data['west_score'] = np.where(data[homeTeamConferenceCol] == "West",
                                  data[homeTeamScoreCol],
                                  data[visitorTeamScoreCol])
    # Create a column with difference in scores
    data['east_minus_west'] = data['east_score'] - data['west_score']
   
    return data



def make_home_df(dataframe, conference=None, n=None):
    """
    Filters the original DataFrames to only display home game scores.
    The resulting DataFrame is used for a hypothesis test
    comparing the score differences of games for the home teams
    to analyze which teams perform the best in their home courts.

    Parameters
    ----------
    dataframe: = Original DataFrame name
    conference: = "East" or "West" (default = None)
    n: = Number of teams to display (default = None)
        Teams are sorted by their score difference means in descending order.

    Returns
    -------
    DataFrame

    """
    data = dataframe.copy()
    # Calculate difference between home team score and visitor team score
    data['home_score_diff'] = data['home_team_score'] - data['visitor_team_score']
    # If conference is specified, filter data to only include teams in the conference
    if conference is not None:
        data = data.loc[data['home_team_conference'] == conference]
    # If n is specified, obtain the top n teams with highest means and filter original dataframe to only include those teams
    if n is not None:
        # Get means of each team
        top_n = pd.DataFrame(data.groupby('home_team_full_name')['home_score_diff'].mean())
        top_n.reset_index(inplace=True)
        # Sort by means, descending
        top_n.sort_values(by='home_score_diff', ascending=False, inplace=True)
        # Obtain top n teams
        top_n_teams = top_n['home_team_full_name'][:n]
        # Filter data to only include teams in top_n_teams
        data = data.loc[data['home_team_full_name'].isin(top_n_teams)]
    # Return team name and score difference columns
    data = data[['home_team_full_name', 'home_score_diff']]

    return data
