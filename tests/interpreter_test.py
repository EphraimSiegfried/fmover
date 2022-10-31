import unittest
from file_mover import interpreter


class InterpreterTest(unittest.TestCase):

    def setUp(self):
        move_config = {'WHERE_FROM': {'wiki': 'Users/Peter/Library'},
                       'NAME': {'China': 'Users/Peter'},
                       'FILE_EXTENSION': {'.zip': 'Users/Peter/Home'}}
        file_props = {'WHERE_FROM': 'wikipedia', 'NAME': 'China', 'FILE_EXTENSION': '.html'}
        self.interpreter = interpreter.Interpreter(file_props, move_config, {})

    def test_token_corresponds_with_WHERE_FROM_parameter_is_true_when_match(self):
        self.assertTrue(self.interpreter.token_corresponds("WHERE_FROM(wikipedia)"))
        self.assertTrue(self.interpreter.token_corresponds("WHERE_FROM(wiki)"))
        self.assertTrue(self.interpreter.token_corresponds("WHERE_FROM(*)"))

    def test_token_corresponds_with_WHERE_FROM_parameter_is_false_when_no_match(self):
        self.assertFalse(self.interpreter.token_corresponds("WHERE_FROM(wikiPEDIA)"))
        self.assertFalse(self.interpreter.token_corresponds("WHERE_FROM(wiki )"))
        self.assertFalse(self.interpreter.token_corresponds("WHERE_FROM(/*)"))

    def test_token_corresponds_with_different_parameters_is_true_when_match(self):
        self.assertTrue(self.interpreter.token_corresponds("NAME(China)"))
        self.assertTrue(self.interpreter.token_corresponds("FILE_EXTENSION(.html)"))
        self.assertTrue(self.interpreter.token_corresponds("FILE_EXTENSION(.)"))  # This might be a problem

    def test_antecedent_corresponds_is_true_when_all_tokens_are_true(self):
        self.assertTrue(self.interpreter.antecedent_corresponds("WHERE_FROM(wiki) & NAME(China)"))
        self.assertTrue(
            self.interpreter.antecedent_corresponds("WHERE_FROM(wiki) & NAME(China) & FILE_EXTENSION(.html)"))

    def test_antecedent_corresponds_is_false_when_there_is_false_token(self):
        self.assertFalse(self.interpreter.antecedent_corresponds("FILE_EXTENSION(*) & WHERE_FROM(wiki)"))
        self.assertFalse(self.interpreter.antecedent_corresponds("WHERE_FROM(China) & NAME(wiki)"))

    def test_get_corresponding_path_returns_the_given_path_in_config_of_given_token(self):
        self.assertIs('Users/Peter/Library', self.interpreter.get_corresponding_path("WHERE_FROM(wiki)"))
        self.assertIs('Users/Peter', self.interpreter.get_corresponding_path("NAME(*)"))
        self.assertIs(None, self.interpreter.get_corresponding_path("FILE_EXTENSION(*)"))

    def test_get_corresponding_path_returns_none_when_no_given_path_exists(self):
        self.assertIs(None, self.interpreter.get_corresponding_path("FILE_EXTENSION(*)"))

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


if __name__ == '__main__':
    unittest.main()
