#!/usr/bin/python
# Classification (U)

"""Program:  isse_guard_transfer.py

    Description:  Process and send pre-reviewed files in a "reviewed"
        directory to an ISSE Guard system (which will send them to a specified
        security enclave).  Also process and package pre-approved documents and
        send them to a "reviewed" directory.

    Usage:
        isse_guard_transfer.py -c file | -d path | -s file |
            -A {process | moveapproved | send} [-f {path | [path1, path2]} |
            -N {SIPR | CW | BICES} |
            -k {True | False}
            [-v | -h]

    Arguments:
        -A {process | moveapproved | send} => Action to perform.
            process -> Process files in a "reviewed" directory and ftp them to
                an ISSE Guard server.
            moveapproved -> Process files in an "IS" directory, package them
                up, and move them to a "reviewed" directory.
            send -> Do not use.  Used for debugging purposes only.
        -s file => SFTP configuration file.  Required argument.
        -N value => Target network to transfer to.  Required argument.
            Values:  SIPR | CW | BICES
        -c file => ISSE Guard configuration file.  Required argument.
        -d dir path => Directory path for option '-c'. Required argument.
        -f path | [path1, path2, ...] => File path or array of filepaths.
            Required for the 'send' option for the -A argument.
        -k True | False => Archive the source files from the files argument,
            otherwise they will be deleted.
        -v => Display version of this program.
        -h => Help and usage message.

        NOTE 1:  -v or -h overrides the other options.

    Notes:
        The two configurationmod/conversion files below are required to run
        this program.  Create them and replace those variables
        (i.e. <VARIABLE>) with a value.

        ISSE Guard configuration file format (config/isse_guard.py.TEMPLATE).
        The configuration file format for the ISSE Guard is for the initial
        environment setup for the program.
            # Dissem_Dir -> Base directory for "moveapproved" option.
            dissem_dir = "DIRECTORY_PATH"
            # Transfer_Dir -> Base directory to security transfer directories.
            transfer_dir = "DIRECTORY_PATH"
            # Log_Dir -> Directory path where program log will be written to.
            log_dir = "DIRECTORY_PATH"
            # Backup -> True archives the files,  False will delete them.
            backup = True

        SSH/SFTP configuration file format (config/ssh_config.py.TEMPLATE).
        The configuration file format is for SFTP connection setup to ISSE
        Guard server.
            username = "USERNAME"
            password = "PSWD"
            host = "SERVER_NAME"
            port = 22
            # Log_File -> Directory path to Paramiko log file location.
            log_file = "DIRECTORY_PATH/paramiko.log"

    Example:
        isse_guard_transfer.py -c isse_guard -d config -s ssh_config -N SIPR
            -A process

"""

# Libraries and Global Variables

# Standard
import os
import sys
import re

# Third party
import pathlib2
import base64

# Local
import lib.arg_parser as arg_parser
import lib.gen_libs as gen_libs
import lib.gen_class as gen_class
import isse_lib.isse_guard_class as isse_guard_class
import sftp_lib.sftp_class as sftp_class
import version

__version__ = version.__version__


def help_message(**kwargs):

    """Function:  help_message

    Description:  Displays the program's docstring which is the help and usage
        message when -h option is selected.

    Arguments:

    """

    print(__doc__)


def load_cfg(cfg_name, cfg_dir, **kwargs):

    """Function:  load_cfg

    Description:  Load the ISSE Guard configuration file and validate the
        contents of the file.

    Arguments:
        (input) cfg_name -> Configuration file name.
        (input) cfg_dir -> Directory path to the configuration file.
        (output) cfg -> Configuration module handler.
        (output) status_flag -> True|False - successfully validate config file.

    """

    status_flag = True

    cfg = gen_libs.load_module(cfg_name, cfg_dir)

    status, msg = gen_libs.chk_crt_dir(cfg.dissem_dir, write=True, read=True)

    if not status:
        status_flag = False

    elif not cfg.dissem_dir.endswith(os.path.sep):
        cfg.dissem_dir = cfg.dissem_dir + os.path.sep

    status, msg = gen_libs.chk_crt_dir(cfg.transfer_dir, write=True, read=True)

    if not status:
        status_flag = False

    elif not cfg.transfer_dir.endswith(os.path.sep):
        cfg.transfer_dir = cfg.transfer_dir + os.path.sep

    if not isinstance(cfg.backup, bool):
        print("Error boolean check on Backup: %s" % (cfg.backup))
        status_flag = False

    status, msg = gen_libs.chk_crt_dir(cfg.log_dir, write=True, read=True)

    if not status:
        status_flag = False

    elif not cfg.log_dir.endswith(os.path.sep):
        cfg.log_dir = cfg.log_dir + os.path.sep

    return cfg, status_flag


