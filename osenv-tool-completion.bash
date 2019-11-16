#/usr/bin/env bash

_osenv-tool()
{
    _script_commands=$( compgen -W '\
        -h --help \
        --version \
        -c --clean \
        -l --list \
        -r --read \
        -w --write \
        -e --environment=<environment-name> \
        -i --edit' -- "$cur" )

    local cur
    COMPREPLY=()
    cur="${COMP_WORDS[COMP_CWORD]}"
    COMPREPLY=( $(compgen -W "${_script_commands}" -- ${cur}) )

    return 0
}
complete -o nospace -F _osenv-tool osenv-tool