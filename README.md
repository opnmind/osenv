[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
# osenv - OpenStack Environment loader

## TODO

Idee: Einen Token generieren der vorübergehend Zugriff gewährt

[x] 1. set 0600 to .enc file
[x] 2. the 0600 is required to work with that file
[ ] 3. find a alternative for using env vars
[ ] 4. add edit function to change one password from a existing list (partly)
[x] 5. add to write function to add a new tenant to an existing list
[ ] 6. better description to activate keyring

## Requirements

- Python 3
- gnome-keyring package

## Description

Steps to use:

00. Setup virtual environment

For virtualenv you can install "python2-virtualenv" or "python3-virtualenv" system package.

```shell
# create a python 3 environment
$ virtualenv -p /usr/bin/python3 venv
$ source venv/bin/active
```

1. Install Requirements and osenv tool.

```shell
$ pip install git@<git-url>:<username>/osenv.git
```

1. Create an encrypted configuration file with all your needed credentials. (RSA Encryption with 4096 bit Key)

```shell
$ osenv -w [.ostackrc.enc]
```

2. Put your configuration into gnome-keyring.

```shell
$ osenv -r [.ostackrc.enc]
# better for automatic source given output
$ $(osenv -r [.ostackrc.enc])
```

3. List available environment's.

```shell
$ osenv -l
PROD
PREPROD
```

4. Load a given environment.

```shell
$ osenv -e PROD
# better for automatic source given output
$ $(osenv -e PROD)
```

5. Unset ENV variables if environment isn't needed anymore.

```shell
$ osenv -c
# better for automatic source given output
$ $(osenv -c)
```

6. Edit a existing encoded file.

```shell
$ osenv -i [.ostackrc.enc]
```

## Usage with bashrc

Now the setup process added the snippet durring the installation to the .bashrc filehistory.

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
        $(osenv -e ${arg2})

    # clean up
    elif [[ $arg1 == "-c" ]]; then
        echo "Clean up .ostackrc variables."
        $(osenv -c)
    
    # read 
    elif [[ $arg1 == "-r" ]]; then
        echo "Read encoded .ostackrc file."
        $(osenv -r ${arg2})

    # forward the rest
    else
        osenv $@
    fi
}
##--OSENV--END--##
```
   
**Hint:**
Everytime you expose only the active enviroment to the Session Variables.

```shell
$ osenv -h
```

```log
usage: osenv [-h]
              (--version | -e <environment-name> | -l | -c | -r [<encoded-file>] | -w [<encoded-file>] | -i [<encoded-file>])

Create and load ostackrc credentials confidentialy.

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  -e <environment-name>, --environment <environment-name>
                        Load .ostackrc environment name.
  -l, --list            List available .ostackrc environments.
  -c, --clean           Clean up active .ostackrc environment.
  -r [<encoded-file>], --read [<encoded-file>]
                        Read encoded file and set content to session
                        variables. Default filename is .ostackrc.enc.
  -w [<encoded-file>], --write [<encoded-file>]
                        Create and write encoded file with multiple ostackrc
                        environments. Default filename is .ostackrc.enc.
  -i [<encoded-file>], --edit [<encoded-file>]
                        Edit a encoded file and write it back. Default
                        filename is .ostackrc.enc.
```