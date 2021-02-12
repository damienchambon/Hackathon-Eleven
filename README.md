# Hackathon-Eleven
 Repository for the Hackathon organized by Eleven strategy (Feb 2021)




## Taxi Time Prediction

The project regards the prediction of the taxi time in a major airport.

Following, a quick documentation on how to use and launch the code, and the main resources we provide for the project.




## Configuration

The main repositories are:

1. main

    * The main.py function will call cleaning, joining, preprocessing, training and testing functions.

2. utils

    * date2datetime.py: contains two functions that load the airport, weather and
      aicraft datasets as pandas dataframes and transforms the relevant columns into
      datetime formats. The first function takes paths as input, while the second
      one directly takes pandas dataframes.
    * date_functions.py: contains 13 functions that were used in exploration (not
      all of them) for date formatting purposes, or calendar objects extractions.
      For instance, the function int2datetime() transforms the integer 20210211 into
      a datetime object corresponding to 11-02-2021.
    * geographic_distance.py: contains a single function that computes the distance
      (in km) between two points, given the respective latitudes and longitudes.
    * explainability.py: mostly contains implementations of library 'shap'. Most
      functions take as input a fitted model and a pandas dataframe of features.
      The function explainer_xgb() will produce a plot to visualise the impact of
      features on the target variable. The function get_interation_plot_tree()
      will produce an interaction plot for tree-based models;  get_summary_plot_tree()
      will produce a summary plot with the impact of features on model output;
      get_dependence_plot_tree() will produce a partial dependence plot based on
      a feature selected as input.
    * Graph_airport.ipynb: has the construction of a graph with the distances between stands and runways
    * add_current_load_airport_N_Q.py: function that computes the N number of aircrafts moving 
        when the airplane starts taxing and also Q, which are 
        the number of aircrafts that finished the movement while 
        the aircraft in focus is still moving.
    * add_current_load_runway.py: Returns the dataframe passed as an input where
        a column representing the load on the runway was added.
        Here, the current load on the runway accounts for how many
        planes were taxiing at the same time and heading to the same
        runway when a specific aircraft starts taxiing.
    * add_shortest_path_length.py: Returns the dataframe passed as an input where
        a column representing the length of the shortest path between a gate and a runway was added.
    * dataset_cleaning.py: cleans all the datasets (accepts different modes -> mode='train' or mode='test')
    * dataset_joining.py: joins the four main dataframes.
    * Preprocessing.py: generates the preprocessing on the merged dataframe. The preprocessing includes the generation of the target   variable, the drop of several useless columns, scaling and OneHot Encoding.

    * train.py: training function that trains the selected model Light GBM on the training data.
    

3. resources
    * In this folder you would need to add the data with the name specified in the main.py
  
4. data exploration
    * Weather data exploration
    * General first exploration
    * Airport location exploration

5. models
    * In this folder you can save the model trained during the train function
