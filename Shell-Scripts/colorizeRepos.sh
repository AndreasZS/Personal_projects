#!/bin/bash

# Credit for this to numerous stackexchange posts and a response by unix.stackexchange user mikeserv
# link: https://unix.stackexchange.com/questions/148342/fine-tune-ls-colors-for-directory-suffixes

# Bash script to detect git repositories
# Can be run from any location

# =========================================================================================================================
# WARNING:
# This works by setting the sticky bits of directories so that users other than the one who created them CANNOT delete them.
# The ls output color of these directories is then based on the value of 'st' in the LS_COLORS environment variable
# =========================================================================================================================

# Function to return list of git repositories
# When run from a directory, checks all files/directories within to see if they contain a '.git' repo base
# If they do, they are appended to the 'output' array
function list_repos {
    local dirs=( $(ls) )
    local final=$1
    local output=()
    local count=0
        for d in ${dirs[@]}; do
            cd $d 2> /dev/null
            if [[ $? -eq 0 ]]
                then ls -a | grep .git &> /dev/null
                if [[ $? -eq 0 ]]
                    # then output=$output:$d; count=$((count + 1)) # This works
                    then output+=( $d ); count=$((count + 1)) # This is for testing stuff
                fi
                cd ..
            fi
        done
    # echo $"$count"
    # echo $"${output[@]}"
    eval $final="'${output[@]}'"
}

# This will set sticky bits for the repo directories
# Other users will NOT be able to delete them
# Its color in ls output will change according to the LS_COLORS environment variable
# Based on the color-code values for 'st'
# To undo, run chmod o-t <directory-name> or following directions below to use 'undo_sticky' function
function set_sticky {
    local git_repos=$1
    for r in ${git_repos[@]}; do
        chmod o+t $r
    done
}

function undo_sticky {
    for r in ${gits[@]}; do
        chmod o-t $r
    done
}

list_repos gits # This line will store an array of git directory names in 'gits'
set_sticky "${gits[@]}" # This will set the sticky bit of the directories named in gits

# Uncomment following line and comment the 'set_sticky' line to undo the sticky bit setting
# undo_sticky  
