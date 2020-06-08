#!/usr/bin/python
# Classification (U)

"""Program:  set_sftp_conn.py

    Description:  Unit testing of set_sftp_conn in isse_guard_transfer.py.

    Usage:
        test/unit/isse_guard_transfer/set_sftp_conn.py

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


class SFTP(object):

    """Class:  Isse

    Description:  Class which is a representation of SFTP class.

    Methods:
        __init__ -> Initialize configuration environment.
        open_conn -> open_conn method.
        chg_dir -> chg_dir method.
        get_pwd -> get_pwd method.

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
        self.dir_path = None

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

        return self.dir_path

    def get_pwd(self):

        """Method:  get_pwd

        Description:  get_pwd method.

        Arguments:

        """

        return self.dir_path


class UnitTest(unittest.TestCase):

    """Class:  UnitTest

    Description:  Class which is a representation of a unit testing.

    Methods:
        setUp -> Initialize testing environment.
        test_no_connection -> Test with no connection to SFTP..
        test_chg_dir_fails -> Test with change directory fails.
        test_good_check -> Test with good directory checks.

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
                __init__ -> Initialize configuration environment.

            """

            def __init__(self):

                """Method:  __init__

                Description:  Initialization instance of the IsseGuard class.

                Arguments:

                """

                self.sftp_dir = "/dir/path"

        self.isse = Isse()
        self.cfg_file = "config_file"
        self.cfg_dir = "/dirpath"
        self.sftp = SFTP(self.cfg_file, self.cfg_dir)

    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_no_connection(self, mock_sftp, mock_log):

        """Function:  test_no_connection

        Description:  Test with no connection to SFTP.

        Arguments:

        """

        self.sftp.is_connected = False

        mock_sftp.return_value = self.sftp
        mock_log.return_value = True

        sftp, status = isse_guard_transfer.set_sftp_conn(
            self.isse, self.cfg_file, self.cfg_dir, mock_log)

        self.assertEqual((sftp.is_connected, status), (False, False))

    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_chg_dir_fails(self, mock_sftp, mock_log):

        """Function:  test_chg_dir_fails

        Description:  Test with change directory fails.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_log.return_value = True

        self.isse.sftp_dir = False

        sftp, status = isse_guard_transfer.set_sftp_conn(
            self.isse, self.cfg_file, self.cfg_dir, mock_log)

        self.assertEqual((sftp.is_connected, status), (True, False))

    @mock.patch("isse_guard_transfer.gen_class.Logger")
    @mock.patch("isse_guard_transfer.sftp_class.SFTP")
    def test_good_check(self, mock_sftp, mock_log):

        """Function:  test_good_check

        Description:  Test with good directory checks.

        Arguments:

        """

        mock_sftp.return_value = self.sftp
        mock_log.return_value = True

        sftp, status = isse_guard_transfer.set_sftp_conn(
            self.isse, self.cfg_file, self.cfg_dir, mock_log)

        self.assertEqual((sftp.is_connected, status), (True, True))


if __name__ == "__main__":
    unittest.main()
