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

#wget http://www.mega-nerd.com/libsndfile/files/libsndfile-${SNDFILE_VER}.tar.gz
#tar xfz libsndfile-${SNDFILE_VER}.tar.gz
#cd libsndfile-${SNDFILE_VER}
#./configure
#make
#sudo make install
#cd -

git clone -b master https://github.com/sippy/rtpproxy.git
git -C rtpproxy submodule update --init --recursive
cd rtpproxy
 ./configure
 for dir in libexecinfo makeann
 do
   make -C "${dir}"
 done
 sudo make -C makeann install
cd -

sudo apt update -y
sudo apt install sox

${PYTHON_CMD} -m pipenv install
