# Python project for the transfer of dissemination documents to an ISSE Guard System.
# Classification (U)

# Description:
  This program is used to process and send pre-reviewed files to an ISSE Guard system (which will send them to a specified security enclave).  Also process and package pre-approved documents and send them to a transfer directory.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Description
  * Program Help Function
  * Help Message
  * Testing
    - Unit
    - Integration
    - Blackbox


# Features:
  * Process and send pre-reviewed files in a "reviewed" directory to an ISSE Guard System.
  * Transfer dissemination documents to a number of security enclaves.
  * Process and package pre-approved documents and send them to a "reviewed" directory.

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - python-libs
    - python-devel
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - lib/gen_class
    - lib/arg_parser
    - lib/gen_libs
    - isse_lib/isse_guard_class
    - sftp_lib/sftp_class


# Installation:

Install the program.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
umask 022
cd {Python_Project}
git clone git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/isse-transfer.git
```

Install/upgrade system modules.

```
cd isse-transfer
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-isse-lib.txt --target isse_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target isse_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-sftp-lib.txt --target sftp_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target sftp_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

# Configuration:

Create ISSE Guard and SFTP configuration files.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd config
cp isse_guard.py.TEMPLATE isse_guard.py
cp ssh_config.py.TEMPLATE ssh_config.py
```

Make the appropriate change to the configuration environments for each config file.
 * Isse_Guard.py configuration file:
   - dissem_dir = "Base directory path for the moveapproved option"
   - transfer_dir = "Base directory path to where the different security transfer directories are located"
   - log_dir = "Directory path to where the program log will be written to"

 * SSH_Config.py configutation file:
   - username = "USERNAME"
   - password = "PASSWORD"
   - host = "HOSTNAME"
   - log_file = "Directory path and file name to where the Paramiko log will be written to"

```
vim isse_guard.py
vim ssh_config.py
chmod 600 ssh_config.py
```


# Program Descriptions:
### Program: isse_guard_transfer.py
##### Description: Process and send pre-reviewed files in a "reviewed" directory to an ISSE Guard system (which will send them to a specified security enclave).  Also process and package pre-approved documents and send them to a "reviewed" directory.


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
{Python_Project}/isse-transfer/isse_guard_transfer.py -h
```


# Help Message:
  Below is the help message for the program.  Recommend running the -h option on the command line to see the latest help message.

    Program:  isse_guard_transfer.py

    Description:  Process and send pre-reviewed files in a "reviewed"
        directory to an ISSE Guard system (which will send them to a specified
        security enclave).  Also process and package pre-approved documents and
        send them to a "reviewed" directory.

    Usage:
        isse_guard_transfer.py [-A {process | moveapproved | send}]
            -N value | -c file | -d path | -s file [-f path | [path1, path2]]
            -k {True | False}
            [-v | -h]

    Arguments:
        -A {process | moveapproved | send} => Action to perform.
            process -> Process files in a "reviewed" directory and ftp them to
                an ISSE Guard server.
            moveapproved -> Process files in an "IS" directory, package them up,
                and move them to a "reviewed" directory.
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
        The two configuration files below are required to run this program.
        Create them and replace those variables (i.e. <VARIABLE>) with a value.
        
        ISSE Guard configuration file format (isse_guard.py).  The
        configuration file format for the ISSE Guard is for the initial
        environment setup for the program.
            # ISSE Guard Configuration file
            # Classification (U)
            # Dissem_Dir -> Base directory for "moveapproved" option.
            dissem_dir = "/<DIR_PATH>/"
            # Transfer_Dir -> Base directory to security transfer directories.
            transfer_dir = "/<DIR_PATH>/"
            # Log_Dir -> Directory path where program log will be written to.
            log_dir = "/<DIR_PATH>/"
            # Backup -> True archives the files,  False will delete them.
            backup = True

        SSH/SFTP configuration file format (ssh_config.py).  The configuration
        file format is for SFTP connection setup to ISSE Guard server.
            # SSH Configuration file
            # Classification (U)
            # Unclassified until filled.
            username = "<USERNAME>"
            password = "<USER_PASSWD>"
            host = "<SERVER_NAME>"
            port = 22
            # Log_File -> Directory path to Paramiko log file location.
            log_file = "/<DIRECTORY_PATH>/paramiko.log"

    Example:
        isse_guard_transfer.py -c isse_guard -d config -s ssh_config -N SIPR
            -A process



# Testing:


# Unit Testing:

### Description: Testing consists of unit testing for the functions in the isse_guard_transfer.py program.

### Installation:

