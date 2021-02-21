def load_scoring_plays(data):
    play_data = data["liveData"]["plays"]
    return [play_data["allPlays"][i] for i in play_data["scoringPlays"]]