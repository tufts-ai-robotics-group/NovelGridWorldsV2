import unittest
import numpy as np 
import gym
import pathlib
import json

from gym_novel_gridworlds2.envs.sequential import NovelGridWorldSequentialEnv
from gym_novel_gridworlds2.utils.json_parser import ConfigParser
from gym_novel_gridworlds2.utils.novelty_injection import inject_novelty

class NoveltyInjectTests(unittest.TestCase):
    def setUp(self):
        self.json_parser = ConfigParser()
        config_file_path = pathlib.Path(__file__).parent.resolve() / \
            "injectiontest.json"
        with open(config_file_path, "r") as f:
            self.config_content = json.load(f)
        self.env = NovelGridWorldSequentialEnv(config_dict=self.config_content)

    def test_inject_config(self):
        novelty = self.config_content['novelties']['100']
        print(novelty)
        new_config = inject_novelty(self.config_content, novelty)

        # new stuff in
        self.assertIn("jump", new_config['actions'])
        self.assertEqual(new_config['actions']['jump'], novelty['actions']['jump'])

        # old stuff still there
        self.assertIn("rotate_left", new_config['actions'])
        self.assertEqual(new_config['actions']['rotate_left'], 
            self.config_content['actions']['rotate_left'])
        self.assertIn("jump", new_config['action_sets']['main'])
