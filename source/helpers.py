import json

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
