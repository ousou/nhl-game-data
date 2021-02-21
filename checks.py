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
    deficit_count_1, recover_count_1 = recover_from_deficit("55:00", 2, 2017)
    deficit_count_2, recover_count_2 = recover_from_deficit("55:00", 2, 2018)
    print("deficit_count", deficit_count_1 + deficit_count_2)
    print("recover_count", recover_count_1 + recover_count_2)
    print("Recover perc %.2f" % (((recover_count_1 + recover_count_2)
                                 / (deficit_count_1 + deficit_count_2))* 100))
