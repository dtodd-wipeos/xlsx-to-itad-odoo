#!/bin/bash

# Sets up the environment and runs the script
source config.sh

pdoc --template-dir .pdoc --force --html .
