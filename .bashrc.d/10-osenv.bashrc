#!/usr/bin/env bash

##--OSENV--BEGIN--##
# Catch output and source it to the active environment
osenv() {
    arg1=$1
    arg2=$2
    osenv_cmd=osenv-tool

    if [ -x "$(command -v $osenv_cmd)" ]; then
        # source environment
        if [[ $arg1 == "-e" ]]; then
            echo "Load .ostackrc for ${arg2}"
            $($osenv_cmd -e ${arg2})

        # clean up
        elif [[ $arg1 == "-c" ]]; then
            echo "Clean up .ostackrc variables."
            $($osenv_cmd -c)

        # read 
        elif [[ $arg1 == "-r" ]]; then
            echo "Read encoded .ostackrc file."
            $($osenv_cmd -r ${arg2})

        # forward the rest
        else
            $osenv_cmd $@
        fi
    else
        echo "Command osenv-tool not found. Please load the correct virtualenv."
    fi
}
##--OSENV--END--##