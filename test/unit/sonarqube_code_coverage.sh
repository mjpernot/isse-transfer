#!/bin/bash
# Unit test code coverage for SonarQube to cover all modules.
# This will run the Python code coverage module against all unit test modules.
# This will show the amount of code that was tested and which lines of code
#       that was skipped during the test.

coverage erase

echo ""
echo "Running unit test modules in conjunction with coverage"
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/_process_item.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/_send.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/cleanup.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/help_message.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/initate_process.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/load_cfg.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/main.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/move_to_reviewed.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/process.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/process_files.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/process_images.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/process_media.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/process_zip.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/run_program.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/set_sftp_conn.py
coverage run -a --source=isse_guard_transfer test/unit/isse_guard_transfer/transfer_file.py


echo ""
echo "Producing code coverage report"
coverage combine
coverage report -m
coverage xml -i
