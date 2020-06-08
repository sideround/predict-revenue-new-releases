import json
import re
import ast
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split, GridSearchCV, StratifiedKFold, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, log_loss
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.metrics import r2_score
from sklearn.model_selection import cross_val_score

people_path = pd.read_csv("../data/processed/people_transformation/people_cast_list.csv")


## 1.Dataset Builder

def convert_output_id(output):
    data = []
    for i in range(0, len(output)):
        if isinstance(output[i], dict):
            if len(output[i]["movie_results"]) >= 1:
                data.append(output[i]["movie_results"][0]["id"])
    return data

def get_transformed_json(path):
    id_remove = []
    json_final = []
    with open(path) as json_file:
        data = json.load(json_file)
        for i in range(0, len(data)):
            if data[i] == "<class 'requests.exceptions.ReadTimeout'>":
                id_remove.append(i)
            elif data[i] == "<class 'requests.exceptions.ConnectionError'>":
                id_remove.append(i)
            else:
                json_final.append(data[i])
    return json_final

## 2.1 Pre_transformation

def from_json_to_array(df, column, regex):
    df[column] = df[column].apply(lambda x: re.findall(rf"{regex}", str(x)))

def split_credits_column(df):
    df["cast"] = df["credits"].apply(lambda x: string_to_dictionary(x, "cast"))
    df["crew"] = df["credits"].apply(lambda x: string_to_dictionary(x, "crew"))
    df.drop("credits", axis=1, inplace=True)

## 2.2 People Pre Pre_transformation

def unique_values(df_list):
    ids_list = [re.findall(r'\b\d+\b', value) for value in df_list]
    return set(flatten(ids_list))

## 4 Data Wrangling

def create_new_columns(df, column):
    value_list = []
    for cell in df[column]:
        lista_genres = re.findall(r'\b\w+\b', cell)
        for value in lista_genres:
            value_list.append(value)
    v = get_value_counts(value_list)
    columns_to_zero(df, v, column)
    validate_column(df, column)

def get_average_people(df, df_list, year):
    ids_list = [re.findall(r'\b\d+\b', value) for value in df_list]
    for i in range(len(df_list)):
        df.loc[i, "cast"] = np.mean(get_score(ids_list[i], year[i]))

## Modeling

def predict(model, X_train, y_train, X_test, y_test, model_text):

    model.fit(X_train, y_train)

    y_pred_test = model.predict(X_test)

    cf_matrix = confusion_matrix(y_test, y_pred_test)
    plot_confusion_matrix(cf_matrix, model_text)
    return baseline_report(model, X_train, X_test, y_train, y_test, model_text)

def predict_linear(model, X_test,  X_train, y_train, X, y, model_text):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    score = r2_score(y_train, y_pred)

    scores = cross_val_score(model,
                             X_train,
                             y_train,
                             cv=5,
                             scoring='r2')

    print('CV Mean: ', np.mean(scores))
    print('STD: ', np.std(scores))

    fig, ax = plt.subplots()
    ax.scatter(y_train, y_pred)
    ax.plot([y.min(), y.max()], [y.min(), y.max()], 'k--', lw=4)
    ax.set_xlabel('Predicted revenue')
    ax.set_ylabel('Predicted revenue')
    plt.title('Measured versus predicted revenue')
    plt.savefig(f"../data/exports/{model_text}_regression_scatter.png")
    plt.show()

# Private functions

## Generics
def isNaN(num):
    return num == num

flatten = lambda l: [item for sublist in l for item in sublist]

def string_to_dictionary(data, key):
    if data and (data == data):
        json_string = ast.literal_eval(data)
        json_dump = json.dumps(json_string)
        json_loaded = json.loads(json_dump)
        return json_loaded[key]
    else:
        return np.NaN

## Encode our categorical values
def get_value_counts(list):
    d = {}
    for name in list:
        d[name.lower()] = d.get(name.lower(), 0) + 1
    sorted_list = dict(sorted(d.items(), key=lambda kv: kv[1], reverse=True))
    return sorted_list

def columns_to_zero(df, sorted_list, column):
    iterator = iter(sorted_list.items())
    for i in range(len(sorted_list)):
        name_column = f"{column}_{list(sorted_list)[i]}"
        df[name_column] = 0
        next(iterator)

