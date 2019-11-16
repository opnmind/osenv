[![Build Status](https://travis-ci.org/opnmind/osenv-tool.svg?branch=master)](https://travis-ci.org/opnmind/osenv-tool)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# osenv-tool - OpenStack Environment loader

## TODO

Idee: Einen Token generieren der vorübergehend Zugriff gewährt

- [ ] find a alternative for using env vars
- [ ] add edit function to change one password from a existing list (partly)
- [x] add to write function to add a new tenant to an existing list
- [ ] better description to activate keyring
- [ ] move the bashrc integration from the installation process to the tool directly (e.g. osenv-tool --integrate-bashrc [-b])
- [ ] Test case file encryption 

## Requirements

- Python 3
- gnome-keyring package

## Description

Steps to use:

1. Setup virtual environment

For virtualenv you can install "python2-virtualenv" or "python3-virtualenv" system package.

```shell
# create a python 3 environment
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/activate
```

2. Install Requirements and osenv tool.

```shell
$ pip install git+https://github.com/opnmind/osenv-tool.git
```

3. Create an encrypted configuration file with all your needed credentials. (RSA Encryption with 4096 bit Key)

```shell
$ osenv-tool -w [~/.ostackrc.enc]
```

4. Put your configuration into gnome-keyring.

```shell
$ osenv-tool -r [~/.ostackrc.enc]
# better for automatic source given output
$ $(osenv-tool -r [~/.ostackrc.enc])
```

5. List available environment's.

```shell
$ osenv-tool -l
PROD
PREPROD
```

6. Load a given environment.

```shell
$ osenv-tool -e PROD
# better for automatic source given output
$ $(osenv-tool -e PROD)
```

7. Unset ENV variables if environment isn't needed anymore.

```shell
$ osenv-tool -c
# better for automatic source given output
$ $(osenv-tool -c)
```

8. Edit a existing encoded file.

```shell
$ osenv-tool -i [~/.ostackrc.enc]
```

## Usage with bashrc

Now the setup process added the snippet durring the installation to the .bashrc.d directory as 10-osenv.bashrc file.

DEPRECATED: If you want the full support, then you have to add those code snippet to you ~/.bashrc.
With this little trick you are able to source the user variables in your shell session.

```shell
# Clean up your environment.
$ osenv -c

# Load your desired .ostackrc environment.
$ osenv -e PROD
```

```shell
mkdir ~/.bashrc.d
chmod 0700 ~/.bashrc.d

for file in ~/.bashrc.d/*.bashrc;
do
    source “$file”
done

##--OSENV--BEGIN--##
# Catch output and source it to the active environment
osenv() {
    arg1=$1
    arg2=$2

    # source environment
    if [[ $arg1 == "-e" ]]; then
        echo "Load .ostackrc for ${arg2}"
        $(osenv-tool -e ${arg2})

    # clean up
    elif [[ $arg1 == "-c" ]]; then
        echo "Clean up .ostackrc variables."
        $(osenv-tool -c)
    
    # read 
    elif [[ $arg1 == "-r" ]]; then
        echo "Read encoded .ostackrc file."
        $(osenv-tool -r ${arg2})

    # forward the rest
    else
        osenv-tool $@
    fi
}
##--OSENV--END--##
```
   
**Hint:**
Everytime you expose only the active enviroment to the Session Variables.

```shell
$ osenv-tool -h
```

```log
usage: osenv-tool [-h]
              (--version | -e <environment-name> | -l | -c | -r [<encoded-file>] | -w [<encoded-file>] | -i [<encoded-file>])

Create and load .ostackrc credentials confidentialy.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -e <environment-name>, --environment <environment-name>
                        Load .ostackrc environment name.
  -l, --list            List available .ostackrc environments.
  -c, --clean           Clean up active .ostackrc environment.
  -r [<encoded-file>], --read [<encoded-file>]
                        Read encoded file and set content to session
                        variables. Default filename is ~/.ostackrc.enc.
  -w [<encoded-file>], --write [<encoded-file>]
                        Create and write encoded file with multiple ostackrc
                        environments. Default filename is ~/.ostackrc.enc.
  -i [<encoded-file>], --edit [<encoded-file>]
                        Edit a encoded file and write it back. Default
                        filename is ~/.ostackrc.enc.
```
