import unittest
import util.play_time as time
import util.scoring as scoring
from test.test_helpers import load_data_from_file


class TestPlayTimeFromGameStart(unittest.TestCase):

    def test_play_time_from_game_start_2019_1(self):
        data = load_data_from_file("2019-1.json")
        scoring_plays = scoring.load_scoring_plays(data)
        self.assertEqual(1, scoring_plays[0]["about"]["period"],
                         "Invalid period for 0th scoring play!")
        self.assertEqual("00:25", scoring_plays[0]["about"]["periodTime"],
                         "Invalid periodTime for 0th scoring play!")

        self.assertEqual("00:25", time.get_play_time_from_game_start(scoring_plays[0]),
                         "Invalid time from game start for 0th scoring play!")


        self.assertEqual(2, scoring_plays[4]["about"]["period"],
                         "Invalid period for 4th scoring play!")
        self.assertEqual("08:02", scoring_plays[4]["about"]["periodTime"],
                         "Invalid periodTime for 4th scoring play!")

        self.assertEqual("28:02", time.get_play_time_from_game_start(scoring_plays[4]),
                         "Invalid time from game start for 4th scoring play!")


        self.assertEqual(3, scoring_plays[7]["about"]["period"],
                         "Invalid period for 7th scoring play!")
        self.assertEqual("17:45", scoring_plays[7]["about"]["periodTime"],
                         "Invalid periodTime for 7th scoring play!")

        self.assertEqual("57:45", time.get_play_time_from_game_start(scoring_plays[7]),
                         "Invalid time from game start for 7th scoring play!")


if __name__ == '__main__':
    unittest.main()