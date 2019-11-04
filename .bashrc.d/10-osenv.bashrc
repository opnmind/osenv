#!/usr/bin/env bash

##--OSENV--BEGIN--##
# Catch output and source it to the active environment
osenv() {
    arg1=$1
    arg2=$2

    until
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
    do
        echo "Command os-env not found. Please load the correct virtualenv."
        break
    done
}
##--OSENV--END--##