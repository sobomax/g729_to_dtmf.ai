#!/bin/sh

set -e

BASEDIR="`dirname "${0}"`/.."
#. "${BASEDIR}/scripts/functions.sub"

for infile in ${BASEDIR}/training_set/*.wav
do
  ifname="`basename "${infile}"`"
  ofpref="${ifname%.wav}"
  ofname="${ofpref}.sln"
  sox "${infile}" --bits 16 --encoding signed-integer --endian little "${ofname}"
  makeann "${ofname}" "${ofpref}"
  g729_ofname="${ofpref}.18"
  ${PYTHON_CMD} -m pipenv run ${PYTHON_CMD} read_g729_data.py "${g729_ofname}"
done
