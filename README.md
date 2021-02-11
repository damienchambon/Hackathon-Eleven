# Hackathon-Eleven
 Repository for the Hackathon organized by Eleven strategy (Feb 2021)




## Taxi Time Prediction

The project regards the prediction of the taxi time in a major airport.

Following, a quick documentation on how to use and launch the code, and the main resources we provide for the project.

We used this cool command: `var example = true`



## Configuration

The main repositories are:

1. Utils

- date2datetime.py: contains two functions that load the airport, weather and
  aicraft datasets as pandas dataframes and transforms the relevant columns into
  datetime formats. The first function takes paths as input, while the second
  one directly takes pandas dataframes.
- date_functions.py: contains 13 functions that were used in exploration (not
  all of them) for date formatting purposes, or calendar objects extractions.
  For instance, the function int2datetime() transforms the integer 20210211 into
  a datetime object corresponding to 11-02-2021.
- geographic_distance.py: contains a single function that computes the distance
  (in km) between two points, given the respective latitudes and longitudes.
- explainability.py: mostly contains implementations of library 'shap'. Most
  functions take as input a fitted model and a pandas dataframe of features.
  The function explainer_xgb() will produce a plot to visualise the impact of
  features on the target variable. The function get_interation_plot_tree()
  will produce an interaction plot for tree-based models;  get_summary_plot_tree()
  will produce a summary plot with the impact of features on model output;
  get_dependence_plot_tree() will produce a partial dependence plot based on
  a feature selected as input.
2. Data Exploration
3. Models
