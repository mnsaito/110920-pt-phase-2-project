# King County Home Price Analysis

A client in King County, WA would like to advise homeowners regarding home improvement projects that will add to the sale price of their homes.  To accomplish this task, I created a model to evaluate how various features will affect the sale price of a home.  I ran a number of model iterations to identify a baseline model that best explains the variance in sale price.  I then used this model to help explain how various home improvement projects may affect the sale price.

## This Repository

### Repository Directory

```
├── README.md        <-- Main README file explaining the project's business case,
│                        methodology, and findings
│
├── data             <-- Data in CSV format
│   ├── processed    <-- Processed (combined, cleaned) data used for modeling
│   └── raw          <-- Original (immutable) data dump
│
├── notebooks        <-- Jupyter Notebooks for exploration and presentation
│   ├── exploratory  <-- Unpolished exploratory data analysis (EDA) notebooks
│   └── report       <-- Polished final notebook(s)
│
├── references       <-- Data dictionaries, manuals, and project instructions
│
├── reports          <-- Generated analysis (including presentation.pdf)
│   └── figures      <-- Generated graphics and figures to be used in reporting
│
└── src              <-- Relevant source code
```

### Quick Links

1. [Final Analysis Notebook](notebooks/report/final_notebook.ipynb)
2. [Presentation Slides](reports/presentation.pdf)

### Setup Instructions

To create a replica of the environment needed to run my notebook, from the project folder, run: 

conda env create --file environment.yml

## Business Understanding

The client would like us to investigate various home improvement projects to determine whether they will increase the sale value of a home.  The improvements I considered in my housing analysis are:
 - Whether adding an open porch, an enclosed porch, or both an open and an enclosed porch will increase the sale price of a home
 - Whether upgrading to a forced-air heating system will increase the sale price of a home
 - Whether converting an attached garage into a bedroom will increase the sale price of a home

## Data Understanding

I used three datasets from the King County Department of Assessments for my analysis:
 - Real Property Sales Records, which includes property sales information between 2015 and 2020
 - Residential Building Records, which includes descriptions for each residential building
 - Parcel Records, which includes the details for each parcel of real property
 
A [data dictionary](references/King_County_Home_Sales_Data_Dictionary.pdf) describes the data within each of the datasets, and a "Look Up" table explains the meaning of many of the attributes included in the datasets.

The [correlation matrix](reports/figures/heatmap.png) indicates that the square footage of the total living space is highly correlated to the sale price, and that the square footage of the lot size is most negatively correlated to the sale price.  The correlation matrix also indicates that year built is negatively correlated to sale price, but it appears to be positively correlated with total living space.  Accordingly, if total living space is included in the base model, it is unlikely that year built will also be included in the model.

Because the [histograms for the sale price and living space square footage](reports/figures/histogram_pretransform.png) are skewed to the right, I [transformed the data](reports/figures/histogram_transformed.png) using both log transform and square root, and evaluated both the original data and the transformed data to derive my base model.

The [porch data box plot](reports/figures/porch_box.png), [heating system box plot](reports/figures/forced_air_box.png), and [renovated garage data box plot](reports/figures/garage_box.png) do not indicate that there is a substantial difference between the categorical groups in terms of their spread and where the means fall.  Based on this information, it is unclear whether these features will be sufficient to explain the difference in sale price.
 

## Data Preparation

I removed entries that did not relate to residential properties

I also removed entries with very low or very high outliers for sale price, very low outliers for living space square footage, and entries with high sales price with low square footage or low sales price with high square footage

To analyze the effect of adding a porch (whether open, enclosed or both), I used the information on square footage of open porches and enclosed porches to categorize the porch data as open, enclosed, both or none.  I then used one hot encoding, dropped the "no porch" option, and fed the data into my model.

To analyze the effect of upgrading to a forced-air heating system, I replaced the codes for the heat systems to identify those that are forced-air versus all others.  I then used label encoder and fed the data into my model.

