import numpy as np
import pandas as pd
import shap


def explainer_xgb(model,df_features,idx_prediction):
    '''
    Model: classifier.fit(x_train,y_train)
    df_features: pandas dataframe
    idx_prediction: what prediction to visualize (row #).
    '''

    shap.initjs()

    explainer = shap.TreeExplainer(model)
    shap_values = explainer.shap_values(df_features)

    return shap.force_plot(explainer.expected_value,
                            shap_values[idx_prediction,:],
                            df_features.iloc[idx_prediction,:])


def explainer_regression(model,df_features,nInstances,feature_name, maximum_display):
    ''' Explaining Coefficients '''
    print("Model coefficients:\n")
    for i in range(df_features.shape[1]):
        print(df_features.columns[i], '=', model.coef_[i].round(4))

    ''' Partial Dependency Plot '''
    X_instances = shap.utils.sample(df_features,nInstances)
    shap.plots.partial_dependence(
    "{}".format(feature_name), model.predict, X_instances, ice = False,
    model_expected_value = True, feature_expected_value = True
    )

    ''' Computing Shap Values for linear model '''
    explainer = shap.Explainer(model.predict, X_instances)
    shap_values = explainer(df_features)

    ''' Standard Partial Dependence Plot '''
    sample_ind = 18
    shap.partial_dependence_plot(
    "{}".format(feature_name), model.predict, X_instances,
    model_expected_value = True, feature_expected_value = True, ice = False,
    shap_values = shap_values[sample_ind:sample_ind+1,:]
    )

    ''' Waterfall Plot '''
    shap.plots.waterfall(shap_values[sample_ind], max_display = maximum_display)


def get_interaction_plot_xbg(model,df_features):
    ''' Creates a summary plot of the interations between features for
    a tree-based model.'''
    shap_values = shap.TreeExplainer(model).shap_values(df_features)
    shap_interation_values = shap.TreeExplainer(model).shap_interation_values(df_features)
    return shap.summary_plot(shap_interation_values,df_features)


def get_summary_plot_xbg(model,df_features):
    ''' Creates a summary plot: impact of features on output.'''
    shap_values = shap.TreeExplainer(model).shap_values(df_features)
    return shap.summary_plot(shap_values,df_features)


def get_dependence_plot_xgb(model,df_features,feature_name:str,categorical = 0):
    '''Creates a dependence plot for a feature given as input.'''
    shap_values = shap.TreeExplainer(model).shap_values(df_features)
    return shap.dependence_plot(feature_name,shap_values,df_features)
