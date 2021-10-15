#!/usr/bin/python
# Classification (U)

"""Program:  load_cfg.py

    Description:  Unit testing of load_cfg in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/load_cfg.py

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
import lib.gen_libs as gen_libs
import version

__version__ = version.__version__


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_backup_not_bool
        test_status_false3
        test_status_false2
        test_status_false
        test_good_check

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
                __init__

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the CfgTest class.

                Arguments:

                """

                self.dissem_dir = "/path/dissem_dir"
                self.transfer_dir = "/path/transfer_dir"
                self.backup = True
                self.log_dir = "/path/log_dir"

        self.cfg = CfgTest()
        self.dissem_dir = "/path/dissem_dir/"
        self.dissem_dir2 = "/path/dissem_dir"
        self.transfer_dir = "/path/transfer_dir/"
        self.transfer_dir2 = "/path/transfer_dir"
        self.log_dir = "/path/log_dir/"
        self.log_dir2 = "/path/log_dir"
        self.cfg_name = "config_file"
        self.cfg_dir = "/dirpath"

    @mock.patch("isse_guard_transfer.gen_libs")
    def test_backup_not_bool(self, mock_lib):

        """Function:  test_backup_not_bool

        Description:  Test with backup is not boolean.

        Arguments:

        """

        self.cfg.backup = "A String"

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (True, None)]

        with gen_libs.no_std_out():
            cfg, status_flag = isse_guard_transfer.load_cfg(self.cfg_name,
                                                            self.cfg_dir)
        self.assertEqual(
            (cfg.dissem_dir, cfg.transfer_dir, cfg.log_dir, status_flag),
            (self.dissem_dir, self.transfer_dir, self.log_dir, False))

    @mock.patch("isse_guard_transfer.gen_libs")
    def test_status_false3(self, mock_lib):

        """Function:  test_status_false3

        Description:  Test with third status flag set to false.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (True, None), (False, "Error Message3")]

        cfg, status_flag = isse_guard_transfer.load_cfg(self.cfg_name,
                                                        self.cfg_dir)
        self.assertEqual(
            (cfg.dissem_dir, cfg.transfer_dir, cfg.log_dir, status_flag),
            (self.dissem_dir, self.transfer_dir, self.log_dir2, False))

    @mock.patch("isse_guard_transfer.gen_libs")
    def test_status_false2(self, mock_lib):

        """Function:  test_status_false2

        Description:  Test with second status flag set to false.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = [
            (True, None), (False, "Error Message2"), (True, None)]

        cfg, status_flag = isse_guard_transfer.load_cfg(self.cfg_name,
                                                        self.cfg_dir)
        self.assertEqual(
            (cfg.dissem_dir, cfg.transfer_dir, cfg.log_dir, status_flag),
            (self.dissem_dir, self.transfer_dir2, self.log_dir, False))

    @mock.patch("isse_guard_transfer.gen_libs")
    def test_status_false(self, mock_lib):

        """Function:  test_status_false

        Description:  Test with first status flag set to false.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.side_effect = [
            (False, "Error Message1"), (True, None), (True, None)]

        cfg, status_flag = isse_guard_transfer.load_cfg(self.cfg_name,
                                                        self.cfg_dir)
        self.assertEqual(
            (cfg.dissem_dir, cfg.transfer_dir, cfg.log_dir, status_flag),
            (self.dissem_dir2, self.transfer_dir, self.log_dir, False))

    @mock.patch("isse_guard_transfer.gen_libs")
    def test_good_check(self, mock_lib):

        """Function:  test_good_check

        Description:  Test with good directory checks.

        Arguments:

        """

        mock_lib.load_module.return_value = self.cfg
        mock_lib.chk_crt_dir.return_value = (True, None)

        cfg, status_flag = isse_guard_transfer.load_cfg(self.cfg_name,
                                                        self.cfg_dir)
        self.assertEqual(
            (cfg.dissem_dir, cfg.transfer_dir, cfg.log_dir, status_flag),
            (self.dissem_dir, self.transfer_dir, self.log_dir, True))


if __name__ == "__main__":
    unittest.main()