To analyze the effect of converting an attached garage into a bedroom, I categorized all properties with an attached garage, and determined the number of bedrooms for those properties.  I categorized properties that did not have an attached garage and included an additional bedroom (compared to those with an attached garage) as renovated.  I then used label encoder and fed the data into my model.


## Modeling

After running a number of iterations, I chose to use square root of the sale price, square root of the living space, and square root of the lot size as my base model.  My final base model is: 

&radic;<SPAN STYLE="text-decoration:overline">sale price</SPAN> = 137.87 + 15.55 * &radic;<SPAN STYLE="text-decoration:overline">living space</SPAN> - 0.14 * &radic<SPAN STYLE="text-decoration:overline">lot size</SPAN>


## Evaluation

For my base model, R-squared is 0.387, so the model only explains 38.7% of the variance in Sale Price

The overall p-value is 0.00, so the model is statistically significant at an alpha of 0.05

In this case, it is unclear what the intercept represents (since it is a property with 0 square feet of living space and a 0 square foot lot) but that property is expected to sell for \$19,007
 - Note: since the model uses the square root of the sale price, the intercept was squared to determine this value
 
Each additional square footage of living space is expected to increase the sale price by \$242 

Each additional square footage of lot space is expected to increase the sale price by \$0.02

p-values for intercept and coefficients are significant at an alpha of 0.05.  Thus, this model finds that the relationship between sale price, living space and lot size is significant

### Assumptions of Linear Regression:
***Linearity***
The null hypothesis is that the model is linearly predicted by the features.  The alternative hypothesis is that it is not.  My base model returned a high Rainbow p-value.  Thus, my base model does not violate the linearity assumption

***Normality***
The null hypothesis is that the residuals are normally distributed.  The alternative hypothesis is that they are not.  My model returned a p-value of 0 under the Jarque-Bera test.  Thus, my model violates the normality assumption.

***Homoscadasticity***
The null hypothesis is homoscedasticity.  The alternative hypothesis is heteroscedasticity.  My model returned a low F-statistic p-value.  Thus, my model violates the homoscedasticity assumption.

***Independence***
The VIFs in my model are less than 5, so it is reasonable to say that it does not violate the independence assumption (i.e., the features are not too colinear).

Because my base model violates both the normality and the homoscadasticity assumptions, there appears to be a link between the independent variables and the error term.  In other words, there is likely a feature missing from the model, which should be investigated further.

## Conclusion

Based on my analysis:
 - The addition of an open porch is expected to increase the sale price of a home by \$23
 - The addition of an enclosed porch is expected to increase the sale price of a home by \$1826
 - The addition of both an open porch and an enclosed porch is expected to increase the sale price of a home by \$4972
 - The conversion of a heating system to forced-air is expected to decrease the sale price of a home by \$2427
 - The conversion of an attached garage to a bedroom is expected to increase the sale price of a home by \$6256
 
I provide the following recommendations to the client:
 - The conversion of an attached garage to a bedroom is expected to increase the sale price by \$6256, so I recommend the client consider this renovation.
 - Both the addition of an enclosed porch, or the addition of both an enclosed porch and an open porch is expected to increase the sale price of a home by \$1826 and \$4972, respectively, so I recommend the client consider these renovations.
 - Although the addition of an open porch is expected to increase the sale price of a home, according to my model, it will only increase the sale price by \$23, which is likely to be less than the cost of adding an open porch.  Thus, I do not recommend adding an open porch to increase the sale price of a home.
 - The conversion to a forced-air heating system is expected to decrease the sale price of a home, so I do not recommend this renovation.
 
### Next Steps
 - As discussed in my Final Analysis Notebook, some anomolies were identified in the models that need to be investigated further
 - If the client has a specific property in mind, I recommend that we target our analysis based on the specific property
     - For example, neighborhoods appear to have a significant effect on the sale price, so I recommend that the sale price be evaluated based on the neighborhood in which the property is located
     - If the property already includes an open porch, I recommend considering the effect of converting the open porch into an enclosed porch
 - I also recommend investigating the cost for the renovation to determine whether it is worth the investment
