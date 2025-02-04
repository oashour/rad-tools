# RAD-tools - program for spin Hamiltonian and magnons.
# Copyright (C) 2022-2023  Andrey Rybakov
#
# e-mail: anry@uv.es, web: adrybakov.com
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

__all__ = [
    "ABS_TOL",
    "REL_TOL",
    "MIN_LENGTH",
    "MAX_LENGTH",
    "ABS_TOL_ANGLE",
    "REL_TOL_ANGLE",
    "MIN_ANGLE",
    "ATOM_TYPES",
    "PEARSON_SYMBOLS",
    "BRAVAIS_LATTICE_NAMES",
    "BRAVAIS_LATTICE_VARIATIONS",
    "TRANSFORM_TO_CONVENTIONAL",
    "DEFAULT_K_PATHS",
    "HS_PLOT_NAMES",
]

# Length variables
ABS_TOL = 1e-8  # Meant for the linear spatial variables
REL_TOL = 1e-4  # Meant for the linear spatial variables
# MIN_LENGTH is a direct consequence of the REL_TOL and ABS_TOL:
# for l = MIN_LENGTH => ABS_TOL = l * REL_TOL
MIN_LENGTH = ABS_TOL / REL_TOL
# MAX_LENGTH is a direct consequence of the ABS_TOL:
# Inverse of the MAX_LENGTH in the real space has to be meaningful
# in the reciprocal space (< ABS_TOL).
MAX_LENGTH = 1 / ABS_TOL

# TODO Think how to connect angle tolerance with spatial tolerance.

ABS_TOL_ANGLE = 1e-4  # Meant for the angular variables, in degrees.
REL_TOL_ANGLE = 1e-2  # Meant for the angular variables.
# MIN_ANGLE is a direct consequence of the REL_TOL_ANGLE and ABS_TOL_ANGLE:
# for a = MIN_ANGLE => ABS_TOL_ANGLE = a * REL_TOL_ANGLE
MIN_ANGLE = ABS_TOL_ANGLE / REL_TOL_ANGLE  # In degrees

ATOM_TYPES = (
    "H",
    "He",
    "Li",
    "Be",
    "B",
    "C",
    "N",
    "O",
    "F",
    "Ne",
    "Na",
    "Mg",
    "Al",
    "Si",
    "P",
    "S",
    "Cl",
    "Ar",
    "K",
    "Ca",
    "Sc",
    "Ti",
    "V",
    "Cr",
    "Mn",
    "Fe",
    "Co",
    "Ni",
    "Cu",
    "Zn",
    "Ga",
    "Ge",
    "As",
    "Se",
    "Br",
    "Kr",
    "Rb",
    "Sr",
    "Y",
    "Zr",
    "Nb",
    "Mo",
    "Tc",
    "Ru",
    "Rh",
    "Pd",
    "Ag",
    "Cd",
    "In",
    "Sn",
    "Sb",
    "Te",
    "I",
    "Xe",
    "Cs",
    "Ba",
    "La",
    "Ce",
    "Pr",
    "Nd",
    "Pm",
    "Sm",
    "Eu",
    "Gd",
    "Tb",
    "Dy",
    "Ho",
    "Er",
    "Tm",
    "Yb",
    "Lu",
    "Hf",
    "Ta",
    "W",
    "Re",
    "Os",
    "Ir",
    "Pt",
    "Au",
    "Hg",
    "Tl",
    "Pb",
    "Bi",
    "Po",
    "At",
    "Rn",
    "Fr",
    "Ra",
    "Ac",
    "Th",
    "Pa",
    "U",
    "Np",
    "Pu",
    "Am",
    "Cm",
    "Bk",
    "Cf",
    "Es",
    "Fm",
    "Md",
    "No",
    "Lr",
    "Rf",
    "Db",
    "Sg",
    "Bh",
    "Hs",
    "Mt",
    "Ds",
    "Rg",
    "Cn",
    "Nh",
    "Fl",
    "Mc",
    "Lv",
    "Ts",
    "Og",
)


PEARSON_SYMBOLS = {
    "CUB": "cP",
    "FCC": "cF",
    "BCC": "cI",
    "TET": "tP",
    "BCT": "tI",
    "ORC": "oP",
    "ORCF": "oF",
    "ORCI": "oI",
    "ORCC": "oS",
    "HEX": "hP",
    "RHL": "hR",
    "MCL": "mP",
    "MCLC": "mS",
    "TRI": "aP",
}

BRAVAIS_LATTICE_NAMES = {
    "CUB": "Cubic",
    "FCC": "Face-centered cubic",
    "BCC": "Body-centered cubic",
    "TET": "Tetragonal",
    "BCT": "Body-centered tetragonal",
    "ORC": "Orthorhombic",
    "ORCF": "Face-centered orthorhombic",
    "ORCI": "Body-centered orthorhombic",
    "ORCC": "C-centered orthorhombic",
    "HEX": "Hexagonal",
    "RHL": "Rhombohedral",
    "MCL": "Monoclinic",
    "MCLC": "C-centered monoclinic",
    "TRI": "Triclinic",
}