def set_sftp_conn(isse, cfg_file, cfg_dir, log, **kwargs):

    """Function:  set_sftp_conn

    Description:  Create SFTP class/connection and set destination path in the
        SFTP connection.

    Arguments:
        (input) isse -> ISSE Guard class instance.
        (input) cfg_file -> SFTP configuration file.
        (input) cfg_dir -> Directory path to SFTP configuration file.
        (input) log -> Log class instance.
        (output) sftp -> SFTP class.
        (output) status -> True|False - Successfully changed directory.

    """

    status = True
    sftp = sftp_class.SFTP(cfg_file, cfg_dir)
    sftp.open_conn()

    if sftp.is_connected:
        log.log_info("SFTP Connection created")

        if sftp.chg_dir(isse.sftp_dir):
            log.log_info("SFTP destination set to: %s" % sftp.get_pwd())

        else:
            log.log_err("SFTP change directory failed: %s" % isse.sftp_dir)
            status = False

    else:
        log.log_err("SFTP open connection failed.")

    return sftp, status


def transfer_file(isse, sftp, log, job, file_path, keep_file=False, **kwargs):

    """Function:  transfer_file

    Description:  Initiate transfer of file to ISSE Guard server.

    Arguments:
        (input) isse -> ISSE Guard class instance.
        (input) sftp -> SFTP class instance.
        (input) log -> Log class instance.
        (input) job -> Log class instance.
        (input) file_path -> Full path and file name being processed.
        (input) keep_file -> True|False - on whether to archive the file.
        (output) True|False -> Succesful completion of transfer.

    """

    file_name = os.path.basename(file_path)

    status, err_msg = gen_libs.chk_crt_file(file_path, write=True, read=True)

    if status:

        if sftp.is_connected and isse.sftp_dir in sftp.get_pwd():
            log.log_info("Transfer => %s" % file_path)
            log.log_info("\tto -> %s" % isse.sftp_dir)

            sftp.put_file(file_path, sftp.get_pwd() + "/" + file_name)
            log.log_info("... Transfer complete.")

        else:

            if not sftp.is_connected:
                log.log_warn("SFTP Connection is not connected.")

            else:
                log.log_err("Directory paths do not match.")
                log.log_err("\tDest Path: %s" % isse.sftp_dir)
                log.log_err("\tCurrent Path: %s" % sftp.get_pwd())

            return False

        log.log_info("Transferred File: %s" % file_path)

        if job:
            job.log_info("%s" % file_name)

        if keep_file:
            log.log_info("Move to complete: %s" % file_name)

            gen_libs.mv_file2(file_path, isse.complete_dir)
            log.log_info("Move to completed: %s" % file_path)

        else:
            log.log_info("Delete: %s" % file_name)

            err_flag, err_msg = gen_libs.rm_file(file_path)

            if err_flag:
                log.log_warn("%s" % str(err_msg))

            else:
                log.log_info("Deleted: %s" % file_path)

    else:
        log.log_warn("File not found: %s" % file_path)
        log.log_warn("Reason:  %s" % err_msg)
        return False

    return True


