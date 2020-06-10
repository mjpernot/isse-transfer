#!/usr/bin/python
# Classification (U)

"""Program:  _remove_files.py

    Description:  Unit testing of _remove_files in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/_remove_files.py

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
        __init__ -> Initialize configuration environment.
        log_err -> log_err method.
        log_warn -> log_warn method.
        log_info -> log_info method.
        log_close -> log_close method.

    """

    def __init__(self, job_name, job_log, log_type, log_format, log_time):

        """Method:  __init__

        Description:  Initialization instance of the IsseGuard class.

        Arguments:
            (input) job_name -> Instance name.
            (input) job_log -> Log name.
            (input) log_type -> Log type.
            (input) log_format -> Log format.
            (input) log_time -> Time format.

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
            (input) data -> Log entry.

        """

        self.data = data

    def log_warn(self, data):

        """Method:  log_warn

        Description:  log_warn method.

        Arguments:
            (input) data -> Log entry.

        """

        self.data = data

    def log_info(self, data):

        """Method:  log_info

        Description:  log_info method.

        Arguments:
            (input) data -> Log entry.

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
        setUp -> Initialize testing environment.
        test_remove_error -> Test with remove files error.
        test_remove_files -> Test with remove files.

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

    @mock.patch("isse_guard_transfer.gen_libs.rm_file",
                mock.Mock(return_value=(True, "Error Message")))
    def test_remove_error(self):

        """Function:  test_remove_error

        Description:  Test with remove files error.

        Arguments:

        """

        self.assertFalse(isse_guard_transfer._remove_files(self.isse,
                                                           self.logger))

    @mock.patch("isse_guard_transfer.gen_libs.rm_file",
                mock.Mock(return_value=(False, None)))
    def test_remove_files(self):

        """Function:  test_remove_files

        Description:  Test with remove files.

        Arguments:

        """

        self.assertFalse(isse_guard_transfer._remove_files(self.isse,
                                                           self.logger))


if __name__ == "__main__":
    unittest.main()
