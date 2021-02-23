#!/bin/sh

set -e

BASEDIR="`dirname "${0}"`/.."
. "${BASEDIR}/scripts/functions.sub"

TRDDIR="${BASEDIR}/training_data"
TRDDIR_P="${TRDDIR}/positive"
TRDDIR_N="${TRDDIR}/negative"

if [ -e "${TRDDIR}" ]
then
  rm -rf "${TRDDIR}"
fi
mkdir "${TRDDIR}"
mkdir "${TRDDIR_P}"
mkdir "${TRDDIR_N}"

for tone in 0 1 2 3 4 5 6 7 8 9 A B C D H M
do
  infile="${BASEDIR}/training_set/dtmf_${tone}.wav"
  ifname="`basename "${infile}"`"
  for volume in 0.1 0.25 0.5 0.75 1.0
  do
    ofpref="${ifname%.wav}_${volume}"
    ofname="${ofpref}.sln"
    sox --volume ${volume} "${infile}" --bits 16 --encoding signed-integer --endian little "${ofname}" trim 0 0.1
    makeann "${ofname}" "${ofpref}"
    g729_ofname="${ofpref}.18"
    #${PYTHON_CMD} -m pipenv run ${PYTHON_CMD} read_g729_data.py "${g729_ofname}"
    mv "${g729_ofname}" "${TRDDIR_P}/"
    echo "Generated ${TRDDIR_P}/${g729_ofname}"
  done
done

i=0
while nfile="${TRDDIR_N}/${i}.18"
do
  dd if=negative.18 of="${nfile}" bs=100 count=1 skip=${i} 2>/dev/null
  if [ ! -s "${nfile}" ]
  then
    rm "${nfile}"
    break
  fi
  echo "Generated ${nfile}"
  i=$((${i} + 1))
done