BRAVAIS_LATTICE_VARIATIONS = [
    "CUB",
    "FCC",
    "BCC",
    "TET",
    "BCT1",
    "BCT2",
    "ORC",
    "ORCF1",
    "ORCF2",
    "ORCF3",
    "ORCI",
    "ORCC",
    "HEX",
    "RHL1",
    "RHL2",
    "MCL",
    "MCLC1",
    "MCLC2",
    "MCLC3",
    "MCLC4",
    "MCLC5",
    "TRI1a",
    "TRI2a",
    "TRI1b",
    "TRI2b",
]

TRANSFORM_TO_CONVENTIONAL = {
    "CUB": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    "FCC": [[-1.0, 1.0, 1.0], [1.0, -1.0, 1.0], [1.0, 1.0, -1.0]],
    "BCC": [[0, 1.0, 1.0], [1.0, 0, 1.0], [1.0, 1.0, 0]],
    "TET": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    "BCT": [[0, 1.0, 1.0], [1.0, 0, 1.0], [1.0, 1.0, 0]],
    "ORC": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    "ORCF": [[-1.0, 1.0, 1.0], [1.0, -1.0, 1.0], [1.0, 1.0, -1.0]],
    "ORCI": [[0, 1.0, 1.0], [1.0, 0, 1.0], [1.0, 1.0, 0]],
    "ORCC": [[1.0, 1.0, 0], [-1.0, 1.0, 0], [0, 0, 1.0]],
    "HEX": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    "RHL": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    "MCL": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    "MCLC": [[1.0, -1.0, 0.0], [1.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
    "TRI": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
}

DEFAULT_K_PATHS = {
    "CUB": "G-X-M-G-R-X|M-R",
    "FCC": "G-X-W-K-G-L-U-W-L-K|U-X",
    "BCC": "G-H-N-G-P-H|P-N",
    "TET": "G-X-M-G-Z-R-A-Z|X-R|M-A",
    "BCT1": "G-X-M-G-Z-P-N-Z1-M|X-P",
    "BCT2": "G-X-Y-S-G-Z-S1-N-P-Y1-Z|X-P",
    "ORC": "G-X-S-Y-G-Z-U-R-T-Z|Y-T|U-X|S-R",
    "ORCF1": "G-Y-T-Z-G-X-A1-Y|T-X1|X-A-Z|L-G",
    "ORCF2": "G-Y-C-D-X-G-Z-D1-H-C|C1-Z|X-H1|H-Y|L-G",
    "ORCF3": "G-Y-T-Z-G-X-A1-Y|X-A-Z|L-G",
    "ORCI": "G-X-L-T-W-R-X1-Z-G-Y-S-W|L1-Y|Y1-Z",
    "ORCC": "G-X-S-R-A-Z-G-Y-X1-A1-T-Y|Z-T",
    "HEX": "G-M-K-G-A-L-H-A|L-M|K-H",
    "RHL1": "G-L-B1|B-Z-G-X|Q-F-P1-Z|L-P",
    "RHL2": "G-P-Z-Q-G-F-P1-Q1-L-Z",
    "MCL": "G-Y-H-C-E-M1-A-X-H1|M-D-Z|Y-D",
    "MCLC1": "G-Y-F-L-I|I1-Z-F1|Y-X1|X-G-N|M-G",
    "MCLC2": "G-Y-F-L-I|I1-Z-F1|N-G-M",
    "MCLC3": "G-Y-F-H-Z-I-F1|H1-Y1-X-G-N|M-G",
    "MCLC4": "G-Y-F-H-Z-I|H1-Y1-X-G-N|M-G",
    "MCLC5": "G-Y-F-L-I|I1-Z-H-F1|H1-Y1-X-G-N|M-G",
    "TRI1a": "X-G-Y|L-G-Z|N-G-M|R-G",
    "TRI1b": "X-G-Y|L-G-Z|N-G-M|R-G",
    "TRI2a": "X-G-Y|L-G-Z|N-G-M|R-G",
    "TRI2b": "X-G-Y|L-G-Z|N-G-M|R-G",
}

HS_PLOT_NAMES = {
    "G": "$\\Gamma$",
    "M": "M",
    "R": "R",
    "X": "X",
    "K": "K",
    "L": "L",
    "U": "U",
    "W": "W",
    "H": "H",
    "P": "P",
    "N": "N",
    "A": "A",
    "Z": "Z",
    "Z1": "Z$_1$",
    "Y": "Y",
    "Y1": "Y$_1$",
    "S": "S",  # it is overwritten to sigma if needed.
    "S1": "S$_1$",  # it is overwritten to sigma if needed.
    "T": "T",
    "A1": "A$_1$",
    "X1": "X$_1$",
    "C": "C",
    "C1": "C$_1$",
    "D": "D",
    "D1": "D$_1$",
    "H1": "H$_1$",
    "L1": "L$_1$",
    "L2": "L$_2$",
    "B": "B",
    "B1": "B$_1$",
    "F": "F",
    "P1": "P$_1$",
    "P2": "P$_2$",
    "Q": "Q",
    "Q1": "Q$_1$",
    "E": "E",
    "H2": "H$_2$",
    "M1": "M$_1$",
    "M2": "M$_2$",
    "N1": "N$_1$",
    "F1": "F$_1$",
    "F2": "F$_2$",
    "F3": "F$_3$",
    "I": "I",
    "I1": "I$_1$",
    "X2": "X$_2$",
    "Y2": "Y$_2$",
    "Y3": "Y$_3$",
}
