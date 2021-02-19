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
done
