import unittest
import typing as T

from ..proficiencies import Proficiency
from ..stats import Stat

class TestProficiencies(unittest.TestCase):
    def test_all_proficiencies_have_matching_stat(self) -> None:
        members = Proficiency.__members__
        for val in members:
            self.assertIsInstance(members[val].corresponding_stat(), Stat)
