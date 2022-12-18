import unittest
from src.fmover import interpreter


class InterpreterTest(unittest.TestCase):

    def setUp(self):
        move_config = {'WHERE_FROM': {'wiki': 'Users/Peter/Library'},
                       'NAME': {'China': 'Users/Peter'},
                       'FILE_EXTENSION': {'.zip': 'Users/Peter/Home'}}
        file_props = {'WHERE_FROM': 'wikipedia', 'NAME': 'China', 'FILE_EXTENSION': '.html'}
        self.interpreter = interpreter.Interpreter(file_props, move_config, [])

    def test_parse_command_returns_correct_path(self):
        self.interpreter.commands = [{'WHERE_FROM(wiki) & NAME(China):': 'WHERE_FROM(wiki)'}]
        self.assertIs('Users/Peter/Library', self.interpreter.parse_command())

        self.interpreter.commands = [{'WHERE_FROM(uni) & NAME(China):': 'WHERE_FROM(wiki)'},
                                     {'WHERE_FROM(wiki) & NAME(China):': 'WHERE_FROM(wiki)'}]
        self.assertIs('Users/Peter/Library', self.interpreter.parse_command())

        self.interpreter.commands = [{'WHERE_FROM(uni) & NAME(China):': 'WHERE_FROM(wiki)'}]
        self.assertIs(None, self.interpreter.parse_command())

    def test_parse_command_handles_ambiguity_correctly(self):
        self.interpreter.config = {'WHERE_FROM': {'wikipedia': 'Users/Peter/Library', 'wiki': 'Users/Peter/Documents'},
                                   'NAME': {'China': 'Users/Peter'},
                                   'FILE_EXTENSION': {'.zip': 'Users/Peter/Home'}}
        self.interpreter.commands = [{'WHERE_FROM(*) & NAME(China):': 'WHERE_FROM(*)'}]
        self.assertIs('Users/Peter/Library', self.interpreter.parse_command())

    def test_parse_command_returns_correct_path_when_file_extension_is_not_in_config(self):
        self.interpreter.config = {'WHERE_FROM': {'wiki': 'Users/Peter/Library'},
                                   'NAME': {'China': 'Users/Peter'}}
        self.interpreter.commands = [{'WHERE_FROM(wiki) & NAME(China):': 'WHERE_FROM(wiki)'}]
        self.assertIs('Users/Peter/Library', self.interpreter.parse_command())


if __name__ == '__main__':
    unittest.main()
