# Movie Release Predictor 📽🍿🎬

![Python application](https://github.com/sideround/predict-revenue-new-releases/workflows/Python%20application/badge.svg)

Isaac Rodriguez

Data Part-Time, Barcelona, Dec 19

<img src="https://bit.ly/2VnXWr2" alt="Ironhack Logo" width="100"/>

# Welcome

This repository project contains my final project for Ironhack. I am predicting if a new release (movie) is going to succeed or not and how much is revenue going to be.

# Approach

Our main structure was to follow these key subjects:

- Data Engineering (To build the dataset)
- Data Analytics (Correlations, get insights, discover not obvious patterns)
- Machine Learning (Train and predict)

# Folder structure

```
  .
  ├── notebooks                                 # (Contains all notebooks to run the project)
  │   ├── 1.Dataset_Builder.ipynb               # Runs and builds the dataset
  │   ├── 2.1.Pre_transformation.ipynb          # Pre-transforms the dataset. JSON -> Array     
  │   ├── 2.2.People_Pre_Transformation.ipynb   # Creates People dataset, by id and year. 
  │   ├── 3.EDA.ipynb                           # Visualize and insights from dataset.
  │   ├── 4.Data_Wrangling.ipynb                # Feature Selection and Feature Engineering
  │   ├── 5.1.Model_Classification.ipynb        # Supervised Learning - Classification
  │   └── 5.2.Model_Regression.ipynb            # Supervised Learning - Regression
  ├── source                      # (Contains all python scripts)      
  │   ├── config.py               # Contains the TMDB API Key
  │   ├── constants.py            # Constants  
  │   ├── constants.py            # Helpers scripts as visualizing confusion matrix, encoding...  
  │   ├── tmdb_retriever.py       # Script to retrieve convert imdb id to tmdb one.  
  │   ├── tmdb_movies.py          # Script to retrieve all movies from a tmdb id.
  │   └── tmdb_people.py          # Script to retrieve all people from a tmdb id. 
  └── data
      ├── pre-processed               # (Contains al pre-processed csv)
      │   └── title_basics.tsv        # IMDB Interface
      └── processed                 # (Contains all processed csv)
          ├── json                  # All outputs from our scripts 
          ├── dataset_builder       # Final dataset output csv
          ├── modeling              # CSV used for modeling
          ├── people_transformation # CSV used for people transformation
          └── transformation        # CSV used for transformation  
```

# Pre-conditions

- To successfully run our python scripts, you should get a [TMDB API KEY](https://www.themoviedb.org/documentation/api) and then put it over `../source/config.py`. 
- You should be aware that running the project from scratch (including getting the dataset) takes between 4 - 5 hours. In case you only want to run the models, contact me and I will provide you the dataset (as it's too big to be included here).
- Tests runs automatically when you push to master.

# Problems to solve

- Is a new movie release going to succeed? We assume movie success when the vote average is superior to 8.0.
- How much will the movie revenue going to be?

# Dataset

We did not discover any dataset which satisfies our standards, so I decided to code my own. Here is the plan:

- Get an interface of Imdb dataset: http://www.imdb.com/interfaces
- Use https://www.themoviedb.org/documentation/api to build the final dataset.

# Cleaning

We can split our cleaning between two datasets we created, movies and people.

**Movies**: Our movies dataset contained JSON values which needed to be transformed to array. We did this transformation on `genres`, `production_companies`, `production_countries`, `spoken_languages`, `cast` and `crew`. 

**People**: Our people dataset was modeled to visualize for each cast member the mean of movies made (value) by year (column). We transformed, melt, grouped by and pivoted our initial dataset to get our desired one.

# Analysis

When we analyzed our data we wanted to make sure our budget was up to date from inflaction point of view. $1 in 1980 is $3.11 now. Also removed NaNs, mantained the distribution for `runtime`, convert from object the correct dtype (boolean, numeric).

# Model Training and Evaluation

We here got two different type of algorithms. Classification and Regression.

**Classification**:

We trained our dataset with the following models: 

- LogisticRegression
- KNeighborsClassifier
- DecisionTreeClassifier
- RandomForestClassifier

Before evaluating our model, we wanted to select the one with lowest number of False Positives. Imagine if a company invests on a movie which turns out it's not a success. Waste of money!

The one with lowest FP was **RandomForestClassifier**

**Regression**:

We trained our dataset with the following models: 

- LinearRegression
- ElasticNet
- Lasso 
- RandomForestRegressor
- XGBRegressor

Before evaluating our model we wanted to select the one with highet r2_score and lowest STD value. 

The one with these metrics was **XGBRegressor** by far!

# Conclusion


# Links

[Slides](https://drive.google.com/file/d/1x8zbtqVa8g73yLTOwFXDrr5NSRB9bXQ2/view)  
