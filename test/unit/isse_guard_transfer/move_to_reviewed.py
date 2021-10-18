#!/usr/bin/python
# Classification (U)

"""Program:  move_to_reviewed.py

    Description:  Unit testing of move_to_reviewed in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/move_to_reviewed.py

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
        test_one_file

    """

    def setUp(self):

        """Function:  setUp

        Description:  Initialization for unit testing.

        Arguments:

        """

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
                self.dissem_dir = "/dir/dissem_dir"

        class MoveTo(object):

            """Class:  MoveTo

            Description:  Class which is a representation of MoveTo class.

            Methods:
                __init__
                get_files

            """

            def __init__(self, dissem_dir):

                """Method:  __init__

                Description:  Initialization instance of the IsseGuard class.

                Arguments:

                """

                self.dissem_dir = dissem_dir
                self.file_list = ["/dir/file1.txt"]

            def get_files(self):

                """Method:  get_files

                Description:  get_files method.

                Arguments:

                """

                return True

        class MoveToFile(object):

            """Class:  MoveToFile

            Description:  Class which is a representation of MoveToFile class.

            Methods:
                __init__
                parse_xml_file
                process_product
                add_to_zip
                add_to_cleanup

            """

            def __init__(self, file_path, review_dir, dissem_dir):

                """Method:  __init__

                Description:  Initialization instance of the IsseGuard class.

                Arguments:

                """

                self.file_path = file_path
                self.review_dir = review_dir
                self.dissem_dir = dissem_dir
                self.xml_file_name = "xml_file_name"
                self.xml_file_path = "xml_file_path"
                self.zip_file_path = "zip_file_path"
                self.cur_file_dir = "cur_file_dir"
                self.cur_file_name = "cur_file_name"
                self.product_line = "product_line"
                self.images = "images"
                self.media = "media"
                self.product_list = ["product_line"]
                self.filename = None
                self.object_id = "object_id"
                self.dissem_level = "dissem_level"

            def parse_xml_file(self):

                """Method:  parse_xml_file

                Description:  parse_xml_file method.

                Arguments:

                """

                return True

            def process_product(self):

                """Method:  process_product

                Description:  process_product method.

                Arguments:

                """

                return True

            def add_to_zip(self, dir_path):

                """Method:  add_to_zip

                Description:  add_to_zip method.

                Arguments:

                """

                self.filename = dir_path

                return True

            def add_to_cleanup(self, dir_path):

                """Method:  add_to_cleanup

                Description:  add_to_cleanup method.

                Arguments:

                """

                self.filename = dir_path

                return True

        self.dissem_level = "GEN-CW"
        self.file_path = "/dir/file1.txt"
        self.review_dir = "/dir/review_dir"
        self.dissem_dir = "/dir/dissem_dir"
        self.moveto = MoveToFile(self.file_path, self.review_dir,
                                 self.dissem_dir)
        self.move = MoveTo(self.dissem_dir)
        self.isse = Isse()
        self.logger = Logger("Name", "Name", "INFO", "%(asctime)s%(message)s",
                             "%m-%d-%YT%H:%M:%SZ|")
        self.file_path = "/dirpath/file1.txt"

    @mock.patch("isse_guard_transfer.gen_libs.chk_crt_file",
                mock.Mock(return_value=(True, None)))
    @mock.patch("isse_guard_transfer.cleanup",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.process_zip",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.process_media",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.process_images",
                mock.Mock(return_value=True))
    @mock.patch("isse_guard_transfer.isse_guard_class.MoveTo")
    @mock.patch("isse_guard_transfer.isse_guard_class.MoveToFile")
    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.isse_guard_class.IsseGuard")
    def test_one_file(self, mock_isse, mock_log, mock_moveto, mock_move):

        """Function:  test_one_file

        Description:  Test with one file check.

        Arguments:

        """

        mock_isse.return_value = self.isse
        mock_log.return_value = self.logger
        mock_moveto.return_value = self.moveto
        mock_move.return_value = self.move

        self.assertFalse(isse_guard_transfer.move_to_reviewed(self.isse,
                                                              self.logger))


if __name__ == "__main__":
    unittest.main()
