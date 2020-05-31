import json
import re
import ast
import numpy as np

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

def split_credits_column(df):
    df["cast"] = df["credits"].apply(lambda x: string_to_dictionary(x, "cast"))
    df["crew"] = df["credits"].apply(lambda x: string_to_dictionary(x, "crew"))
    df.drop("credits", axis=1, inplace=True)

def from_json_to_array(df, column, regex):
    df[column] = df[column].apply(lambda x: re.findall(rf"{regex}", str(x)))

# Private functions
def string_to_dictionary(data, key):
    if data and (data == data):
        json_string = ast.literal_eval(data)
        json_dump = json.dumps(json_string)
        json_loaded = json.loads(json_dump)
        return json_loaded[key]
    else:
        return np.NaN
