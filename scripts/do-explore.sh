#!/bin/sh

set -e

BASEDIR="`dirname "${0}"`/.."
. "${BASEDIR}/scripts/functions.sub"

for infile in ${BASEDIR}/training_set/*.wav
do
  for volume in 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9 1.0
  do
    ifname="`basename "${infile}"`"
    ofpref="${ifname%.wav}.vol${volume}"
    ofname="${ofpref}.sln"
    sox --volume ${volume} "${infile}" --bits 16 --encoding signed-integer --endian little "${ofname}"
    makeann "${ofname}" "${ofpref}"
    g729_ofname="${ofpref}.18"
    ${PYTHON_CMD} -m pipenv run ${PYTHON_CMD} read_g729_data.py "${g729_ofname}"
  done
done
