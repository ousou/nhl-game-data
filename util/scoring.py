import util.play_time as pt


def load_scoring_plays(data):
    play_data = data["liveData"]["plays"]
    return [play_data["allPlays"][i] for i in play_data["scoringPlays"]]


def get_score_at_time(scoring_plays, play_time):
    home_score = 0
    away_score = 0
    for p in scoring_plays:
        t = pt.get_play_time_from_game_start(p)
        if t <= play_time:
            home_score = p["about"]["goals"]["home"]
            away_score = p["about"]["goals"]["away"]
        else:
            break

    return {"home": home_score,
            "away": away_score}