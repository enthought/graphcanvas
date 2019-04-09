#! /usr/bin/env sh
# (C) Copyright 2010-2019 Enthought, Inc., Austin, TX
# All rights reserved.
set -e

export EDM_VER=1.5

if [[ ${TRAVIS_OS_NAME} == "osx" ]]
then
    # download and install EDM
    wget https://package-data.enthought.com/edm/osx_x86_64/${EDM_VER}/edm_${EDM_VER}.0.pkg
    sudo installer -pkg edm_${EDM_VER}.0.pkg -target /
else
    # download and install EDM
    wget https://package-data.enthought.com/edm/rh5_x86_64/${EDM_VER}/edm_${EDM_VER}.0_linux_x86_64.sh
    chmod u+x edm_${EDM_VER}.0_linux_x86_64.sh
    ./edm_${EDM_VER}.0_linux_x86_64.sh -b -p ~
    export PATH="~/bin:${PATH}"
fi

# install pip and invoke into default EDM environment
edm install -y pip invoke
