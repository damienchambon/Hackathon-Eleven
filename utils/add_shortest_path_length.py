#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import networkx as nx
import os
import pandas as pd


def add_shortest_path_length(merged_df, graph_path):
    '''
    Returns the dataframe passed as an input where
    a column representing the length of the shortest path
    between a gate and a runway was added.
    Input: Pandas dataframe object,
    Output: Pandas dataframe object with one extra column
    '''

    # loading the Excel file containing the graph information
    xls = pd.ExcelFile(graph_path)

    # loading the coordinates of the airport stands
    stands = pd.read_excel(xls, 'stands')

    # loading the turning points to go to runways
    t_points_runways = pd.read_excel(xls, 'ts2')

    # creating the graph
    G = nx.DiGraph()

    # adding the stand nodes
    for i in range(len(stands)):
        G.add_node(str(stands.iloc[i, 0]))

    # creating the turning points and runways
    Ts = [
        'T1', 'T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'T8',
        'T9', 'T10', 'T11', 'T12', 'T14', 'T15', 'T16'
        ]
    Rs = [
        'RUNWAY_1', 'RUNWAY_2', 'RUNWAY_3', 'RUNWAY_4'
        ]

    # adding turning points and runways as nodes
    for t in Ts:
        G.add_node(t)
    for r in Rs:
        G.add_node(r)

    # creating connections stands and turning points with distances as weights
    for i in range(len(stands)):
        G.add_edge(str(stands.iloc[i, 0]),
                   str(stands.iloc[i, 1]),
                   weight=stands.iloc[i, 2])
        G.add_edge(str(stands.iloc[i, 1]),
                   str(stands.iloc[i, 0]),
                   weight=stands.iloc[i, 2])

    # creating connections turning points and runways with distances as weights
    for i in range(len(t_points_runways)):
        G.add_edge(str(t_points_runways.iloc[i, 0]),
                   str(t_points_runways.iloc[i, 1]),
                   weight=t_points_runways.iloc[i, 2])
        G.add_edge(str(t_points_runways.iloc[i, 1]),
                   str(t_points_runways.iloc[i, 0]),
                   weight=t_points_runways.iloc[i, 2])

    # filling in the shortest path length in the dataframe
    # using the stand and the runway as an input to the function
    # used to compute the shortest path
    full_df = merged_df.copy()
    full_df['shortest_path_length'] = full_df\
        .apply(lambda x:
               nx.shortest_path_length(G, source=x['stand'].split('_')[1],
                                       target=x['runway'],
                                       weight='string')-2, axis=1)

    return full_df
