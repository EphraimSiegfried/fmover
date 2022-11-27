from unittest import TestCase

from src.fmover.config import MoveConfig


class TestMoveConfig(TestCase):

    def test_validate_config_returns_true(self):
        config = {'COMMAND': [{'WHERE_FROM(wiki) & NAME(China)': 'WHERE_FROM(wiki)'}],
                    'WHERE_FROM': {'wiki': 'Users/Peter/Library'},
                    'NAME': {'China': 'Users/Peter'},
                    'FILE_EXTENSION': {'.zip': 'Users/Peter/Home'}}
        move_config = MoveConfig(config)
        self.assertTrue(move_config.validate_config())

    def test_validate_config_raises_value_exception_when_config_is_empty(self):
        config = {}
        move_config = MoveConfig(config)
        self.assertRaises(ValueError, move_config.validate_config)

    def test_validate_config_raises_value_exception_when_config_does_not_have_key_command(self):
        config = {'WHERE_FROM': {'wiki': 'Users/Peter/Library'},
                    'NAME': {'China': 'Users/Peter'},
                    'FILE_EXTENSION': {'.zip': 'Users/Peter/Home'}}
        move_config = MoveConfig(config)
        self.assertRaises(ValueError, move_config.validate_config)

    def test_validate_config_raises_value_exception_when_config_key_command_is_not_a_list(self):
        config = {'COMMAND': {'WHERE_FROM(wiki) & NAME(China)': 'WHERE_FROM(wiki)'},
                    'WHERE_FROM': {'wiki': 'Users/Peter/Library'},
                    'NAME': {'China': 'Users/Peter'},
                    'FILE_EXTENSION': {'.zip': 'Users/Peter/Home'}}
        move_config = MoveConfig(config)
        self.assertRaises(ValueError, move_config.validate_config)

    def test_validate_config_raises_value_exception_when_config_key_command_is_not_a_singleton_dictionary(self):
        config = {'COMMAND': [{'WHERE_FROM(wiki) & NAME(China)': 'WHERE_FROM(wiki)', 'FILE_EXTENSION(.zip) & NAME(China)': 'WHERE_FROM(wiki)'}],
                    'WHERE_FROM': {'wiki': 'Users/Peter/Library'},
                    'NAME': {'China': 'Users/Peter'},
                    'FILE_EXTENSION': {'.zip': 'Users/Peter/Home'}}
        move_config = MoveConfig(config)
        self.assertRaises(ValueError, move_config.validate_config)






