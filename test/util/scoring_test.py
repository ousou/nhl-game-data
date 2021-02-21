import unittest
import json
import util.scoring as scoring


def load_data_from_file(file_name):
    with open("test/data/" + file_name, "r") as f:
        return json.loads(f.read())


class TestScoringPlays(unittest.TestCase):

    def test_scoring_plays_2019_1(self):
        data = load_data_from_file("2019-1.json")
        scoring_plays = scoring.load_scoring_plays(data)
        self.assertEqual(8, len(scoring_plays), "Invalid amount of scoring plays!")
        for s in scoring_plays:
            self.assertEqual("Goal", s["result"]["event"], "Returned other than scoring play!")
        self.assertEqual(1, scoring_plays[0]["about"]["period"],
                         "Invalid period for 0th scoring play!")
        self.assertEqual("00:25", scoring_plays[0]["about"]["periodTime"],
                         "Invalid periodTime for 0th scoring play!")

        self.assertEqual("Brady Tkachuk", scoring_plays[0]["players"][0]["player"]["fullName"],
                         "Invalid scorer for 0th scoring play!")

        self.assertEqual(3, scoring_plays[7]["about"]["period"],
                         "Invalid period for 7th scoring play!")
        self.assertEqual("17:45", scoring_plays[7]["about"]["periodTime"],
                         "Invalid periodTime for 7th scoring play!")

        self.assertEqual("Bobby Ryan", scoring_plays[7]["players"][0]["player"]["fullName"],
                         "Invalid scorer for 7th scoring play!")

if __name__ == '__main__':
    unittest.main()