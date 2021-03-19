import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.diagnostic import linear_rainbow, het_breuschpagan
from statsmodels.stats.outliers_influence import variance_inflation_factor

from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import LabelEncoder

# Define Function to Create Model
def create_model(df, y, X):
    """df = dataframe with data
    y = target variable
    X = list of features
    Runs data through ols model and prints results.
    Also checks the assumptions of linear regression.
    Uses Rainbow test to check linearity.
    For independence, if there is more than one feature, will calculate the variance inflation factor for each feature.
    Runs the Breusch-Pagan test for homoscadasticity, and plots predicted life expectancy vs the residuals.  
     
    """
    model_df = df[[y, *X]]
    Formula = y + ' ~ ' + X[0]
    for i in range(len(X)-1):
        Formula += ' + '
        Formula += X[i+1]
    model = ols(formula = Formula, data = model_df)
    model_results = model.fit()
    print(model_results.summary())
       
    #Check Linearity
    rainbow_statistic, rainbow_p_value = linear_rainbow(model_results)
    print('\n\nCheck Assumptions of Linear Regression\n\nLinearity\nRainbow Statistic:', rainbow_statistic)
    print('Rainbow p-value:', rainbow_p_value)
    
    #Independence
    vif_df = pd.DataFrame()
    rows = model_df[X].values
    if len(X) != 1:
        vif_df['VIF'] = [variance_inflation_factor(rows, i) for i in range(len(X))]
        vif_df['feature'] = X
        print('\n\nIndependence\n', vif_df)

    # Homoscadasticity
    y = model_df[y]
    y_hat = model_results.predict()
    fig2, ax2 = plt.subplots()
    ax2.set(xlabel = 'Predicted Sale Price',
            ylabel = 'Residuals (Predicted - Actual Sale Price)')
    ax2.scatter(x=y_hat, y=y_hat-y, color='blue', alpha=0.2);
    
    lm, lm_p_value, fvalue, f_p_value = het_breuschpagan(y-y_hat, model_df[X])
    print('\n\nHomoscadasticity\nLagrange Multiplier p-value:', lm_p_value)
    print('F-statistic p-value:', f_p_value)
    
    return
