import os

import pytest
import numpy as np

from rad_tools.tb2j_tools.file_logic import *
from rad_tools.tb2j_tools.template_logic import *


class TestExchangeModelTB2J:

    model = ExchangeModelTB2J(os.path.join(
        'utest', 'tb2j_tools', 'resourses', 'exchange.out'
    ))
    template = [('Cr1', 'Cr1', (1, 0, 0)), ('Cr1', 'Cr1', (-1, 0, 0)),
                ('Cr2', 'Cr2', (1, 0, 0)), ('Cr2', 'Cr2', (-1, 0, 0)),
                ('Cr1', 'Cr1', (1, 0, 0)), ('Cr2', 'Cr2', (-1, 0, 0)),
                ('Cr1', 'Cr1', (-1, 0, 0)), ('Cr2', 'Cr2', (1, 0, 0)),
                ('Cr1', 'Cr2', (0, 0, 0)), ('Cr1', 'Cr2', (1, 0, 0)),
                ('Cr1', 'Cr2', (0, -1, 0)), ('Cr1', 'Cr2', (1, -1, 0)),
                ('Cr2', 'Cr1', (0, 0, 0)), ('Cr2', 'Cr1', (-1, 0, 0)),
                ('Cr2', 'Cr1', (0, 1, 0)), ('Cr2', 'Cr1', (-1, 1, 0)),
                ('Cr1', 'Cr2', (1, 0, 0)), ('Cr1', 'Cr2', (1, -1, 0)),
                ('Cr2', 'Cr1', (-1, 0, 0)), ('Cr2', 'Cr1', (-1, 1, 0)),
                ('Cr1', 'Cr2', (0, 0, 0)), ('Cr1', 'Cr2', (0, -1, 0)),
                ('Cr2', 'Cr1', (0, 0, 0)), ('Cr2', 'Cr1', (0, 1, 0)),
                ('Cr1', 'Cr1', (0, 1, 0)), ('Cr1', 'Cr1', (0, -1, 0)),
                ('Cr2', 'Cr2', (0, 1, 0)), ('Cr2', 'Cr2', (0, -1, 0))]


class TestInputFilename(TestExchangeModelTB2J):

    def test_empty_filename(self):
        with pytest.raises(TypeError):
            model = ExchangeModelTB2J(None)

    def test_wrong_filename(self):
        with pytest.raises(FileNotFoundError):
            model = ExchangeModelTB2J(
                "Ah, music. A magic beyond all we do here!")

    def test_correct_filename(self):
        model = ExchangeModelTB2J(os.path.join(
            'utest', 'tb2j_tools', 'resourses', 'exchange.out'))


