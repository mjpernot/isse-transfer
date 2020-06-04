#!/usr/bin/python
# Classification (U)

"""Program:  process_files.py

    Description:  Unit testing of process_files in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/process_files.py

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
        test_transfer_fails -> Test with transfer fails.
        test_make_hash -> Test with make hash set to True.
        test_make_base64 -> Test with creating base64 file.
        test_one_file -> Test with one file check.
        taerDown -> Clean up of unit testing.

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
                __init__ -> Initialize configuration environment.
                open_conn -> open_conn method.
                chg_dir -> chg_dir method.
                get_pwd -> get_pwd method.
                put_file -> put_file method.

            """

            def __init__(self, cfg_file, cfg_dir):

                """Method:  __init__

                Description:  Initialization instance of the IsseGuard class.

                Arguments:
                    (input) cfg_file -> SFTP configuration file.
                    (input) cfg_dir -> Path to SFTP configuration file.

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
                    (input) dir_path -> Directory path.

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
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the IsseGuard class.

                Arguments:

                """

                self.sftp_dir = "/dir/path"
                self.review_dir = "/dir/review_dir"
                self.complete_dir = "test/unit/isse_guard_transfer/tmp"

        self.cfg_file = "file1.txt"
        self.cfg_dir = "/dir/path"
        self.sftp = SFTP(self.cfg_file, self.cfg_dir)
        self.isse = Isse()
        self.file_path = "/dirpath/file1.txt"
        self.filter_list = ["file1.zip"]
        self.file_list = \
            ["test/unit/isse_guard_transfer/basefiles/test_base64.txt"]
        self.basefile = \
            "test/unit/isse_guard_transfer/basefiles/test_base64_txt.64.txt"

    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=False))
    @mock.patch("isse_guard_transfer.gen_libs")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_transfer_fails(self, mock_sftp, mock_isse, mock_log, mock_lib):

        """Function:  test_transfer_fails

        Description:  Test with transfer fails.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_log.return_value = True
        mock_lib.list_filter_files.return_value = self.filter_list

        self.assertEqual(isse_guard_transfer.process_files(
            self.isse, self.sftp, mock_log, mock_log), 1)

    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.gen_libs")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_make_hash(self, mock_sftp, mock_isse, mock_log, mock_lib):

        """Function:  test_make_hash

        Description:  Test with make hash set to True.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_log.return_value = True
        mock_lib.list_filter_files.return_value = self.filter_list
        mock_lib.make_md5_hash.return_value = True

        self.assertEqual(isse_guard_transfer.process_files(
            self.isse, self.sftp, mock_log, mock_log, make_hash=True), 1)

    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.gen_libs")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_make_base64(self, mock_sftp, mock_isse, mock_log, mock_lib):

        """Function:  test_make_base64

        Description:  Test with creating base64 file.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_log.return_value = True
        mock_lib.list_filter_files.return_value = self.file_list

        self.assertEqual(isse_guard_transfer.process_files(
            self.isse, self.sftp, mock_log, mock_log, make_base64=True), 1)

    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.gen_libs")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_one_file(self, mock_sftp, mock_isse, mock_log, mock_lib):

        """Function:  test_one_file

        Description:  Test with one file check.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_log.return_value = True
        mock_lib.list_filter_files.return_value = self.filter_list

        self.assertEqual(isse_guard_transfer.process_files(
            self.isse, self.sftp, mock_log, mock_log), 1)

    def tearDown(self):

        """Function:  tearDown

        Description:  Clean up of unit testing.

        Arguments:

        """

        if os.path.isfile(self.basefile):
            os.remove(self.basefile)
        


if __name__ == "__main__":
    unittest.main()