def process_files(isse, sftp, log, job, file_filter="*.zip", keep_file=False,
                  make_hash=False, make_base64=False, **kwargs):

    """Function:  process_files

    Description:  Processes individual files in a directory using filtering to
        determine whether a MD5 file is created for the file and if the file is
        converted to base64 file format.

    Arguments:
        (input) isse -> ISSE Guard class instance.
        (input) sftp -> SFTP class instance.
        (input) log -> Log class instance.
        (input) job -> Log class instance.
        (input) file_filter -> File name or wildcard expansion file name.
        (input) keep_file -> True|False - on whether to archive the file.
        (input) make_hash -> True|False - create a MD5 hash for the file.
        (input) make_base64 -> True|False - convert file to base64 format.
        (output) cnt -> Number of files processed.

    """

    str_val = "=" * 80
    file_list = gen_libs.list_filter_files(isse.review_dir, file_filter)
    cnt = len(file_list)
    file_cnt = 0

    log.log_info("process_files::start")
    log.log_info("Pre-count %s: %s files" % (file_filter, str(cnt)))

    for file_path in file_list:
        log.log_info("Processing: %s" % file_path)

        if make_base64:
            f_base, f_ext = os.path.splitext(file_path)
            base64_file = f_base + f_ext[:1].replace(".", "_") + f_ext[1:] \
                + ".64.txt"

            log.log_info("Base64 convert: %s to %s" % (file_path, base64_file))
            base64.encode(open(file_path, 'rb'), open(base64_file, 'wb'))

            log.log_info("Move to complete: %s" % os.path.basename(file_path))
            gen_libs.mv_file2(file_path, isse.complete_dir)
            log.log_info("Move to completed: %s" % file_path)

            file_path = base64_file

        if make_hash:
            hash_file = gen_libs.make_md5_hash(file_path)
            log.log_info("Make hash => %s" % hash_file)

        if not transfer_file(isse, sftp, log, job, file_path,
                             keep_file):
            log.log_err("Failed to transfer: %s" % file_path)

        else:
            file_cnt += 1

    log.log_info("Post-count %s: %s files" % (file_filter, str(file_cnt)))

    if cnt != file_cnt:
        log.log_warn("Counts do not match")

    log.log_info("process_files::end")
    log.log_info("%s" % str_val)

    return cnt


def process(isse, sftp, log, **kwargs):

    """Function:  process

    Description:  Handle the transfer of different file types for a given
        network to the ISSE Guard server.

    Arguments:
        (input) isse -> ISSE Guard class instance.
        (input) sftp -> SFTP class instance.
        (input) log -> Log class instance.
        (input) **kwargs:
            pattern -> pattern matching string for other filenames

    """

    file_cnt = 0
    keep_log = False
    pattern = kwargs.get("pattern", False)
    job = gen_class.Logger(isse.job_log, isse.job_log, "INFO",
                           "%(asctime)s%(message)s", "%m-%d-%YT%H:%M:%SZ|")

    log.log_info("process::start")
    log.log_info("Processing: %s %s" % (isse.network, isse.review_dir))

    for f_type in isse.file_types:
        file_cnt += process_files(isse, sftp, log, job, f_type,
                                  isse.backup, isse.file_types[f_type]["MD5"],
                                  isse.file_types[f_type]["Base64"])

    # Handle MD5 files after all other files have been processed.
    if isse.network in ["SIPR", "CW"]:
        process_files(isse, sftp, log, job, "*.md5.txt", False, False)

    for item in isse.other_files:

        if pattern and re.search(pattern, item):
            file_cnt += process_files(isse, sftp, log, job, item,
                                      isse.other_files[item],
                                      isse.other_file_types[item])

        elif pathlib2.Path(item).is_file():

            if isse.other_file_types[item]:
                hash_file = gen_libs.make_md5_hash(item)
                log.log_info("Make hash => %s" % hash_file)

            if transfer_file(isse, sftp, log, job, item,
                             isse.other_files[item]):
                file_cnt += 1

            else:
                log.log_err("Failed to transfer: %s" % item)

        else:
            log.log_info("Other_Files: processing %s" % item)
            tmp_cnt = process_files(isse, sftp, log, job, item,
                                    isse.other_files[item],
                                    isse.other_file_types[item])
            file_cnt += tmp_cnt
            log.log_info("Other_Files: %s count %s" % (item, tmp_cnt))

    # Handle MD5 files after all other files have been processed.
    if isse.network in ["SIPR", "CW"]:
        process_files(isse, sftp, log, job, "*.md5.txt", False, False)

    if file_cnt == 0:
        job.log_info("NOFILES")

    job.log_close()

    log.log_info("Processed file count: %s" % str(file_cnt))

    # Do not send LastRun file to BICES.
    if isse.network != "BICES":
        if not transfer_file(isse, sftp, log, None, isse.job_log,
                             keep_log):
            log.log_err("Failed to transfer: %s" % isse.job_log)

    else:
        err_flag, err_msg = gen_libs.rm_file(isse.job_log)

        if err_flag:
            log.log_warn("%s" % str(err_msg))

    log.log_info("process::end %s: %s" % (isse.review_dir, str(file_cnt)))


