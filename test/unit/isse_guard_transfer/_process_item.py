#!/usr/bin/python
# Classification (U)

"""Program:  _process_item.py

    Description:  Unit testing of _process_item in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/_process_item.py

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
            (input) job_name
            (input) job_log
            (input) log_type
            (input) log_format
            (input) log_time

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
            (input) data

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
            (input) data

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
        test_transfer_file_true
        test_transfer_file_false

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

                item = "test/unit/isse_guard_transfer/basefiles/proc.txt"

                self.sftp_dir = "/dir/path"
                self.review_dir = "/dir/review_dir"
                self.complete_dir = "/dir/complete_dir"
                self.file_types = {"text": {"MD5": True, "Base64": True}}
                self.job_log = "job_log"
                self.network = "CW"
                self.backup = True
                self.other_files = {item: True}
                self.other_file_types = {item: True}

        self.cfg_file = "file1.txt"
        self.cfg_dir = "/dir/path"
        self.sftp = SFTP(self.cfg_file, self.cfg_dir)
        self.isse = Isse()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.job = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                          "%m-%d-%YT%H:%M:%SZ|")
        self.item = "test/unit/isse_guard_transfer/basefiles/proc.txt"

    @mock.patch("isse_guard_transfer.gen_libs.make_md5_hash",
                mock.Mock(return_value="FileName"))
    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=True))
    def test_transfer_file_true(self):

        """Function:  test_transfer_file_true

        Description:  Test with transfer file is set to True.

        Arguments:

        """

        self.assertEqual(isse_guard_transfer._process_item(
            self.isse, self.sftp, self.logger, self.job, self.item), 1)

    @mock.patch("isse_guard_transfer.gen_libs.make_md5_hash",
                mock.Mock(return_value="FileName"))
    @mock.patch("isse_guard_transfer.transfer_file",
                mock.Mock(return_value=False))
    def test_transfer_file_false(self):

        """Function:  test_transfer_file_false

        Description:  Test with transfer file is set to False.

        Arguments:

        """

        self.assertEqual(isse_guard_transfer._process_item(
            self.isse, self.sftp, self.logger, self.job, self.item), 0)


if __name__ == "__main__":
    unittest.main()
