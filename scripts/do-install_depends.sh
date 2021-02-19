#!/bin/sh

set -e

BASEDIR="`dirname "${0}"`/.."
#. "${BASEDIR}/scripts/functions.sub"

BCG729_VER=1.1.1
#SNDFILE_VER=1.0.28

uname -a
which ${CC}
${CC} --version
${PYTHON_CMD} --version
automake --version
autoconf --version
autoreconf --version

mkdir deps
cd deps
wget -O bcg729-${BCG729_VER}.tar.gz \
  https://github.com/BelledonneCommunications/bcg729/archive/${BCG729_VER}.tar.gz
tar xfz bcg729-${BCG729_VER}.tar.gz
cd bcg729-${BCG729_VER}
touch NEWS AUTHORS ChangeLog bcg729.spec.in # Hello, automake! :)
./autogen.sh
./configure
make
sudo make install
cd -
