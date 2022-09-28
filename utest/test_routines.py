from os.path import isdir, join
from os import rmdir

import pytest

from rad_tools.routines import *


class TestTerminalColours:

    def test_for_human(self):
        print("\n Please check that the following colours "
              "are displayed correctly:\n")
        print(f'{TerminalCoulours.BLACK}BLACK{TerminalCoulours.RESET}',
              f'{TerminalCoulours.RED}RED{TerminalCoulours.RESET}',
              f'{TerminalCoulours.GREEN}GREEN{TerminalCoulours.RESET}',
              f'{TerminalCoulours.YELLOW}YELLOW{TerminalCoulours.RESET}',
              f'{TerminalCoulours.BLUE}BLUE{TerminalCoulours.RESET}',
              f'{TerminalCoulours.MAGENTA}MAGENTA{TerminalCoulours.RESET}',
              f'{TerminalCoulours.CYAN}CYAN{TerminalCoulours.RESET}',
              f'{TerminalCoulours.WHITE}WHITE{TerminalCoulours.RESET}',
              sep='\n')
        assert TerminalCoulours.WARNING == TerminalCoulours.YELLOW
        assert TerminalCoulours.OK == TerminalCoulours.GREEN
        assert TerminalCoulours.ERROR == TerminalCoulours.RED


def test_get_256_colours():
    print("\n Please check that the following colour's table "
          "looks beautifull:\n")
    for i in range(0, 16):
        for j in range(0, 16):
            print(f'{get_256_colours(16 * i + j)}'
                  f'{16 * i + j:3}'
                  f'{TerminalCoulours.RESET}',
                  end=' ')
        print()
    with pytest.raises(ValueError):
        get_256_colours(345)
    with pytest.raises(ValueError):
        get_256_colours(256)
    with pytest.raises(ValueError):
        get_256_colours(34.5)
    with pytest.raises(ValueError):
        get_256_colours(-45)
    with pytest.raises(ValueError):
        get_256_colours('sadfasd')
    assert get_256_colours(0) == '\033[38:5:0m'
    assert get_256_colours(255) == '\033[38:5:255m'
    assert get_256_colours(34) == '\033[38:5:34m'


def test_check_make():
    with pytest.raises(FileNotFoundError):
        check_make(join('sadfsd', 'sdfgsd'))
    check_make('tmp')
    assert isdir('tmp') == True
    check_make('tmp')
    assert isdir('tmp') == True
    rmdir('tmp')


@pytest.mark.parametrize("iso, aniso, dmi, matrix", [
    (1,
     None,
     None,
     [[1, 0, 0],
      [0, 1., 0],
      [0, 0, 1]]),

    (1,
     [[1, 0, 0],
      [0, 1., 0],
      [0, 0, 1]],
        None,
     [[2, 0, 0],
      [0, 2., 0],
      [0, 0, 2]]),

    (1.23,
     [[0.01, 5., 0.004],
      [5., -0.003, 0],
      [0.004, 0, .034]],
        None,
        [[1.24, 5., 0.004],
         [5., 1.227, 0],
         [0.004, 0, 1.264]]),

    (None,
     [[0.01, 5., 0.004],
      [5., -0.003, 0],
      [0.004, 0, .034]],
        None,
        [[0.01, 5., 0.004],
         [5., -0.003, 0],
         [0.004, 0, 0.034]]),

    (0,
     [[0.01, 5., 0.004],
      [5., -0.003, 0],
      [0.004, 0, .034]],
        None,
        [[0.01, 5., 0.004],
         [5., -0.003, 0],
         [0.004, 0, 0.034]]),

    (None,
     [[0.01, 5., 0.004],
      [5., -0.003, 0],
      [0.004, 0, .034]],
        (0, 0, 0),
        [[0.01, 5., 0.004],
         [5., -0.003, 0],
         [0.004, 0, 0.034]]),

    (None,
     [[0.01, 5., 0.005],
      [5., -0.003, 0],
      [0.005, 0, .034]],
        (1, 0.06, -0.001),
        [[0.01, 4.999, -0.055],
         [5.001, -0.003, 1],
         [0.065, -1, 0.034]]),

    (3.0830,
     [[-0.009, 0, 0.004],
      [0, -0.013, 0],
      [0.004, 0, -0.007]],
        (-0.0002, 0.0001, 0.0001),
        [[3.074, 0.0001, 0.0039],
         [-0.0001, 3.07, -0.0002],
         [0.0041, 0.0002, 3.076]])

])
def test_exchange_to_matrix(iso, aniso, dmi, matrix):
    for i in range(0, 3):
        for j in range(0, 3):
            assert round(exchange_to_matrix(iso, aniso, dmi)[i][j], 4) ==\
                round(matrix[i][j], 4)


@pytest.mark.parametrize("iso, aniso, dmi, matrix", [
    (1,
     [[0, 0, 0],
      [0, 0, 0],
      [0, 0, 0]],
     (0, 0, 0),
     [[1, 0, 0],
      [0, 1., 0],
      [0, 0, 1]]),

    (2,
     [[0, 0, 0],
      [0, 0, 0],
      [0, 0, 0]],
        (0, 0, 0),
     [[2, 0, 0],
      [0, 2., 0],
      [0, 0, 2]]),

    (1.2437,
     [[-0.0037, 5., 0.004],
      [5., -0.0167, 0],
      [0.004, 0, 0.0203]],
        (0, 0, 0),
        [[1.24, 5., 0.004],
         [5., 1.227, 0],
         [0.004, 0, 1.264]]),

    (0.0137,
     [[-0.0037, 5., 0.004],
      [5., -0.0167, 0],
      [0.004, 0, 0.0203]],
        (0, 0, 0),
        [[0.01, 5., 0.004],
         [5., -0.003, 0],
         [0.004, 0, 0.034]]),

    (0.0137,
     [[-0.0037, 5., 0.004],
      [5., -0.0167, 0],
      [0.004, 0, 0.0203]],
        (1, 0.06, -0.001),
        [[0.01, 4.999, -0.056],
         [5.001, -0.003, 1],
         [0.064, -1, 0.034]])

])
def test_exchange_from_matrix(iso, aniso, dmi, matrix):
    iso_d, aniso_d, dmi_d = exchange_from_matrix(matrix)

    assert iso == round(iso_d, 4)

    for i in range(0, 3):
        assert round(dmi[i], 4) == round(dmi_d[i], 4)
        for j in range(0, 3):
            assert round(aniso[i][j], 4) == round(aniso_d[i][j], 4)
