import unittest
from collections import OrderedDict
from molecule_parser import find_multiplier
from molecule_parser import convert_submolecule_to_atoms_dict
from molecule_parser import parse_submolecule_multiplier
from molecule_parser import parse_molecule


class ParsermoleculeTestCase(unittest.TestCase):
    """Tests for 'parsermolecule.py`."""

    def test_find_multiplier(self):
        """Is multiplier successfully returned?"""
        self.assertEqual(find_multiplier(")5"), 5)
        self.assertEqual(find_multiplier(")10"), 10)
        self.assertEqual(find_multiplier("))5"), 1)

    def test_convert_submolecule_to_atoms_dict(self):
        """Is submolecule successfully converted to atoms dict?"""
        dict_list = {"H2O": 1}
        self.assertEqual(
            convert_submolecule_to_atoms_dict(dict_list),
            OrderedDict([('H', 2), ('O', 1)]))

    def test_parse_submolecule_multiplier(self):
        """Check if submolecules and their multipliers can be extracted sucessfully """
        water = ['H2O']
        magnesium_hydroxide = ['Mg', '(', 'OH', ')2']
        fremy_salt = ['K4', '[', 'ON', '(', 'SO3', ')2', ']2']
        self.assertEqual(
            parse_submolecule_multiplier(water), OrderedDict([('H2O', 1)]))
        self.assertEqual(
            parse_submolecule_multiplier(magnesium_hydroxide),
            OrderedDict([('Mg', 1), ('OH', 2)]))
        self.assertEqual(
            parse_submolecule_multiplier(fremy_salt),
            OrderedDict([('K4', 1), ('ON', 2), ('SO3', 4)]))

if __name__ == '__main__':
    unittest.main()
