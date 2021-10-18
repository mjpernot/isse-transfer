#!/usr/bin/python
# Classification (U)

"""Program:  initate_process.py

    Description:  Unit testing of initate_process in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/initate_process.py

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
        test_action_wrong
        test_sftp_fail
        test_sftp_down
        test_send_no_files
        test_send
        test_move
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
                close_conn

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

            def close_conn(self):

                """Method:  close_conn

                Description:  get_pwdclose_connmethod.

                Arguments:

                """

                return True

        class Isse(object):

            """Class:  Isse

            Description:  Class which is a representation of IsseGuard class.

            Methods:
                __init__
                set_other_files

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
                self.prog_log = "prog_log"
                self.name = "name"
                self.transfer_dir = "/dir/transfer_dir"
                self.action = "process"
                self.files = "/path/file"

            def set_other_files(self):

                """Method:  set_other_files

                Description:  set_other_files emthod.

                Arguments:

                """

                return True

        self.args_array = {"-s": True, "-d": True}
        self.cfg_file = "file1.txt"
        self.cfg_dir = "/dir/path"
        self.sftp = SFTP(self.cfg_file, self.cfg_dir)
        self.isse = Isse()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.file_path = "/dirpath/file1.txt"

    @mock.patch("isse_guard_transfer.set_sftp_conn")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_action_wrong(self, mock_log, mock_ftp):

        """Function:  test_action_wrong

        Description:  Test with incorrect action set.

        Arguments:

        """

        self.isse.action = "bad_action"

        mock_ftp.return_value = (self.sftp, True)
        mock_log.return_value = self.logger

        with gen_libs.no_std_out():
            self.assertFalse(isse_guard_transfer.initate_process(
                self.args_array, self.isse))

    @mock.patch("isse_guard_transfer.move_to_reviewed",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.set_sftp_conn")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_sftp_fail(self, mock_log, mock_ftp):

        """Function:  test_sftp_fail

        Description:  Test with sftp fails change directory.

        Arguments:

        """

        self.isse.action = "process"

        mock_ftp.return_value = (self.sftp, False)
        mock_log.return_value = self.logger

        with gen_libs.no_std_out():
            self.assertFalse(isse_guard_transfer.initate_process(
                self.args_array, self.isse))

    @mock.patch("isse_guard_transfer.move_to_reviewed",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.set_sftp_conn")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_sftp_down(self, mock_log, mock_ftp):

        """Function:  test_sftp_down

        Description:  Test with sftp connection down.

        Arguments:

        """

        self.isse.action = "process"
        self.sftp.is_connected = False

        mock_ftp.return_value = (self.sftp, True)
        mock_log.return_value = self.logger

        with gen_libs.no_std_out():
            self.assertFalse(isse_guard_transfer.initate_process(
                self.args_array, self.isse))

    @mock.patch("isse_guard_transfer.move_to_reviewed",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.set_sftp_conn")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_send_no_files(self, mock_log, mock_ftp):

        """Function:  test_send_no_files

        Description:  Test with send option, but no files.

        Arguments:

        """

        self.isse.action = "send"
        self.isse.files = None

        mock_ftp.return_value = (self.sftp, True)
        mock_log.return_value = self.logger

        with gen_libs.no_std_out():
            self.assertFalse(isse_guard_transfer.initate_process(
                self.args_array, self.isse))

    @mock.patch("isse_guard_transfer._send", mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.move_to_reviewed",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.set_sftp_conn")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_send(self, mock_log, mock_ftp):

        """Function:  test_send

        Description:  Test with send option.

        Arguments:

        """

        self.isse.action = "send"

        mock_ftp.return_value = (self.sftp, True)
        mock_log.return_value = self.logger

        with gen_libs.no_std_out():
            self.assertFalse(isse_guard_transfer.initate_process(
                self.args_array, self.isse))

    @mock.patch("isse_guard_transfer.move_to_reviewed",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_move(self, mock_log):

        """Function:  test_move

        Description:  Test with move approved option.

        Arguments:

        """

        self.isse.action = "moveapproved"

        mock_log.return_value = self.logger

        self.assertFalse(isse_guard_transfer.initate_process(self.args_array,
                                                             self.isse))

    @mock.patch("isse_guard_transfer.process", mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.set_sftp_conn")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_one_file(self, mock_log, mock_ftp):

        """Function:  test_one_file

        Description:  Test with one file check.

        Arguments:

        """

        mock_log.return_value = self.logger
        mock_ftp.return_value = (self.sftp, True)

        self.assertFalse(isse_guard_transfer.initate_process(self.args_array,
                                                             self.isse))


if __name__ == "__main__":
    unittest.main()
