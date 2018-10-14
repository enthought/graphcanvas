#! /usr/bin/env sh

set -e

if [[ ${TRAVIS_OS_NAME} == "osx" ]]
then
    # download and install EDM
    wget https://package-data.enthought.com/edm/osx_x86_64/${EDM_MAJOR_MINOR}/edm_${EDM_VER}.pkg
    sudo installer -pkg edm_${EDM_VER}.pkg -target /
else
    # download and install EDM
    wget https://package-data.enthought.com/edm/rh5_x86_64/${EDM_MAJOR_MINOR}/edm_${EDM_VER}_linux_x86_64.sh
    chmod u+x edm_${EDM_VER}_linux_x86_64.sh
    ./edm_${EDM_VER}_linux_x86_64.sh -b -p ~
    export PATH="~/bin:${PATH}"
fi

# install pip and invoke into default EDM environment
edm install -y pip invoke
