#!/usr/bin/env python3
# -*- coding: utf-8 -*-

def train(X,y):
    '''
    Trains a Light GBM Model on the training data.
    Input: X_train, y_train
    Displays the accuracy on validation set for a time window of
    3 and 5 minutes
    Output: returns the model
    '''
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.33, random_state=42
        )

    # best model that we found after doing a grid search
    gbm = lgb.LGBMRegressor(num_leaves=400,
                            learning_rate=0.05,
                            n_estimators=500)

    # train the model
    model = gbm.fit(X_train, y_train,
                    eval_set=[(X_test, y_test)],
                    eval_metric='l1',
                    early_stopping_rounds=30)

    predictions_gbm = pd.DataFrame(y_test)

    time_windows = [3, 5]

    for time in time_windows:
        # making predictions
        predictions_gbm['lower'] = gbm.predict(X_test)-time
        predictions_gbm['prediction'] = gbm.predict(X_test)
        predictions_gbm['upper'] = gbm.predict(X_test)+time

        predictions_gbm['in'] = predictions_gbm['taxi_out']\
            .between(predictions_gbm['lower'], predictions_gbm['upper'])

        acc = round(sum(predictions_gbm['in']) / len(predictions_gbm) * 100, 2)

        print('Accuracy for a time-window of', time, 'min:', acc, '%')

    return model
