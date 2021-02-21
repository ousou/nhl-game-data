import util.data as data
import util.scoring as scoring
import concurrent.futures
from functools import partial
import os


def home_lead(score):
    return score["home"] - score["away"]


def _recover_from_deficit_in_game(season, deficit, play_time, game_no):
    game_data = data.load_data_from_file(game_no, season)
    deficit_count = 0
    recover_count = 0
    scoring_plays = scoring.load_scoring_plays(game_data)
    lead_at_time = home_lead(scoring.get_score_at_time(scoring_plays, play_time))
    if lead_at_time == deficit or -lead_at_time == deficit:
        deficit_count += 1
        lead_at_end = home_lead(scoring.get_score_at_time(scoring_plays, "60:00"))
        if lead_at_end == 0 or (lead_at_end < 0 and lead_at_time > 0) \
                or (lead_at_end > 0 and lead_at_time < 0):
            recover_count += 1

    return deficit_count, recover_count


def recover_from_deficit(play_time, deficit, season):
    deficit_count = 0
    recover_count = 0
    with concurrent.futures.ProcessPoolExecutor(max_workers=os.cpu_count() - 1) as executor:
        results = executor.map(partial(_recover_from_deficit_in_game,
            season,
            deficit,
            play_time), range(1, data.game_count(season) + 1))
        for d_c, r_c in results:
            deficit_count += d_c
            recover_count += r_c

    return deficit_count, recover_count


if __name__ == '__main__':
    goal_deficit = [1, 2, 3]
    play_time = ["40:00", "45:00", "50:00", "55:00", "57:30", "59:00", "59:30", "59:50"]
    years = [2013, 2014, 2015, 2016, 2017, 2018]
    for g in goal_deficit:
        for p in play_time:
            deficit_count = 0
            recover_count = 0
            for y in years:
                deficit_count_1, recover_count_1 = recover_from_deficit(p, g, y)
                deficit_count += deficit_count_1
                recover_count += recover_count_1
            print("goal_deficit", g)
            print("play_time", p)
            print("deficit_count", deficit_count)
            print("recover_count", recover_count)
            print("Recover perc %.2f" % ((recover_count / deficit_count)*100))
            print("-------------")
