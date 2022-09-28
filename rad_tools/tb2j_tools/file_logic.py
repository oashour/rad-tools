from copy import deepcopy
from typing import Union, Tuple
import numpy as np

from rad_tools.tb2j_tools.template_logic import ExchangeTemplate
from rad_tools.routines import exchange_from_matrix, exchange_to_matrix


class Bond:
    """
    Class with implemented logic for one bond

    Parameters
    ----------
    iso : float
        Value of isotropic exchange parameter in meV. If `iso` is 
        not specified then it will be 0.
        J
        Matrix from:

             J | 0 | 0 
            ---|---|---
             0 | J | 0 
            ---|---|---
             0 | 0 | J 
    aniso : 3 x 3 np.ndarray of floats
        3 x 3 matrix of symmetric anisotropic exchange in meV. If `aniso` 
        is not specified then it will be filled with zeros.
            J_xx | J_xy | J_xz
            -----|------|-----
            J_xy | J_yy | J_yz
            -----|------|-----
            J_xz | J_yz | J_zz
    dmi : 3 x 1 np.ndarray of floats
        Dzyaroshinsky-Moria interaction vector (Dx, Dy, Dz) in meV. If `dmi` 
        is not specified then it will be filled with zeros.
        [D_x, D_y, D_z]
        Matrix form:
               0  |  D_z | -D_y
            ------|------|------
             -D_z |   0  | D_x
            ------|------|------
              D_y | -D_x |  0
    matrix : 3 x 3 np.ndarray of floats
        Exchange matrix in meV. If `matrix` is specified then `iso`, 
        `aniso` and `dmi` will be ignored and derived from `matrix`.
        If `matrix` is not specified then it will be derived from 
        `iso`, `aniso` and `dmi`.
            J_xx | J_xy | J_xz
            -----|------|-----
            J_yx | J_yy | J_yz
            -----|------|-----
            J_zx | J_zy | J_zz
    """

    def __init__(self,
                 iso=None,
                 aniso=None,
                 dmi=None,
                 matrix=None,
                 distance=None) -> None:
        self.iso = 0.
        self.aniso = np.zeros((3, 3), dtype=float)
        self.dmi = np.zeros(3, dtype=float)
        self.matrix = np.zeros((3, 3), dtype=float)
        self.dis = 0.

        if matrix is not None:
            self.matrix = np.array(matrix, dtype=float)
            self.iso, self.aniso, self.dmi = exchange_from_matrix(self.matrix)
        else:
            if iso is not None:
                self.iso = float(iso)
            if aniso is not None:
                self.aniso = np.array(aniso, dtype=float)
            if dmi is not None:
                self.dmi = np.array(dmi, dtype=float)
            self.matrix = exchange_to_matrix(self.iso, self.aniso, self.dmi)

        if distance is not None:
            self.dis = float(distance)


class ExchangeModel:
    """
    Class containing the whole information extracted from TB2J *.out

    Keeping resolved data from the file
    and provide a number of functions to process it.

    Attributes
    ----------
    cell : 3 x 3 np.ndarray of floats
        3 x 3 matrix of lattice vectors in Angstrom.
            a_x | a_y | a_z
            ----|-----|----
            b_x | b_y | b_z
            ----|-----|----
            c_x | x_y | c_z

    magnetic_atoms : dict 
       Dictionary with keys : str - marks of atoms and value : 1 x 3 np.ndarray
       - coordinate of the atom in Angstroms.

    bonds : dict
        Dictionary of bonds.
        {
            Atom_1: {
                Atom_2: {
                    R: bond,
                    ...
                },
                ...
            },
            ...
        }

    Methods
    -------
    add_bond(bond, atom1, atom2, R)
        Add one bond to the model.

    remove_bond(atom1, atom2, R)
        Remove one bond from the model.

    add_atom(name, x, y, z)
        Add magnetic atom to the model.

    remove_atom(name)
        Remove magnetic atom from the model

    filter(distance=None, number=None, template=None, from_scratch=False)
        Filter all present exchange parameters
        with respect to the provided conditions
    """

    def __init__(self) -> None:
        self.cell = np.zeros((3, 3), dtype=float)
        self.magnetic_atoms = {}
        self.bonds = {}

    def add_atom(self, name: str,
                 x: Union[int, float],
                 y: Union[int, float],
                 z: Union[int, float]):
        """
        Add magnetic atom to the model.

        Parameters
        ----------
        name : str
            Mark for the atom. Note: if an atom with the same mark already 
            exists in `magnetic_atoms` then it will be rewritten
        x : int or float
            x coordinate of the atom, in Angstroms.
        y : int or float
            y coordinate of the atom, in Angstroms.
        z : int or float
            z coordinate of the atom, in Angstroms.
        """
        self.magnetic_atoms[name] = (float(x), float(y), float(z))

    def remove_atom(self, name: str):
        """
        Remove magnetic atom from the model

        Note: this method will remove atom from `magnetic_atoms` and all the 
        bonds, which starts or ends in this atom.

        Parameters
        ----------
        name : str
            Mark for the atom. 
        """
        if name in self.magnetic_atoms:
            del self.magnetic_atoms[name]
        if name in self.bonds:
            del self.bonds[name]
        for atom1 in self.bonds:
            if name in self.bonds[atom1]:
                del self.bonds[atom1][name]

    def add_bond(self, bond: Bond, atom1: str, atom2: str, R: Tuple[int]):
        """
        Add one bond to the model.

        Parameters
        ----------
        bond : Bond
            An instance of Bond Class with the information about 
            exchange parameters.
        atom1 : str
            Name of atom1 in (0, 0, 0) unit cell.
        atom2 : str 
            Name of atom2 in R unit cell.
        R : tuple of ints
            Radius vector of the unit cell for atom2.
        """
        if atom1 not in self.bonds:
            self.bonds[atom1] = {}
        if atom2 not in self.bonds[atom1]:
            self.bonds[atom1][atom2] = {}
        self.bonds[atom1][atom2][R] = bond

    def remove_bond(self, atom1: str, atom2: str, R: Tuple[int]):
        """
        Remove one bond from the model.

        Parameters
        ----------
        atom1 : str
            Name of atom1 in (0, 0, 0) unit cell.
        atom2 : str 
            Name of atom2 in R unit cell.
        R : tuple of ints
            Radius vector of the unit cell for atom2.
        """
        if atom1 in self.bonds and \
            atom2 in self.bonds[atom1] and \
                R in self.bonds[atom1][atom2]:
            del self.bonds[atom1][atom2][R]
            if not self.bonds[atom1][atom2]:
                del self.bonds[atom1][atom2]
            if not self.bonds[atom1]:
                del self.bonds[atom1]

    def filter(self,
               distance: Union[float, int] = None,
               template: list = None):
        """
        Filter the exchange entries based on the given conditions.

        The result will be defined by logical conjugate of the conditions. 
        Saying so the filtering will be performed for each given condition 
        one by one.
        Note: this method is not modifying the instance at which it is called.
        It will create a new instance with sorted `bonds` and all the other
        attributes will be copied (through deepcopy).

        Parameters
        ----------
        distance : float or int, optional
            Distance for sorting, the condition is <<less or equal>>.
        template : list
            List of pairs for keeping. Specifying atom1, atom2, R.
            [(atom1, atom2, R), ...]
        """
        filtered_model = deepcopy(self)

        if template is not None:
            filtered_model.bonds = {}
            for atom1, atom2, R in template:
                filtered_model.add_bond(self.bonds[atom1][atom2][R],
                                        atom1, atom2, R)
        bonds_for_removal = []
        if distance is not None:
            for atom1 in filtered_model.bonds:
                for atom2 in filtered_model.bonds[atom1]:
                    for R in filtered_model.bonds[atom1][atom2]:
                        if filtered_model.bonds[atom1][atom2][R].dis > distance:
                            bonds_for_removal.append((atom1, atom2, R))
        for atom1, atom2, R in bonds_for_removal:
            filtered_model.remove_bond(atom1, atom2, R)
        return filtered_model


