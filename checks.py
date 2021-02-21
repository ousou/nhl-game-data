import util.data as data
import util.scoring as scoring
import util.play_time as play_time_u


def home_lead(score):
    return score["home"] - score["away"]




def recover_from_deficit(play_time, deficit, season):
    deficit_count = 0
    recover_count = 0
    for game_no in range(1, data.game_count(season) + 1):
        game_data = data.load_data_from_file(game_no, season)
        scoring_plays = scoring.load_scoring_plays(game_data)
        lead_at_time = home_lead(scoring.get_score_at_time(scoring_plays, play_time))
        if lead_at_time == deficit or -lead_at_time == deficit:
            deficit_count += 1
            lead_at_end = home_lead(scoring.get_score_at_time(scoring_plays, "60:00"))
            if lead_at_end == 0 or (lead_at_end < 0 and lead_at_time > 0) \
                or (lead_at_end > 0 and lead_at_time < 0):
                recover_count += 1

    return deficit_count, recover_count


if __name__ == '__main__':
    deficit_count_1, recover_count_1 = recover_from_deficit("55:00", 2, 2017)
    deficit_count_2, recover_count_2 = recover_from_deficit("55:00", 2, 2018)
    print("deficit_count", deficit_count_1 + deficit_count_2)
    print("recover_count", recover_count_1 + recover_count_2)
