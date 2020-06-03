#!/usr/bin/python
# Classification (U)

"""Program:  process_zip.py

    Description:  Unit testing of process_zip in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/process_zip.py

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
        test_incorrect_level -> Test with incorrect dissem level.
        test_newer_file -> Test with newer file check.
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
                self.dir_path = None
                self.files_to_zip = ["Files"]

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
                    (input) filename -> File name.

                """

                self.dir_path = dir_path

                return True

        self.dissem_level = "GEN-CW"
        self.dissem_level2 = "BAD-LEVEL"
        self.move = MoveToFile(self.dissem_level)
        self.move2 = MoveToFile(self.dissem_level2)
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")

    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_incorrect_level(self, mock_log):

        """Function:  test_incorrect_level

        Description:  Test with incorrect dissem level.

        Arguments:

        """

        mock_log.return_value = self.logger

        self.assertFalse(isse_guard_transfer.process_zip(self.move2, mock_log))

    @mock.patch("isse_guard_transfer.os.path")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_newer_file(self, mock_log, mock_os):

        """Function:  test_newer_file

        Description:  Test with newer file check.

        Arguments:

        """

        mock_log.return_value = self.logger
        mock_os.isfile.return_value = True
        mock_os.getctime.side_effect = [1, 2]

        self.assertFalse(isse_guard_transfer.process_zip(self.move, mock_log))

    @mock.patch("isse_guard_transfer.gen_libs.make_zip",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.os.path")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    def test_one_file(self, mock_log, mock_os):

        """Function:  test_one_file

        Description:  Test with one file check.

        Arguments:

        """

        mock_log.return_value = self.logger
        mock_os.isfile.return_value = False

        self.assertFalse(isse_guard_transfer.process_zip(self.move, mock_log))


if __name__ == "__main__":
    unittest.main()
