#!/bin/sh

set -e

BASEDIR="`dirname "${0}"`/.."
. "${BASEDIR}/scripts/functions.sub"

TRDDIR="${BASEDIR}/training_data"
TRDDIR_P="${TRDDIR}/positive"
TRDDIR_N="${TRDDIR}/negative"
TRDDIR_V="${TRDDIR}/validate"

if [ -e "${TRDDIR}" ]
then
  rm -rf "${TRDDIR}"
fi
mkdir "${TRDDIR}"
mkdir "${TRDDIR_P}"
mkdir "${TRDDIR_N}"
mkdir "${TRDDIR_V}"

for tone in 0 1 2 3 4 5 6 7 8 9 A B C D H M
do
  infile="${BASEDIR}/training_set/dtmf_${tone}.wav"
  ifname="`basename "${infile}"`"
  for volume in 0.1 0.25 0.5 0.75 1.0
  do
    ofpref="${ifname%.wav}_${volume}"
    ofname="${ofpref}.sln"
    sox --volume ${volume} "${infile}" --bits 16 --encoding signed-integer \
     --endian little "${ofname}" trim 0 0.1
    makeann "${ofname}" "${ofpref}"
    g729_ofname="${ofpref}.18"
    #${PYTHON_CMD} -m pipenv run ${PYTHON_CMD} read_g729_data.py "${g729_ofname}"
    mv "${g729_ofname}" "${TRDDIR_P}/"
    echo "Generated ${TRDDIR_P}/${g729_ofname}"
    sox --volume ${volume} "${infile}" --bits 16 --encoding signed-integer \
     --endian little "${ofname}" trim 0.01 0.11
    makeann "${ofname}" "${ofpref}"
    mv "${g729_ofname}" "${TRDDIR_N}/"
    echo "Generated ${TRDDIR_N}/${g729_ofname}"
  done
  for volume in 0.15 0.30 0.6 0.85 1.05
  do
    ofpref="${ifname%.wav}_${volume}"
    ofname="${ofpref}.sln"
    sox --volume ${volume} "${infile}" --bits 16 --encoding signed-integer --endian little "${ofname}" trim 0 0.1
    makeann "${ofname}" "${ofpref}"
    g729_ofname="${ofpref}.18"
    #${PYTHON_CMD} -m pipenv run ${PYTHON_CMD} read_g729_data.py "${g729_ofname}"
    mv "${g729_ofname}" "${TRDDIR_V}/"
    echo "Generated ${TRDDIR_V}/${g729_ofname}"
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

i=0
while nfile="${TRDDIR_V}/negative_${i}.18"
do
  dd if=white_noise.18 of="${nfile}" bs=100 count=1 skip=${i} 2>/dev/null
  if [ ! -s "${nfile}" ]
  then
    rm "${nfile}"
    break
  fi
  echo "Generated ${nfile}"
  i=$((${i} + 1))
done
