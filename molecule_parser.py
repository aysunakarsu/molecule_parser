# -*- coding: utf-8 -*-
"""

This module is counting the number of atoms of each element 
contained in the molecule and return a dict for a given
chemical formula represented by a string.

Examples:
>>> water = 'H2O'
>>> parse_molecule(water) 
{'H': 2, 'O': 1}
>>> magnesium_hydroxide = 'Mg(OH)2'
>>> parse_molecule(magnesium_hydroxide)
{'Mg': 1, 'O': 2, 'H': 2}
>>> fremy_salt = 'K4[ON(SO3)2]2'
>>> parse_molecule(fremy_salt)
{'K': 4, 'O': 14, 'N': 2, 'S': 4}
"""
import re
from collections import OrderedDict
import json

OPEN_BRACKETS = '[({'
CLOSE_BRACKETS = '])}'


def find_multiplier(var_submolecule):
    var_multiplier = 1
    digits = re.search(r'(?<=^[\]\)\}])(\d+)', var_submolecule)
    if digits is not None:
        var_multiplier = int(digits.group(0))
    return var_multiplier


def add_to_dict(old_dict, new_dict):
    for element, value in new_dict.items():
        if element in old_dict:
            old_dict[element] += value
        else:
            old_dict[element] = value


def convert_submolecule_to_atoms_dict(var_submolecules_dict):
    dict_atoms = OrderedDict()
    for item, multiplier in var_submolecules_dict.items():
        search_list = re.findall(r'([A-Z][a-z]?)(\d*)', item)
        for element, value in search_list:
            if value == '':
                value = 1 * multiplier
            else:
                value = int(value) * multiplier
            add_to_dict(dict_atoms, OrderedDict([(element, value)]))
    return dict_atoms


def parse_submolecule_multiplier(var_submolecules, multiplier=1):
    dict_submolecules = OrderedDict()
    stack = []
    submolecule_multiplier = 1
    for index_submolecule, submolecule in enumerate(var_submolecules):
        if submolecule in OPEN_BRACKETS:
            stack.append(index_submolecule)
        elif submolecule[0] in CLOSE_BRACKETS:
            index_start = stack.pop() + 1
            submolecule_multiplier = find_multiplier(submolecule) * multiplier
            if not stack:
                add_to_dict(
                    dict_submolecules,
                    parse_submolecule_multiplier(
                        var_submolecules[index_start:index_submolecule],
                        submolecule_multiplier))
            else:
                parse_submolecule_multiplier(
                    var_submolecules[index_start:index_submolecule],
                    submolecule_multiplier)
        elif not stack:
            add_to_dict(dict_submolecules,
                        OrderedDict([(submolecule, multiplier)]))
    return dict_submolecules


def parse_molecule(molecule):
    pattern_submolecule = re.compile("([\[\(\{]|[\]\)\}][\d]*)")
    list_submolecules = [
        x.strip() for x in pattern_submolecule.split(molecule) if x
    ]
    submolecule_dict = parse_submolecule_multiplier(list_submolecules)
    submolecule_dict_to_atoms_dict = convert_submolecule_to_atoms_dict(
        submolecule_dict)
    print("{}".format(
        json.dumps(submolecule_dict_to_atoms_dict).replace('"', '\'')))


if __name__ == '__main__':
    import doctest
    count, _ = doctest.testmod()
    if count == 0:
        print('*** ALL TESTS PASS ***')
