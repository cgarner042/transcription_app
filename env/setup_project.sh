#!/bin/bash

# Define the base directory
PARENT_DIR=/home/garner/code
BASE_DIR="transcription_app"

# Create directory structure
mkdir -p $PARENT_DIR/$BASE_DIR/{data/{input,output},models,src/{gui,core},tests/{sample_files},env,logs}

# Create empty placeholder files
touch $PARENT_DIR/$BASE_DIR/src/{__init__.py,main.py}
touch $PARENT_DIR/$BASE_DIR/src/gui/{__init__.py,main_window.py}
touch $PARENT_DIR/$BASE_DIR/src/core/{__init__.py,transcription.py,utils.py}
touch $PARENT_DIR/$BASE_DIR/tests/{test_transcription.py,test_utils.py}
touch $PARENT_DIR/$BASE_DIR/README.md
touch $PARENT_DIR/$BASE_DIR/LICENSE
touch $PARENT_DIR/$BASE_DIR/env/{conda.yaml,requirements.txt}

echo "Project structure created successfully!"
