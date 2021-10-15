#!/usr/bin/python
# Classification (U)

"""Program:  process.py

    Description:  Unit testing of process in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/process.py

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


class Logger(object):

    """Class:  Logger

    Description:  Class which is a representation of gen_class.Logger class.

    Methods:
        __init__
        log_err
        log_warn
        log_info
        log_close

    """

    def __init__(self, job_name, job_log, log_type, log_format, log_time):

        """Method:  __init__

        Description:  Initialization instance of the IsseGuard class.

        Arguments:

        """

        self.job_name = job_name
        self.job_log = job_log
        self.log_type = log_type
        self.log_format = log_format
        self.log_time = log_time
        self.data = None

    def log_err(self, data):

        """Method:  log_err

        Description:  log_err method.

        Arguments:

        """

        self.data = data

    def log_warn(self, data):

        """Method:  log_warn

        Description:  log_warn method.

        Arguments:
            (input) data

        """

        self.data = data

    def log_info(self, data):

        """Method:  log_info

        Description:  log_info method.

        Arguments:

        """

        self.data = data

    def log_close(self):

        """Method:  log_close

        Description:  log_close method.

        Arguments:

        """

        return True


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp
        test_bices_error
        test_bices_files
        test_no_files
        test_transfer_file_true-> Test with transfer file is set to True.
        test_is_file
        test_pattern_search
        test_one_file

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
                self.review_dir = "/dir/review_dir"
                self.complete_dir = "/dir/complete_dir"
                self.file_types = {"text": {"MD5": True, "Base64": True}}
                self.job_log = "job_log"
                self.network = "CW"
                self.backup = True
                self.other_files = {"/dir/file.xml": True}
                self.other_file_types = {"/dir/file.xml": True}

        self.cfg_file = "file1.txt"
        self.cfg_dir = "/dir/path"
        self.sftp = SFTP(self.cfg_file, self.cfg_dir)
        self.isse = Isse()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.file_path = "/dirpath/file1.txt"
        self.other_files = \
            {"test/unit/isse_guard_transfer/basefiles/proc.txt": True}

    @mock.patch("isse_guard_transfer.gen_libs.rm_file",
                mock.Mock(return_value=(True, "Error Message")))
    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=False))
    @mock.patch("isse_guard_transfer.re.search", mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.process_files", mock.Mock(return_value=1))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_bices_error(self, mock_sftp, mock_isse, mock_job):

        """Function:  test_bices_error

        Description:  Test with bices remove error.

        Arguments:

        """

        self.isse.network = "BICES"

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_job.return_value = self.logger

        self.assertFalse(isse_guard_transfer.process(self.isse, self.sftp,
                                                     self.logger))

    @mock.patch("isse_guard_transfer.gen_libs.rm_file",
                mock.Mock(return_value=(False, None)))
    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=False))
    @mock.patch("isse_guard_transfer.re.search", mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.process_files", mock.Mock(return_value=1))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_bices_files(self, mock_sftp, mock_isse, mock_job):

        """Function:  test_bices_files

        Description:  Test with bices files.

        Arguments:

        """

        self.isse.network = "BICES"

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_job.return_value = self.logger

        self.assertFalse(isse_guard_transfer.process(self.isse, self.sftp,
                                                     self.logger))

    @mock.patch("isse_guard_transfer.gen_libs.make_md5_hash",
                mock.Mock(return_value="FileName"))
    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=False))
    @mock.patch("isse_guard_transfer.re.search", mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.process_files", mock.Mock(return_value=0))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_no_files(self, mock_sftp, mock_isse, mock_job):

        """Function:  test_no_files

        Description:  Test with no files processed.

        Arguments:

        """

        self.isse.other_files = self.other_files
        self.isse.other_file_types = self.other_files

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_job.return_value = self.logger

        self.assertFalse(isse_guard_transfer.process(self.isse, self.sftp,
                                                     self.logger))

    @mock.patch("isse_guard_transfer.gen_libs.make_md5_hash",
                mock.Mock(return_value="FileName"))
    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.re.search", mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.process_files", mock.Mock(return_value=1))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_transfer_file_true(self, mock_sftp, mock_isse, mock_job):

        """Function:  test_transfer_file_true

        Description:  Test with transfer file is set to True.

        Arguments:

        """

        self.isse.other_files = self.other_files
        self.isse.other_file_types = self.other_files

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_job.return_value = self.logger

        self.assertFalse(isse_guard_transfer.process(self.isse, self.sftp,
                                                     self.logger))

    @mock.patch("isse_guard_transfer.gen_libs.make_md5_hash",
                mock.Mock(return_value="FileName"))
    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=False))
    @mock.patch("isse_guard_transfer.re.search", mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.process_files", mock.Mock(return_value=1))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_is_file(self, mock_sftp, mock_isse, mock_job):

        """Function:  test_is_file

        Description:  Test with is file check.

        Arguments:

        """

        self.isse.other_files = self.other_files
        self.isse.other_file_types = self.other_files

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_job.return_value = self.logger

        self.assertFalse(isse_guard_transfer.process(self.isse, self.sftp,
                                                     self.logger))

    @mock.patch("isse_guard_transfer.re.search", mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=False))
    @mock.patch("isse_guard_transfer.re.search", mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.process_files", mock.Mock(return_value=1))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_pattern_search(self, mock_sftp, mock_isse, mock_job):

        """Function:  test_pattern_search

        Description:  Test with pattern search.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_job.return_value = self.logger

        self.assertFalse(isse_guard_transfer.process(
            self.isse, self.sftp, self.logger, pattern="String"))

    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=False))
    @mock.patch("isse_guard_transfer.re.search", mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.process_files", mock.Mock(return_value=1))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_one_file(self, mock_sftp, mock_isse, mock_job):

        """Function:  test_one_file

        Description:  Test with one file check.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_isse.return_value = self.isse
        mock_job.return_value = self.logger

        self.assertFalse(isse_guard_transfer.process(self.isse, self.sftp,
                                                     self.logger))


if __name__ == "__main__":
    unittest.main()
