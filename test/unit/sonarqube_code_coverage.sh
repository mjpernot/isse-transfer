#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#       that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/help_message.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/load_cfg.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/process_files.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/set_sftp_conn.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/transfer_file.py


echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i
