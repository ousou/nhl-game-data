import gzip
import json

def game_count(season):
    if season >= 2017:
        return 1271
    else:
        return 1230


def load_data_from_file(game_no, season):
    with gzip.open("data/" + str(season) + "/" + str(game_no) + ".json.gz", "r") as f:
        s = f.read().decode("utf-8")
        return json.loads(s)