def _send(isse, sftp, log, **kwargs):

    """Function:  _send

    Description:  Debugging option to test transferring files to the ISSE
        Guard.

    WARNING:  Do not use this for production use.

    Arguments:
        (input) isse -> ISSE Guard class instance.
        (input) sftp -> SFTP class instance.
        (input) log -> Log class instance.

    """

    # Make Job log name unique for Send to prevent conflict with other runs.
    job_path = os.path.dirname(isse.job_log) + os.path.sep + "Send-" \
        + os.path.basename(isse.job_log)

    job = gen_class.Logger(job_path, job_path, "INFO",
                           "%(asctime)s%(message)s", "%m-%d-%YT%H:%M:%SZ|")

    if isinstance(isse.files, list):

        for file_path in isse.files:
            log.log_info("send %s%s" % (isse.target, file_path))
            if not transfer_file(isse, sftp, log, job, file_path,
                                 isse.keep):
                log.log_err("Failed to transfer: %s" % file_path)

    elif isinstance(isse.files, str):
        log.log_info("send %s%s" % (isse.target, isse.files))
        if not transfer_file(isse, sftp, log, job, isse.files,
                             isse.keep):
            log.log_err("Failed to transfer: %s" % isse.files)

    job.log_close()

    if isse.keep:
        gen_libs.mv_file2(job_path, isse.complete_dir)

    else:
        err_flag, err_msg = gen_libs.rm_file(job_path)

        if err_flag:
            log.log_warn("%s" % str(err_msg))


def process_images(move_file, log, **kwargs):

    """Function:  process_images

    Description:  Process the images that are listed in the MOVE_FILE class.

    Arguments:
        (input) move_file -> Move_To_File class instance.
        (input) log -> Log class instance.

    """

    log.log_info("process_images::start %s" % str(len(move_file.images)))

    for item in move_file.images:
        file_base, file_ext = os.path.splitext(item)
        image_name = os.path.basename(item)
        thumb_name = file_base + ".jpg"

        # Add the image and thumb to the zip list.
        move_file.add_to_zip("sgraphics/" + image_name)
        move_file.add_to_zip("sgraphics/thumbnails/" + thumb_name)
        move_file.add_to_cleanup(move_file.dissem_dir + "sgraphics/" +
                                 image_name)
        move_file.add_to_cleanup(move_file.dissem_dir +
                                 "sgraphics/thumbnails/" + thumb_name)

        log.log_info("process_images::Files_To_Zip sgraphics/%s" % image_name)
        log.log_info("process_images::Files_To_Zip sgraphics/thumbnails/%s"
                     % thumb_name)


def process_media(move_file, log, **kwargs):

    """Function:  process_media

    Description:  Process the media that are listed in the MOVE_FILE class.

    Arguments:
        (input) move_file -> Move_To_File class instance.
        (input) log -> Log class instance.

    """

    log.log_info("process_media::start %s" % str(len(move_file.media)))

    for item in move_file.media:
        file_name = os.path.basename(item)
        file_path = move_file.dissem_dir + "attachments/" + file_name

        # Do not zip power point files.
        if os.path.splitext(file_path)[1] == ".pptx":
            log.log_info("process_media %s" % file_path)
            gen_libs.mv_file2(file_path, move_file.review_dir, move_file.org +
                             "-" + move_file.tape_dir + "-" + file_name)
            log.log_info("process_media::moved %s" % file_path)

        else:
            move_file.add_to_zip("attachments/" + file_name)
            log.log_info("process_media::Files_To_Zip %s" % file_name)

        move_file.add_to_cleanup(file_path)


