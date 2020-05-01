#!/usr/bin/python
# Classification (U)

"""Program:  run_program.py

    Description:  Unit testing of run_program in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/run_program.py

    Arguments:

"""

# Libraries and Global Variables

# Standard
import sys
import os

if sys.version_info < (2, 7):
    import unittest2 as unittest
else:
    import unittest

# Third-party
import mock

# Local
sys.path.append(os.getcwd())
import isse_guard_transfer
import version

__version__ = version.__version__


class Isse(object):

    """Class:  Isse

    Description:  Class which is a representation of IsseGuard class.

    Methods:
        __init__ -> Initialize configuration environment.

    """

    def __init__(self, level, cfg, action, files, keep):

        """Method:  __init__

        Description:  Initialization instance of the IsseGuard class.

        Arguments:

        """

        self.level = level
        self.cfg = cfg
        self.action = action
        self.files = files
        self.keep = keep


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_one_file -> Test with one file check.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class CfgTest(object):

            """Class:  CfgTest

            Description:  Class which is a representation of a cfg module.

            Methods:
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.name = "name"

        self.cfg = CfgTest()
        self.args_array = {"-c": "config", "-d": "/path", "-N": "SIPR"}
        self.isse = Isse("Level", self.cfg, "process", None, False)

    @mock.patch("isse_guard_transfer.initate_process",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.load_cfg")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    def test_one_file(self, mock_isse, mock_cfg):

        """Function:  test_one_file

        Description:  Test with one file check.

        Arguments:

        """

        mock_isse.return_value = self.isse
        mock_cfg.return_value = (self.cfg, True)

        self.assertFalse(isse_guard_transfer.run_program(self.args_array))


if __name__ == "__main__":
    unittest.main()
