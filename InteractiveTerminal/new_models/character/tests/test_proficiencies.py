import unittest
import typing as T

from ..proficiencies import Proficiency
from ..stats import Stat


class TestProficiencies(unittest.TestCase):
    def test_all_func(self) -> None:
        self.assertEqual(len(Proficiency.__members__), len(Proficiency.all()))

    def test_all_proficiencies_have_matching_stat(self) -> None:
        for each_prof in Proficiency.all():
            self.assertIsInstance(each_prof.corresponding_stat(), Stat)