def process_zip(move_file, log, **kwargs):

    """Function:  process_zip

    Description:  Create a zip file of the files in the MOVE_FILE class.

    Arguments:
        (input) move_file -> Move_To_File class instance.
        (input) log -> Log class instance.

    """

    if move_file.dissem_level in move_file.dissem_list:

        # Do not create new zip if zip is newer than html.
        if not os.path.isfile(move_file.zip_file_path) \
           or os.path.getctime(move_file.cur_file_dir + "/" +
                               move_file.cur_file_name) \
                > os.path.getctime(move_file.zip_file_path):

            gen_libs.make_zip(move_file.zip_file_path, move_file.cur_file_dir,
                              move_file.files_to_zip, is_rel_path=True)

            log.log_info("process_zip::created %s" % move_file.zip_file_path)

        else:
            log.log_warn("%s is newer than  %s" % (move_file.zip_file_path,
                                                   move_file.cur_file_name))

    else:
        log.log_warn("%s did not meet dissem_level" % move_file.cur_file_name)
        log.log_warn("\t Dissem: %s" % move_file.dissem_level)


def cleanup(move_file, log, **kwargs):

    """Function:  cleanup

    Description:  Clean up files in the MOVE_FILE class.

    Arguments:
        (input) move_file -> Move_To_File class instance.
        (input) log -> Log class instance.

    """

    for item in move_file.cleanup_list:
        status, err_msg = gen_libs.chk_crt_file(item, write=True, read=True)

        if status:

            err_flag, err_msg = gen_libs.rm_file(item)

            if err_flag:
                log.log_warn("%s" % str(err_msg))

            else:
                log.log_info("cleanup::deleted %s" % item)


def move_to_reviewed(isse, log, **kwargs):

    """Function:  move_to_reviewed

    Description:  Processes pre-approved products and prepares and moves them
        to the reviewed directory for further processing.

    Arguments:
        (input) isse -> ISSE Guard class instance.
        (input) log -> Log class instance.

    """

    move = isse_guard_class.MoveTo(isse.dissem_dir)
    move.get_files()

    cnt = 0
    str_val = "=" * 80

    log.log_info("move_to_reviewed::start")
    log.log_info("Processing pre-approved files...")
    log.log_info("Pre-File Count: %s %s" % (str(len(move.file_list)),
                                            move.dissem_dir))

    for file_path in move.file_list:

        log.log_info("Processing: %s" % file_path)

        move_file = isse_guard_class.MoveToFile(file_path, isse.review_dir,
                                                isse.dissem_dir)

        log.log_info("%s" % str_val)
        log.log_info("File_Name: %s" % move_file.cur_file_name)
        log.log_info("File_Dir: %s" % move_file.cur_file_dir)
        log.log_info("Zip_File: %s" % move_file.zip_file_path)
        log.log_info("XML_File_Path: %s" % move_file.xml_file_path)
        log.log_info("XML_File_Name: %s" % move_file.xml_file_name)
        log.log_info("%s" % str_val)

        status, err_msg = gen_libs.chk_crt_file(move_file.xml_file_path,
                                                write=True, read=True)

        if status:

            move_file.parse_xml_file()

            log.log_info("Product_Line: %s Image_Count: %s Media_Count: %s"
                         % (move_file.product_line, str(len(move_file.images)),
                            str(len(move_file.media))))

            if move_file.product_line in move_file.product_list:
                log.log_info("Product_Line: %s processing..."
                             % move_file.product_line)

                move_file.process_product()

                log.log_info("Object_ID: %s Dissem_Level: %s"
                             % (move_file.object_id, move_file.dissem_level))

                # Add the html and xml to the zip list.
                move_file.add_to_zip(move_file.cur_file_name)
                move_file.add_to_zip(move_file.xml_file_name)
                move_file.add_to_cleanup(move_file.dissem_dir +
                                         move_file.cur_file_name)
                move_file.add_to_cleanup(move_file.dissem_dir +
                                         move_file.xml_file_name)

                log.log_info("move_to_reviewed::Files_To_Zip %s"
                             % move_file.cur_file_name)
                log.log_info("move_to_reviewed::Files_To_Zip %s"
                             % move_file.xml_file_name)

                process_images(move_file, log)
                process_media(move_file, log)
                process_zip(move_file, log)
                cleanup(move_file, log)
                cnt += 1

    log.log_info("Moved_To_Reviewed::end %s: %s" % (move.dissem_dir, str(cnt)))


