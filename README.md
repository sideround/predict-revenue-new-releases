# Movie Release Predictor 📽🍿🎬

![Python application](https://github.com/sideround/predict-revenue-new-releases/workflows/Python%20application/badge.svg)

Isaac Rodriguez

Data Part-Time , Barcelona, Dec 19

<img src="https://bit.ly/2VnXWr2" alt="Ironhack Logo" width="100"/>

# Welcome

This repository project contains my final project for Ironhack. I am predicting if a new release (movie) is going to succeed or not and how much is going to make in total.

# Project structure

  .
  ├── notebooks             
  │   ├── 1.Dataset_Builder.ipynb               # Table of contents     
  │   ├── 2.1.Pre_transformation.ipynb          # Table of contents      
  │   ├── 2.2.People_Pre_Transformation.ipynb   # Table of contents   
  │   ├── 3.EDA.ipynb                           # Table of contents  
  │   ├── 4.Data_Wrangling.ipynb                # Table of contents  
  │   ├── 5.1.Model_Classification.ipynb        # Table of contents  
  │   └── 5.2.Model_Regression.ipynb            # Table of contents  
  ├── source                  
  │   ├── config.py               # Table of contents
  │   ├── constants.py            # Table of contents  
  │   ├── imdb_retriever.py       # Table of contents  
  │   ├── tmdb_movies.py          # Table of contents  
  │   └── tmdb_retriever.py       # Table of contents  
  └── data
      ├── pre-processed               # Table of contents
      │   └── title_basics.tsv               # Table of contents
      └── processed               # Table of contents
          ├── json
          ├── dataset_builder
          ├── modeling                # Table of contents  
          ├── people_transformation          # Table of contents  
          └── transformation          # Table of contents  

# Problems to solve

- Is a new movie release going to succeed? We assume movie success when the vote average is superior to 8.0.
- How much is the movie going to make?

# Dataset

We did not discover any dataset which satisfies our standards, so I decided to code my own. Here is the plan:

- Get an interface of Imdb dataset: http://www.imdb.com/interfaces
- Use https://www.themoviedb.org/documentation/api to build the final dataset.

# Cleaning

# Analysis

# Model Training and Evaluation

# Conclusion

# Links

[Slides](https://drive.google.com/file/d/1x8zbtqVa8g73yLTOwFXDrr5NSRB9bXQ2/view)  