def validate_column(df, column):
    for i, j in df.iterrows():
        lista_genres = re.findall(r'\b\w+\b', j[column])
        for value in lista_genres:
            name_column = f"{column}_{value.lower()}"
            df.loc[i, name_column] = 1

## Retrieve average cast value from df
def get_score(ids, year):
    values = []
    for id_ in ids:
        dict_people = people_path[people_path["tmdb_id"] == int(id_)].to_dict('r')
        if len(dict_people) > 0:
            values.append(get_mean_value(get_values_people(dict_people, year)))
    return values

def get_mean_value(array):
    try:
        mean_value = sum(array) / len(array)
    except ZeroDivisionError:
        mean_value = 0
    return mean_value

def get_values_people(dictionary, year):
    values = []
    for i,k in dictionary[0].items():
        if i != "tmdb_id":
            if '{0:g}'.format(float(i)) == str(year):
                if isNaN(k):
                    values.append(k)
                return values
            else:
                if isNaN(k):
                    values.append(k)

## Model visualization

def plot_confusion_matrix(cf_matrix, model_text):
    group_names = ["True Neg", "False Pos", "False Neg", "True Pos"]
    group_counts = ["{0:0.0f}".format(value) for value in cf_matrix.flatten()]
    group_percentages = ["{0:.2%}".format(value) for value in
                     cf_matrix.flatten()/np.sum(cf_matrix)]
    labels = [f"{v1}\n{v2}\n{v3}" for v1, v2, v3 in zip(group_names,group_counts,group_percentages)]
    labels = np.asarray(labels).reshape(2,2)
    sns_heatmap = sns.heatmap(cf_matrix, annot=labels, fmt="", cmap='Blues')
    sns_heatmap.figure.savefig(f"../data/exports/{model_text}_classification_heatmap.png")

def baseline_report(model, X_train, X_test, y_train, y_test, name):
    """
    The function takes the model, the split data and the name and returns the dataframe with
    the scores of the models with training and test data.
    """
    strat_k_fold = StratifiedKFold(n_splits=5, shuffle=True)
    model.fit(X_train, y_train)
    accuracy     = np.mean(cross_val_score(model, X_train, y_train, cv=strat_k_fold, scoring='accuracy'))
    precision    = np.mean(cross_val_score(model, X_train, y_train, cv=strat_k_fold, scoring='precision'))
    recall       = np.mean(cross_val_score(model, X_train, y_train, cv=strat_k_fold, scoring='recall'))
    f1score      = np.mean(cross_val_score(model, X_train, y_train, cv=strat_k_fold, scoring='f1'))
    rocauc       = np.mean(cross_val_score(model, X_train, y_train, cv=strat_k_fold, scoring='roc_auc'))
    y_pred_train = model.predict(X_train)
    logloss      = log_loss(y_train, y_pred_train)

    df_model_train = pd.DataFrame({'data'        : 'training',
                             'model'        : [name],
                             'accuracy'     : [accuracy],
                             'precision'    : [precision],
                             'recall'       : [recall],
                             'f1score'      : [f1score],
                             'rocauc'       : [rocauc],
                             'logloss'      : [logloss]})

    accuracy     = np.mean(cross_val_score(model, X_test, y_test, cv=strat_k_fold, scoring='accuracy'))
    precision    = np.mean(cross_val_score(model, X_test, y_test, cv=strat_k_fold, scoring='precision'))
    recall       = np.mean(cross_val_score(model, X_test, y_test, cv=strat_k_fold, scoring='recall'))
    f1score      = np.mean(cross_val_score(model, X_test, y_test, cv=strat_k_fold, scoring='f1'))
    rocauc       = np.mean(cross_val_score(model, X_test, y_test, cv=strat_k_fold, scoring='roc_auc'))
    y_pred_test = model.predict(X_test)
    logloss      = log_loss(y_test, y_pred_test)   # SVC & LinearSVC unable to use cvs

    df_model_test = pd.DataFrame({'data'        : 'test',
                             'model'        : [name],
                             'accuracy'     : [accuracy],
                             'precision'    : [precision],
                             'recall'       : [recall],
                             'f1score'      : [f1score],
                             'rocauc'       : [rocauc],
                             'logloss'      : [logloss]})   # timetaken: to be used for comparison later

    df_model = pd.concat([df_model_train, df_model_test], ignore_index=True)

    return df_model
