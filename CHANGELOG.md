# Changelog
All notable changes to this project will be documented in this file.

The format is based on "Keep a Changelog".  This project adheres to Semantic Versioning.


## [3.0.5] - 2021-10-15
### Changed
- process:  Changed positional args to keywords args in process_files call.
- process_files:  Moved a number of positional args to keyword args.
- Documentation updates.


## [3.0.4] - 2020-04-29
### Fixed
- set_sftp_conn:  Set status to correct value if connection fails to open.
- main:  Fixed handling command line arguments from SonarQube scan finding.
- initate_process, run_program:  Fixed problem with mutable default arguments issue.
- process_media:  Incorrect reference to review_dir attribute.

### Added
- Added global variable for a printing template.
- \_remove_files:  Private function for process to decrease complexity.
- \_process_item:  Private function for process to decrease complexity.

### Changed
- process_images:  Replaced returning value with placeholder.
- process:  Replaced section of code with call to \_remove_files function.
- process:  Replaced section of code with call to \_process_item function.
- transfer_file:  Refactored if statements.
- transfer_file:  Removed check for job log.
- main:  Refactored if statements.
- run_program:  Removed redundant code.
- \_send, process, process_files:  Used global variable for template printing.
- initate_process:  Renamed \_\_send() to \_send().
- \_\_send:  Renamed function to single underscore \_send().
- Changed variables name to standard naming convention to most of the functions.
- Documentation updates.


## [3.0.3] - 2018-11-26
### Changed
- transfer_file: Added \*\*kwargs to parameter list.
- Documentation updates.


## [3.0.2] - 2018-05-25
### Fixed
- transfer_file, process_files, \_\_send, process_media:  Changed "gen_libs.mv_file" to "gen_libs.mv_file2" call.


## [3.0.1] - 2018-05-17
### Changed
- Documentation updates.


## [3.0.0] - 2018-04-20
Breaking Change

### Changed
- Changed "gen_libs" calls to new naming schema.
- move_to_reviewed, cleanup, transfer_file:  Replaced Chk_Crt_File with chk_crt_file and changed logic check code.
- load_cfg:  Replaced Chk_Crt_Dir with chk_crt_dir and changed logic check code.
- Changed "arg_parser" calls to new naming schema.
- Changed "isse_guard_class" calls to new naming schema.
- Changed "gen_class" calls to new naming schema.
- Changed function names from uppercase to lowercase.
- Setup single-source version control.


## [2.1.0] - 2018-04-19
### Changed
- Changed isse_guard_class module to sub-directory supporting library.
- Changed sftp_class module to sub-directory supporting library.

### Added
- Added single-source version control.


## [2.0.0] - 2017-10-23
Breaking Change

### Changed
- Add ability to convert certain file types to base64 format.
- Process:  Change/add arguments to Process_Files call.
- Process:  Change ISSE.file_types reference due to structural change.
- Process_Files:  Add input argument format.
- Process_Files:  Add check for base64 conversion of file.
- Documentation:  Add ISSE and SSH configuration file formats to help message and other minor changes in help message.


## [1.1.1] - 2017-09-27
### Fixed
- ISSE.other_files does not have capability to create MD5 files as there is no value setting for them.
- Process:  Add MD5 hash file argument to Process_Files call in processing ISSE.other_files.  Single file processing will call the MD5 creation function.


## [1.1.0] - 2017-09-25
### Changed
- Process:  Archiving of the LastRun.txt is no longer required.  Removing code and setting archive to False for LastRun.


## [1.0.1] - 2017-08-03
### Fixed
- Rename List_Files to List_Filter_Files due to duplicate function name in gen_libs library.
- Process_Files:  Rename List_Files to List_Filter_Files.


## [1.0.0] - 2017-07-31
- General release.


## [0.3.1] - 2017-07-28
### Changed
- Initate_Process:  Change date format of Logger class to YYYY-MM-DD.


## [0.3.0] - 2017-07-28
- Field test release.


## [0.2.1] - 2017-07-25
### Changed
- Process:  Refactor an 'if' statement for easier use.


## [0.2.0] - 2017-07-25
- Beta release.


## [0.1.0] - 2017-07-11
- Alpha release.