class ExchangeModelTB2J(ExchangeModel):
    """
    Class containing the exchange model extracted from TB2J *.out

    Parameters
    ----------
    filename : str
        Path to the TB2J *.out file.
    """
    _major_sep = '=' * 90 + '\n'
    _minor_sep = '-' * 88 + '\n'
    _garbage = str.maketrans({'(': None,
                              ')': None,
                              '[': None,
                              ']': None,
                              ',': None,
                              '\'': None})
    _cell_flag = 'Cell (Angstrom):'
    _atoms_flag = 'Atoms:'
    _atom_end_flag = 'Total'
    _exchange_flag = 'Exchange:'
    _iso_flag = 'J_iso:'
    _aniso_flag = 'J_ani:'
    _dmi_flag = 'DMI:'
    _atoms = {}

    def __init__(self, filename: str) -> None:
        super().__init__()
        file = open(filename, 'r')
        line = True

        # Read everything before exchange
        while line:
            line = file.readline()

            # Read cell
            if line and self._cell_flag in line:
                self.cell = np.array([
                    list(map(float, file.readline().split())),
                    list(map(float, file.readline().split())),
                    list(map(float, file.readline().split()))
                ])

            # Read atoms
            if line and self._atoms_flag in line:
                line = file.readline()
                line = file.readline()
                line = file.readline().split()
                while line and self._atom_end_flag not in line:
                    self._atoms[line[0]] = tuple(map(float, line[1:4]))
                    line = file.readline().split()

            if line and self._exchange_flag in line:
                break

        # Read exchange
        while line:
            while line and self._minor_sep not in line:
                line = file.readline()
            line = file.readline().translate(self._garbage).split()
            atom1 = line[0]
            atom2 = line[1]
            R = tuple(map(int, line[2:5]))
            distance = float(line[-1])
            while line and self._minor_sep not in line:
                line = file.readline()

                # Read isotropic exchange
                if line and self._iso_flag in line:
                    iso = float(line.split()[-1])

                # Read anisotropic exchange
                if line and self._aniso_flag in line:
                    aniso = np.array([
                        list(map(float, file.readline().translate(
                            self._garbage).split())),
                        list(map(float, file.readline().translate(
                            self._garbage).split())),
                        list(map(float, file.readline().translate(
                            self._garbage).split()))
                    ])

                # Read DMI
                if line and self._dmi_flag in line:
                    dmi = tuple(map(float, line.translate(
                        self._garbage).split()[-3:]))

            # Adding info from the exchange block to the ExchangeModel structure
            if atom1 not in self.magnetic_atoms:
                self.add_atom(atom1, *self._atoms[atom1])
            if atom2 not in self.magnetic_atoms:
                self.add_atom(atom2, *self._atoms[atom2])
            bond = Bond(iso=iso, aniso=aniso, dmi=dmi, distance=distance)
            self.add_bond(bond, atom1, atom2, R)
