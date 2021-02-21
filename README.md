# G.729 to DTMF AI

## About

This project is set out to explore the possibility of applying deep learning
and (R)NN to detect various features in industry-standard speech low-bitrate
codecs (such as ITU-T's G.729[ab] for example) while operating on codec data
directly, without decoding the audio and then applying MFCC conversion to raw
audio data.

The goal is to build a usable pre-trained ML model and set of simple
transformations allowing to process stream of G.729 frames and output DTMF
codes with minimal latency and maximal accuracy.

## Who?

- Maksym Sobolyev <sobomax@sippysoft.com>
- Giovanni Maruzzelli <gmaruzz@opentelecom.it>

## Plan of the Attack

 - [x] Generate some sample data
 - [x] Build visual representation of the G.729 coefficients as function of time
 - [x] Apply our natural NNs (i.e. visual cortexes) to spot any patterns
 - [ ] Apply our neo cortexes + prior art (i.e. MFCC itself) and programming skills
       to massage data to make patterns more obvious
 - [ ] Design, build a neural net to detect those patterns
 - [ ] Test, train
 - [ ] Rinse and Repeat
 - [ ] Profit?

## Links

- http://practicalcryptography.com/miscellaneous/machine-learning/guide-mel-frequency-cepstral-coefficients-mfccs/
- https://arxiv.org/pdf/1410.7455v4.pdf
- https://github.com/jameslyons/python_speech_features
- http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.185.1908&rep=rep1&type=pdf
- https://www.audiocheck.net/audiocheck_dtmf.php
