# Python project for the transfer of dissemination documents to an ISSE Guard System.
# Classification (U)

# Description:
  Used to process and send pre-reviewed files to an ISSE Guard system (which will send them to a specified security enclave).  Also process and package pre-approved documents and send them to a transfer directory.


###  This README file is broken down into the following sections:
  * Features
  * Prerequisites
  * Installation
  * Configuration
  * Program Help Function
  * Testing
    - Unit


# Features:
  * Process and send pre-reviewed files in a "reviewed" directory to an ISSE Guard System.
  * Transfer dissemination documents to a number of security enclaves.
  * Process and package pre-approved documents and send them to a "reviewed" directory.

# Prerequisites:

  * List of Linux packages that need to be installed on the server.
    - git
    - python-pip

  * Local class/library dependencies within the program structure.
    - python-lib
    - isse-lib
    - sftp-lib


# Installation:

Install the program.
  * From here on out, any reference to **{Python_Project}** or **PYTHON_PROJECT** replace with the baseline path of the python program.

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

```
cd config
cp isse_guard.py.TEMPLATE isse_guard.py
cp ssh_config.py.TEMPLATE ssh_config.py
```

Make the appropriate change to the configuration environments for each config file.
 * Isse_Guard.py configuration file:
   - dissem_dir = "DIRECTORY_PATH"
   - transfer_dir = "DIRECTORY_PATH"
   - log_dir = a"DIRECTORY_PATH"

 * SSH_Config.py configutation file:
   - username = "USERNAME"
   - password = "PASSWORD"
   - host = "HOSTNAME"
   - log_file = "DIRECTORY_PATH/paramiko.log"

```
vim isse_guard.py
vim ssh_config.py
chmod 600 ssh_config.py
```


# Program Help Function:

  The program has a -h (Help option) that will show display an usage message.  The help message will usually consist of a description, usage, arugments to the program, example, notes about the program, and any known bugs not yet fixed.  To run the help command:

```
{Python_Project}/isse-transfer/isse_guard_transfer.py -h
```


# Testing:

# Unit Testing:

### Installation:

Install the project using the procedures in the Installation section.

### Testing:

```
cd {Python_Project}/isse-transfer
test/unit/isse_guard_transfer/unit_test_run.sh
```

### Code Coverage:
```
cd {Python_Project}/isse-transfer
test/unit/isse_guard_transfer/code_coverage.sh
```

