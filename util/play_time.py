def get_play_time_from_game_start(play):
    period_minutes, period_seconds = [int(p) for p in play["about"]["periodTime"].split(":")]
    period = play["about"]["period"]

    period_minutes += (period - 1) * 20

    return str(period_minutes).zfill(2) + ":" + str(period_seconds).zfill(2)