#!/bin/bash
# Unit testing program for the program module.
# This will run all the units tests for this program.
# Will need to run this from the base directory where the module file
#   is located at.

echo ""
echo "Unit testing..."
test/unit/isse_guard_transfer/_process_item.py
test/unit/isse_guard_transfer/_remove_files.py
test/unit/isse_guard_transfer/_send.py
test/unit/isse_guard_transfer/cleanup.py
test/unit/isse_guard_transfer/help_message.py
test/unit/isse_guard_transfer/initate_process.py
test/unit/isse_guard_transfer/load_cfg.py
test/unit/isse_guard_transfer/main.py
test/unit/isse_guard_transfer/move_to_reviewed.py
test/unit/isse_guard_transfer/process.py
test/unit/isse_guard_transfer/process_files.py
test/unit/isse_guard_transfer/process_images.py
test/unit/isse_guard_transfer/process_media.py
test/unit/isse_guard_transfer/process_zip.py
test/unit/isse_guard_transfer/run_program.py
test/unit/isse_guard_transfer/set_sftp_conn.py
test/unit/isse_guard_transfer/transfer_file.py
