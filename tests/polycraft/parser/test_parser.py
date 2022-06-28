import unittest
from gym_novel_gridworlds2.utils.json_parser import ConfigParser
import gym
from gym.utils.play import play
import pygame
import numpy as np
import pathlib


class ActionSpaceTests(unittest.TestCase):
    def setUp(self):
        self.json_parser = ConfigParser()

    def get_file_path(self, file_name):
        return pathlib.Path(__file__).parent.resolve() / file_name

    def test_map_size(self):
        file_name = "parser_test_basics.json"

        config_file_path = self.get_file_path(file_name)
        state, dynamic, entities = self.json_parser.parse_json(config_file_path)
        self.assertEqual(state._map.shape, (20, 30))

    def test_action(self):
        file_name = "parser_test_actions.json"

        config_file_path = self.get_file_path(file_name)
        state, dynamic, entities = self.json_parser.parse_json(config_file_path)

        self.assertEqual(len(dynamic.actions), 4)
        self.assertTrue("move_left" in dynamic.actions)
        self.assertEqual(dynamic.actions["move_left"].vec, (0, -1))

        self.assertTrue("move_up" in dynamic.actions)
        self.assertEqual(dynamic.actions["move_up"].vec, (-1, 0))

        self.assertTrue("move_down" in dynamic.actions)
        self.assertEqual(dynamic.actions["move_down"].vec, (1, 0))

        self.assertTrue("move_right" in dynamic.actions)
        self.assertEqual(dynamic.actions["move_right"].vec, (0, 1))

    def test_recipes(self):
        file_name = "parser_test_recipes.json"

        json_parser = ConfigParser()
        config_file_path = self.get_file_path(file_name)
        state, dynamic, entities = json_parser.parse_json(config_file_path)

        self.assertEqual(len(dynamic.actions), 3)
        self.assertTrue("craft_stick" in dynamic.actions)
        self.assertTrue("craft_plank" in dynamic.actions)
        self.assertTrue("craft_pogo_stick" in dynamic.actions)
