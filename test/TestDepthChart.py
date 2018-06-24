import unittest
import depth_chart
import os, pickle


class TestDepthChart(unittest.TestCase):
    def test_populate_teams_dict(self):
        os.chdir(os.path.join(os.pardir, "fantasy-football"))
        depth_chart.populate_teams_dict()
        with open("team_dict.pickle", "rb") as file:
            team_dict=pickle.load(file)
        self.assertDictEqual(depth_chart.team_dict, team_dict)

    def test_populate_exception_dict(self):
        depth_chart.populate_exception_dict()
        with open("exception_dict.pickle", "rb") as file:
            exception_dict=pickle.load(file)
        self.assertDictEqual(exception_dict, depth_chart.exception_dict)