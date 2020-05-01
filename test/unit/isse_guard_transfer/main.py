#!/usr/bin/python
# Classification (U)

"""Program:  main.py

    Description:  Unit testing of main in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/main.py

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


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_help_true -> Test help if returns true.
        test_help_false -> Test help if returns false.
        test_arg_req_true -> Test arg_require if returns true.
        test_arg_req_false -> Test arg_require if returns false.
        test_arg_valid_false -> Test arg_valid_val if returns false.
        test_arg_valid_true -> Test arg_valid_val if returns true.
        test_arg_dir_true -> Test arg_dir_chk_crt if returns true.
        test_arg_dir_false -> Test arg_dir_chk_crt if returns false.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        self.args_array = {"-c": "CfgFile", "-d": "CfgDir", "-A": "process",
                           "-N": "SIPR"}

    @mock.patch("isse_guard_transfer.gen_libs.help_func")
    @mock.patch("isse_guard_transfer.arg_parser.arg_parse2")
    def test_help_true(self, mock_arg, mock_help):

        """Function:  test_help_true

        Description:  Test help if returns true.

        Arguments:

        """

        mock_arg.return_value = self.args_array
        mock_help.return_value = True

        self.assertFalse(isse_guard_transfer.main())

    @mock.patch("isse_guard_transfer.gen_libs.help_func")
    @mock.patch("isse_guard_transfer.arg_parser")
    def test_help_false(self, mock_arg, mock_help):

        """Function:  test_help_false

        Description:  Test help if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True

        self.assertFalse(isse_guard_transfer.main())

    @mock.patch("isse_guard_transfer.gen_libs.help_func")
    @mock.patch("isse_guard_transfer.arg_parser")
    def test_arg_req_true(self, mock_arg, mock_help):

        """Function:  test_arg_req_true

        Description:  Test arg_require if returns true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = True

        self.assertFalse(isse_guard_transfer.main())

    @mock.patch("isse_guard_transfer.gen_libs.help_func")
    @mock.patch("isse_guard_transfer.arg_parser")
    def test_arg_req_false(self, mock_arg, mock_help):

        """Function:  test_arg_req_false

        Description:  Test arg_require if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = False

        self.assertFalse(isse_guard_transfer.main())

    @mock.patch("isse_guard_transfer.gen_libs.help_func")
    @mock.patch("isse_guard_transfer.arg_parser")
    def test_arg_valid_false(self, mock_arg, mock_help):

        """Function:  test_arg_valid_false

        Description:  Test arg_valid_val if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = False

        self.assertFalse(isse_guard_transfer.main())

    @mock.patch("isse_guard_transfer.gen_libs.help_func")
    @mock.patch("isse_guard_transfer.arg_parser")
    def test_arg_valid_true(self, mock_arg, mock_help):

        """Function:  test_arg_valid_true

        Description:  Test arg_valid_val if returns true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(isse_guard_transfer.main())

    @mock.patch("isse_guard_transfer.gen_libs.help_func")
    @mock.patch("isse_guard_transfer.arg_parser")
    def test_arg_dir_true(self, mock_arg, mock_help):

        """Function:  test_arg_dir_true

        Description:  Test arg_dir_chk_crt if returns true.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = True

        self.assertFalse(isse_guard_transfer.main())

    @mock.patch("isse_guard_transfer.run_program")
    @mock.patch("isse_guard_transfer.gen_libs.help_func")
    @mock.patch("isse_guard_transfer.arg_parser")
    def test_arg_dir_false(self, mock_arg, mock_help, mock_run):

        """Function:  test_arg_dir_false

        Description:  Test arg_dir_chk_crt if returns false.

        Arguments:

        """

        mock_arg.arg_parse2.return_value = self.args_array
        mock_help.return_value = False
        mock_arg.arg_require.return_value = False
        mock_arg.arg_valid_val.return_value = True
        mock_arg.arg_dir_chk_crt.return_value = False
        mock_run.return_value = True

        self.assertFalse(isse_guard_transfer.main())


if __name__ == "__main__":
    unittest.main()