class TestReadFunctions(TestExchangeModelTB2J):

    def test_read_cell(self):
        assert self.model.cell is not None
        cell_values = [[3.588, 0.000, 0.000],
                       [0.000,  4.807,  0.000],
                       [0.000,  0.000, 23.571]]
        for i in range(0, 3):
            for j in range(0, 3):
                assert self.model.cell[i][j] == cell_values[i][j]

    def test_read_atoms(self):
        assert self.model._atoms is not None
        atoms_value = {
            'Br1': (0.8970, 1.2018, -0.0668),
            'Cr1': (2.6910, 1.2018,  1.7371),
            'S1':  (2.6910, 3.6054,  2.2030),
            'Br2': (2.6910, 3.6054,  5.6376),
            'Cr2': (0.8970, 3.6054,  3.8336),
            'S2':  (0.8970, 1.2018,  3.3678)
        }
        for key in self.model._atoms:
            assert key in atoms_value
        for key in atoms_value:
            assert key in self.model._atoms
            assert atoms_value[key] == self.model._atoms[key]

    @pytest.mark.parametrize("atom1, atom2, R, iso, aniso, dmi, distance",
                             [
                                 ('Cr1', 'Cr1',
                                  (-1, 0, 0),
                                  3.5386,
                                  [[-0.032, 0, 0],
                                   [0, -0.054, 0],
                                   [0, 0, -0.028]],
                                  (0, -0.0163, 0),
                                  3.588),

                                 ('Cr1', 'Cr2',
                                  (0, 0, 0),
                                  3.0830,
                                  [[-0.009, 0, 0.004],
                                   [0, -0.013, 0],
                                   [0.004, 0, -0.007]],
                                  (-0.0002, 0.0001, 0.0001),
                                  3.659),

                                 ('Cr1', 'Cr1',
                                  (0, 1, 0),
                                  4.1479,
                                  [[-0.016, 0, 0],
                                   [0, -0.003, 0],
                                   [0, 0, -0.008]],
                                  (-0.0584, 0, 0),
                                  4.807),

                                 ('Cr1', 'Cr1',
                                  (-1, 1, 0),
                                  0.0422,
                                  [[-0.007, 0, 0],
                                   [0, -0.006, 0],
                                   [0, 0, -0.005]],
                                  (0.0194, -0.0170, 0),
                                  5.999),

                                 ('Cr2', 'Cr2',
                                  (0, -1, 0),
                                  4.1423,
                                  [[-0.016, 0, 0],
                                   [0, -0.003, 0],
                                   [0, 0, -0.008]],
                                  (-0.0568, 0, 0),
                                  4.807),

                                 ('Cr2', 'Cr2',
                                  (0, 2, 0),
                                  0.1209,
                                  [[-0.001, 0, 0],
                                   [0, 0, 0],
                                   [0, 0, 0]],
                                  (0.0363, 0, 0),
                                  9.614),

                                 ('Cr2', 'Cr1',
                                  (1, -1, 0),
                                  0.0038,
                                  [[-0.001, 0, 0],
                                   [0, -0.001, 0],
                                   [0, 0, -0.001]],
                                  (0, 0, 0),
                                  9.239),

                                 ('Cr1', 'Cr2',
                                  (1, -2, 0),
                                  0.5503,
                                  [[-0.001, 0, 0],
                                   [0, -0.002, 0],
                                   [0, 0, -0.001]],
                                  (0.0001, -0.0001, 0),
                                  7.721),

                                 ('Cr2', 'Cr1',
                                  (-1, 1, 0),
                                  3.0830,
                                  [[-0.009, 0, -0.004],
                                   [0, -0.013, 0],
                                   [-0.004, 0, -0.007]],
                                  (-0.0002, 0.0001, -0.0001),
                                  3.659),
                             ])
    def test_read_exchange_examples(self, atom1, atom2, R, iso, aniso, dmi, distance):
        assert self.model.bonds[atom1][atom2][R].iso == iso
        assert self.model.bonds[atom1][atom2][R].dis == distance
        for i in range(0, 3):
            assert self.model.bonds[atom1][atom2][R].dmi[i] == dmi[i]
            for j in range(0, 3):
                assert self.model.bonds[atom1][atom2][R].aniso[i][j] == aniso[i][j]

    def test_magnetic_atoms(self):
        assert len(self.model.magnetic_atoms) == 2
        assert self.model.magnetic_atoms['Cr1'] == (2.6910, 1.2018,  1.7371)
        assert self.model.magnetic_atoms['Cr2'] == (0.8970, 3.6054,  3.8336)


class TestFilter(TestExchangeModelTB2J):

    def count_entries(self, dictionary):
        i = 0
        if dictionary is not None:
            for atom1 in dictionary:
                for atom2 in dictionary[atom1]:
                    for R in dictionary[atom1][atom2]:
                        i += 1
        return i

    @pytest.mark.parametrize("distance, elements_number", [
        (4.807, 16),
        (6, 24),
        (0, 0),
        (5, 16),
        (4.0, 12),
        (1000, 72)
    ])
    def test_filter_by_distance(self, distance, elements_number):
        filtered_model = self.model.filter(distance=distance)
        assert self.count_entries(filtered_model.bonds) == elements_number

    def test_filter_by_template(self):
        filtered_model = self.model.filter(
            template=self.template)
        assert self.count_entries(filtered_model.bonds) == 16

    @pytest.mark.parametrize("distance, elements_number", [
        (4.807, 16),
        (6, 16),
        (0, 0),
        (5, 16),
        (4.0, 12),
        (1000, 16),
        (8, 16)
    ])
    def test_filter_by_distance_and_template(self,
                                             distance,
                                             elements_number):
        filtered_model = self.model.filter(distance=distance,
                                           template=self.template)
        assert self.count_entries(filtered_model.bonds) == elements_number