Install the program.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/isse-transfer.git
```

Install/upgrade system modules.

```
cd isse-transfer
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.

```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-isse-lib.txt --target isse_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target isse_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-sftp-lib.txt --target sftp_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target sftp_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```


# Unit test runs for isse_guard_transfer.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/isse-transfer
```

### Unit:  help_message
```
test/unit/isse_guard_transfer/help_message.py
```

### Unit:  
```
test/unit/isse_guard_transfer/
```

### Unit:  
```
test/unit/isse_guard_transfer/
```

### Unit:  run_program
```
test/unit/isse_guard_transfer/run_program.py
```

### Unit:  main
```
test/unit/isse_guard_transfer/main.py
```

### All unit testing
```
test/unit/isse_guard_transfer/unit_test_run.sh
```

### Code coverage program
```
test/unit/isse_guard_transfer/code_coverage.sh
```


# Integration Testing:

### Description: Testing consists of integration testing of functions in the isse_guard_transfer.py program.

### Installation:

Install these programs using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/isse-transfer.git
```

Install/upgrade system modules.

```
cd isse-transfer
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-isse-lib.txt --target isse_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target isse_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-sftp-lib.txt --target sftp_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target sftp_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create ISSE Guard and SFTP configuration files.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd test/integration/isse-transfer/config
cp ../../../../config/isse_guard.py.TEMPLATE isse_guard.py
cp ../../../../config/ssh_config.py.TEMPLATE ssh_config.py
```

Make the appropriate change to the configuration environments for each config file.
 * Isse_Guard.py configuration file:
   - dissem_dir = "Base directory path for the moveapproved option"
   - transfer_dir = "Base directory path to where the different security transfer directories are located"
   - log_dir = "Directory path to where the program log will be written to"

 * SSH_Config.py configutation file:
   - username = "USERNAME"
   - password = "PASSWORD"
   - host = "HOSTNAME"
   - log_file = "Directory path and file name to where the Paramiko log will be written to"

```
vim isse_guard.py
vim ssh_config.py
chmod 600 ssh_config.py
```


# Integration test runs for isse_guard_transfer.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/isse-transfer
```

### Integration:  
```
test/integration/isse_guard_transfer/
```

### All integration testing
```
test/integration/isse_guard_transfer/integration_test_run.sh
```

### Code coverage program
```
test/integration/isse_guard_transfer/code_coverage.sh
```


# Blackbox Testing:

### Description: Testing consists of blackbox testing of the isse_guard_transfer.py program.

### Installation:

Install these programs using git.
  * Replace **{Python_Project}** with the baseline path of the python program.
  * Replace **{Branch_Name}** with the name of the Git branch being tested.  See Git Merge Request.

```
umask 022
cd {Python_Project}
git clone --branch {Branch_Name} git@sc.appdev.proj.coe.ic.gov:JAC-DSXD/isse-transfer.git
```

Install/upgrade system modules.

```
cd isse-transfer
sudo bash
umask 022
pip install -r requirements.txt --upgrade --trusted-host pypi.appdev.proj.coe.ic.gov
exit
```

Install supporting classes and libraries.
```
pip install -r requirements-python-lib.txt --target lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-isse-lib.txt --target isse_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target isse_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-sftp-lib.txt --target sftp_lib --trusted-host pypi.appdev.proj.coe.ic.gov
pip install -r requirements-python-lib.txt --target sftp_lib/lib --trusted-host pypi.appdev.proj.coe.ic.gov
```

### Configuration:

Create ISSE Guard and SFTP configuration files.
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd test/blackbox/isse-transfer/config
cp ../../../../config/isse_guard.py.TEMPLATE isse_guard.py
cp ../../../../config/ssh_config.py.TEMPLATE ssh_config.py
```

Make the appropriate change to the configuration environments for each config file.
 * Isse_Guard.py configuration file:
   - dissem_dir = "Base directory path for the moveapproved option"
   - transfer_dir = "Base directory path to where the different security transfer directories are located"
   - log_dir = "Directory path to where the program log will be written to"

 * SSH_Config.py configutation file:
   - username = "USERNAME"
   - password = "PASSWORD"
   - host = "HOSTNAME"
   - log_file = "Directory path and file name to where the Paramiko log will be written to"

```
vim isse_guard.py
vim ssh_config.py
chmod 600 ssh_config.py
```


# Blackbox test run for isse_guard_transfer.py:
  * Replace **{Python_Project}** with the baseline path of the python program.

```
cd {Python_Project}/isse-transfer
```


### Blackbox:  
```
test/blackbox/isse_guard_transfer/blackbox_test.sh
```

