import unittest
from file_mover import interpreter


class InterpreterTest(unittest.TestCase):

    def setUp(self):
        move_config = {'WHERE_FROM': {'wiki': 'Users/Peter/Library'},
                       'NAME': {'China': 'Users/Peter'},
                       'FILE_EXTENSION': {'.zip': 'Users/Peter/Home'}}
        file_props = {'WHERE_FROM': 'wikipedia', 'NAME': 'China', 'FILE_EXTENSION': '.html'}
        self.interpreter = interpreter2.Interpreter(file_props, move_config, {})

    def test_token_corresponds_with_WHERE_FROM_parameter(self):
        self.assertTrue(self.interpreter.token_corresponds("WHERE_FROM(wikipedia)"))
        self.assertTrue(self.interpreter.token_corresponds("WHERE_FROM(wiki)"))
        self.assertTrue(self.interpreter.token_corresponds("WHERE_FROM(*)"))

        self.assertFalse(self.interpreter.token_corresponds("WHERE_FROM(wikiPEDIA)"))
        self.assertFalse(self.interpreter.token_corresponds("WHERE_FROM(wiki )"))
        self.assertFalse(self.interpreter.token_corresponds("WHERE_FROM(/*)"))

    def test_token_corresponds_with_different_parameters(self):
        self.assertTrue(self.interpreter.token_corresponds("NAME(China)"))
        self.assertTrue(self.interpreter.token_corresponds("FILE_EXTENSION(.html)"))
        self.assertTrue(self.interpreter.token_corresponds("FILE_EXTENSION(.)"))  # This might be a problem

    def test_antecedent_corresponds(self):
        self.assertTrue(self.interpreter.antecedent_corresponds("WHERE_FROM(wiki) & NAME(China)"))
        self.assertTrue(self.interpreter.antecedent_corresponds("WHERE_FROM(wiki) & NAME(China) & FILE_EXTENSION(.html)"))
        self.assertFalse(self.interpreter.antecedent_corresponds("FILE_EXTENSION(*) & WHERE_FROM(wiki)"))
        self.assertFalse(self.interpreter.antecedent_corresponds("WHERE_FROM(China) & NAME(wiki)"))

    def test_get_corresponding_path(self):
        self.assertIs('Users/Peter/Library', self.interpreter.get_corresponding_path("WHERE_FROM(wiki)"))
        self.assertIs('Users/Peter', self.interpreter.get_corresponding_path("NAME(*)"))
        self.assertIs(None, self.interpreter.get_corresponding_path("FILE_EXTENSION(*)"))

    def test_parse_command(self):
        self.interpreter.commands = [{'WHERE_FROM(wiki) & NAME(China):': 'WHERE_FROM(wiki)'}]
        self.assertIs('Users/Peter/Library', self.interpreter.parse_command())

        self.interpreter.commands = [{'WHERE_FROM(uni) & NAME(China):': 'WHERE_FROM(wiki)'},
                                     {'WHERE_FROM(wiki) & NAME(China):': 'WHERE_FROM(wiki)'}]
        self.assertIs('Users/Peter/Library', self.interpreter.parse_command())

        self.interpreter.commands = [{'WHERE_FROM(uni) & NAME(China):': 'WHERE_FROM(wiki)'}]
        self.assertIs(None, self.interpreter.parse_command())