import json


def load_data_from_file(file_name):
    with open("test/data/" + file_name, "r") as f:
        return json.loads(f.read())