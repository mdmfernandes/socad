#!/usr/bin/env sh
# This file is part of SOCAD
# Copyright (C) 2018 Miguel Fernandes
#
# SOCAD is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# SOCAD is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

# Project name
export SOCAD_PROJECT_NAME="commonSource-tutorial"
# Project work space
SOCAD_WORK_SPACE="/home/tarzan/Projects"

## Server info
# Client Address
export SOCAD_CLIENT_ADDR="localhost"
# Client Port
export SOCAD_CLIENT_PORT="4000"


#############################################
#       Do not change the code below!       #
#############################################
# Define Paths
export SOCAD_ROOT_DIR="$SOCAD_WORK_SPACE/$SOCAD_PROJECT_NAME"
export SOCAD_SCRIPT_DIR="$SOCAD_ROOT_DIR/script"

# Create the root dir, if it doesn't exist
if [ ! -d "$SOCAD_ROOT_DIR" ]; then
    echo
    echo "[INFO] Creating $SOCAD_ROOT_DIR ..."
    mkdir $SOCAD_ROOT_DIR
    cp -r script/ $SOCAD_ROOT_DIR # Copy the script folder to the project folder
else
    echo
    echo "[INFO] The directory $SOCAD_ROOT_DIR already exists."
fi

# Create the results file in the project root directory
touch "$SOCAD_ROOT_DIR/sim_res"

echo
echo "**********************************************************************"
echo "*                          Starting Cadence                          *"
echo "**********************************************************************"
# Code to run Cadence and the script cadence.il
icfb -nograph -restore cadence.il
