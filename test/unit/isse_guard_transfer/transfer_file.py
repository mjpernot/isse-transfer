#!/usr/bin/python
# Classification (U)

"""Program:  transfer_file.py

    Description:  Unit testing of transfer_file in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/transfer_file.py

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
        setUp
        test_status_fail
        test_remove_fail
        test_keep_files
        test_no_sftp_dir
        test_no_connect
        test_good_check

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class SFTP(object):

            """Class:  Isse

            Description:  Class which is a representation of SFTP class.

            Methods:
                __init__
                open_conn
                chg_dir
                get_pwd
                put_file

            """

            def __init__(self, cfg_file, cfg_dir):

                """Method:  __init__

                Description:  Initialization instance of the IsseGuard class.

                Arguments:

                """

                self.cfg_file = cfg_file
                self.cfg_dir = cfg_dir
                self.is_connected = True
                self.dir_path = cfg_dir
                self.source = None
                self.destination = None

            def open_conn(self):

                """Method:  open_conn

                Description:  open_conn method.

                Arguments:

                """

                return True

            def chg_dir(self, dir_path):

                """Method:  chg_dir

                Description:  chg_dir method.

                Arguments:

                """

                self.dir_path = dir_path

                return True

            def get_pwd(self):

                """Method:  get_pwd

                Description:  get_pwd method.

                Arguments:

                """

                return self.dir_path

            def put_file(self, source, destination):

                """Method:  put_file

                Description:  put_file method.

                Arguments:

                """

                self.source = source
                self.destination = destination

                return True

        class Isse(object):

            """Class:  Isse

            Description:  Class which is a representation of IsseGuard class.

            Methods:
                __init__

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the IsseGuard class.

                Arguments:

                """

                self.sftp_dir = "/dir/path"
                self.complete_dir = "/dir/complete_dir"

        self.cfg_file = "file1.txt"
        self.cfg_dir = "/dir/path"
        self.sftp = SFTP(self.cfg_file, self.cfg_dir)
        self.isse = Isse()
        self.file_path = "/dirpath/file1.txt"

    @mock.patch("isse_guard_transfer.gen_libs.chk_crt_file",
                mock.Mock(return_value=(False, "Error Message2")))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_status_fail(self, mock_sftp, mock_isse, mock_log):

        """Function:  test_status_fail

        Description:  Test with status set to false.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_log.return_value = True

        self.assertFalse(isse_guard_transfer.transfer_file(
            self.isse, self.sftp, mock_log, mock_log, self.file_path))

    @mock.patch("isse_guard_transfer.gen_libs.rm_file",
                mock.Mock(return_value=(True, "Error Message")))
    @mock.patch("isse_guard_transfer.gen_libs.chk_crt_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_remove_fail(self, mock_sftp, mock_isse, mock_log):

        """Function:  test_remove_fail

        Description:  Test with remove file fails.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_log.return_value = True

        self.assertTrue(isse_guard_transfer.transfer_file(
            self.isse, self.sftp, mock_log, mock_log, self.file_path))

    @mock.patch("isse_guard_transfer.gen_libs.mv_file2",
                mock.Mock(return_value=(False, None)))
    @mock.patch("isse_guard_transfer.gen_libs.chk_crt_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_keep_files(self, mock_sftp, mock_isse, mock_log):

        """Function:  test_keep_files

        Description:  Test with keep files set to True.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_log.return_value = True

        self.assertTrue(isse_guard_transfer.transfer_file(
            self.isse, self.sftp, mock_log, mock_log, self.file_path,
            keep_file=True))

    @mock.patch("isse_guard_transfer.gen_libs.chk_crt_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_no_sftp_dir(self, mock_sftp, mock_isse, mock_log):

        """Function:  test_no_sftp_dir

        Description:  Test with no ftp directory.

        Arguments:

        """

        self.isse.sftp_dir = "/dir/no_path"

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_log.return_value = True

        self.assertFalse(isse_guard_transfer.transfer_file(
            self.isse, self.sftp, mock_log, mock_log, self.file_path))

    @mock.patch("isse_guard_transfer.gen_libs.chk_crt_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_no_connect(self, mock_sftp, mock_isse, mock_log):

        """Function:  test_no_connect

        Description:  Test with no connection to SFTP.

        Arguments:

        """

        self.sftp.is_connected = False

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_log.return_value = True

        self.assertFalse(isse_guard_transfer.transfer_file(
            self.isse, self.sftp, mock_log, mock_log, self.file_path))

    @mock.patch("isse_guard_transfer.gen_libs.rm_file",
                mock.Mock(return_value=(False, None)))
    @mock.patch("isse_guard_transfer.gen_libs.chk_crt_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_good_check(self, mock_sftp, mock_isse, mock_log):

        """Function:  test_good_check

        Description:  Test with good directory checks.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_log.return_value = True

        self.assertTrue(isse_guard_transfer.transfer_file(
            self.isse, self.sftp, mock_log, mock_log, self.file_path))


if __name__ == "__main__":
    unittest.main()
