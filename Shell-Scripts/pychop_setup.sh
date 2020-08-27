#!/bin/bash
# Bash script to install required packages for pychop3d
#

CHECK_PIP=$(apt list python3-pip 2> /dev/null)
DEPS=(matplotlib numpy scipy pytest networkx PyYAML requests trimesh triangle pyglet MeshPy Shapely Rtree)

echo $'This setup assumes you already have python3.x installed.'

function install_deps {
    if [ "$CHECK_PIP" != "Listing..." ]
        then echo $'pip3 already installed.\nInstalling pychop3d dependencies.'
    else
        echo $'pip3 not installed. \nInstalling python3-pip now.'; sudo apt install python3-pip 
    fi
    pip3 install ${DEPS}
}

install_deps