#!/bin/bash
# Part of XLSX to Odoo import
# Copyright 2020 David Todd <dtodd@oceantech.com>
# License: MIT License, refer to `license.md` for more information

# This is a simple script that will build and run the linter docker container
# Expects a user that has the `docker` group or is `root` (NOTE: The docker group grants privileges equivalent to the root user)
# Every time this script is ran, it will do some housecleaning steps such as:
#   Removing the previous container - The code inside it will most likely have changed since the last run
#   Removing the previous image - Same reason as above
#   Build a fresh container - In the same vain as the github workflow
#   Run the newly built container

project=alpine-pylint-project

# This is required to remove the previous image
echo "Removing previous container - An error is expected if the container doesn't exist"
docker ps -a | grep ${project} | awk '{print $1}' | xargs docker rm

# This is required because each successive `docker build` will
# create a brand new image on your drive.
# Each container is pretty small at ~65MiB, but it will quickly add up.
echo "Removing previous build - An error is expected if the image doesn't exist"
docker images | grep ${project} | awk '{print $3}' | xargs docker rmi

# Creates an image with the tag `${project}:latest`
echo "Building Container ${project}:latest from Dockerfile"
docker build --tag ${project} .

# Automatically uses the `:latest` tag
# You can also include a `.env` (environment variables inside the container) file here if needed with:
# `docker run --env-file .env ${project}`
# For more information: https://docs.docker.com/engine/reference/commandline/run/#set-environment-variables--e---env---env-file
echo "Running your app"
docker run ${project}