def initate_process(args_array, isse, **kwargs):

    """Function:  initate_process

    Description:  Sets up the program log, opens a sftp connection, and
        determines which option will be ran.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) isse -> ISSE Guard class instance.
        (input) **kwargs:
            pattern -> pattern matching string for other filenames

    """

    log = gen_class.Logger(isse.prog_log, isse.prog_log, "INFO",
                           "%(asctime)s %(levelname)s %(message)s",
                           "%Y-%m-%dT%H:%M:%SZ")

    str_val = "=" * 80
    log.log_info("%s Initialized" % isse.name)
    log.log_info("%s" % str_val)
    log.log_info("Transfer Dir: %s" % isse.transfer_dir)
    log.log_info("Review Dir: %s" % isse.review_dir)
    log.log_info("Complete Dir: %s" % isse.complete_dir)
    log.log_info("Job Log: %s" % isse.job_log)
    log.log_info("%s" % str_val)

    sftp = None

    if isse.action != "moveapproved":
        sftp, status = set_sftp_conn(isse, args_array["-s"], args_array["-d"],
                                     log)

    if isse.action == "moveapproved":
        move_to_reviewed(isse, log)

    elif sftp.is_connected and status and isse.action == "process":
        isse.set_other_files()
        log.log_info("set_other_files...")
        log.log_info("[ %s ]" % ", ".join(isse.other_files))

        process(isse, sftp, log, **kwargs)

    elif sftp.is_connected and status and isse.action == "send":
        print("NOTE:  Send option is for debugging purposes only.")

        if isse.files:
            _send(isse, sftp, log)

        else:
            print("ERROR:  Expected file path or array of file paths.")

    elif not sftp.is_connected:
        log.log_err("SFTP Connection failed to open")

    elif not status:
        log.log_err("SFTP failure on changing directory")

    else:
        log.log_err("initate_process::Unknown error")

    if sftp and sftp.is_connected:
        sftp.close_conn()
        log.log_info("SFTP Connection closed")

    log.log_close()


def run_program(args_array, **kwargs):

    """Function:  run_program

    Description:  Creates class instance(s) and controls flow of the program.

    Arguments:
        (input) args_array -> Dict of command line options and values.
        (input) **kwargs:
            pattern -> pattern matching string for other filenames

    """

    cfg, status_flag = load_cfg(args_array["-c"], args_array["-d"])

    if not status_flag:
        print("Error:  Problem in configuration file.")
        return

    else:
        try:
            isse = isse_guard_class.IsseGuard(
                args_array["-N"], cfg,
                action=args_array.get("-A", "process"),
                files=args_array.get("-f", None),
                keep=args_array.get("-k", False))

        except ValueError as msg:
            print("Value Error: %s" % msg)

        except OSError as msg:
            print("OS Error: %s" % msg)

        else:
            initate_process(args_array, isse, **kwargs)


def main():

    """Function:  main

    Description:  Initializes program-wide used variables and processes command
        line arguments and values.  Create a program lock to prevent other
        instantiations from running.

    Variables:
        dir_chk_list -> contains options which will be directories.
        opt_req_list -> contains options that are required for the program.
        opt_val_list -> contains options which require values.
        opt_valid_val -> contains options with their valid values.
        pattern -> pattern matching string for other filenames to be processed

    Arguments:
        (input) argv -> Arguments from the command line.

    """

    dir_chk_list = ["-d"]
    opt_req_list = ["-N", "-c", "-d", "-s"]
    opt_val_list = ["-A", "-N", "-c", "-d", "-f", "-k", "-s"]
    opt_valid_val = {"-A": ["moveapproved", "process", "send"]}
    pattern = "PULLED"

    # Process argument list from command line.
    args_array = arg_parser.arg_parse2(sys.argv, opt_val_list)

    if not gen_libs.help_func(args_array, __version__, help_message):
        if not arg_parser.arg_require(args_array, opt_req_list) \
           and arg_parser.arg_valid_val(args_array, opt_valid_val) \
           and not arg_parser.arg_dir_chk_crt(args_array, dir_chk_list):

            try:
                flavor_id = args_array.get("-A") + args_array.get("-N")
                prog_lock = gen_class.ProgramLock(sys.argv, flavor_id)

                run_program(args_array, pattern=pattern)

                del prog_lock

            except gen_class.SingleInstanceException:
                print("WARNING:  Lock in place for: -A: %s  -N: %s"
                      % (args_array.get("-A"), args_array.get("-N")))


if __name__ == "__main__":
    sys.exit(main())
