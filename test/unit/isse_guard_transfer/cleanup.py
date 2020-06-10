#!/usr/bin/python
# Classification (U)

"""Program:  cleanup.py

    Description:  Unit testing of cleanup in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/cleanup.py

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
        test_remove_fail -> Test with remove failing.
        test_one_file -> Test with one file check.

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

        class MoveToFile(object):

            """Class:  MoveToFile

            Description:  Class which is a representation of MoveToFile class.

            Methods:
                __init__ -> Initialize configuration environment.
                add_to_zip -> add_to_zip method.
                add_to_cleanup -> add_to_cleanup method.

            """

            def __init__(self, dissem_level):

                """Method:  __init__

                Description:  Initialization instance of the IsseGuard class.

                Arguments:
                    (input) dissem_level -> Dissemination level.

                """

                self.filname = None
                self.dissem_dir = "/dissem_dir/"
                self.dissem_level = dissem_level
                self.dissem_list = ["GEN-SCOL", "GEN-CW"]
                self.zip_file_path = "zip_file_path"
                self.cur_file_dir = "cur_file_dir"
                self.cur_file_name = "cur_file_name"
                self.cleanup_list = ["file1.txt"]
                self.dir_path = None

            def add_to_zip(self, filename):

                """Method:  add_to_zip

                Description:  add_to_zip method.

                Arguments:
                    (input) filename -> File name.

                """

                self.filname = filename

                return True

            def add_to_cleanup(self, dir_path):

                """Method:  add_to_cleanup

                Description:  add_to_cleanup method.

                Arguments:
                    (input) dir_path -> Directory path.

                """

                self.dir_path = dir_path

                return True

        self.dissem_level = "GEN-CW"
        self.move = MoveToFile(self.dissem_level)
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")

    @mock.patch("isse_guard_transfer.gen_libs.rm_file",
                mock.Mock(return_value=(True, "Error Message")))
    @mock.patch("isse_guard_transfer.gen_libs.chk_crt_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_remove_fail(self, mock_log):

        """Function:  test_remove_fail

        Description:  Test with remove failing.

        Arguments:

        """

        mock_log.return_value = self.logger

        self.assertFalse(isse_guard_transfer.cleanup(self.move, mock_log))

    @mock.patch("isse_guard_transfer.gen_libs.rm_file",
                mock.Mock(return_value=(False, None)))
    @mock.patch("isse_guard_transfer.gen_libs.chk_crt_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_one_file(self, mock_log):

        """Function:  test_one_file

        Description:  Test with one file check.

        Arguments:

        """

        mock_log.return_value = self.logger

        self.assertFalse(isse_guard_transfer.cleanup(self.move, mock_log))


if __name__ == "__main__":
    unittest.main()