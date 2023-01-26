#!/bin/bash
fission spec init
fission env create --spec --name onb-br-steps-env --image nexus.sigame.com.br/fission-onboarding-br-steps:0.1.2 --poolsize 2 --graceperiod 3 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onb-br-steps-fn --env onb-br-steps-env --code fission.py --executortype poolmgr --requestsperpod 10000 --spec
fission route create --spec --method GET --url /onboarding/steps_br --function onb-br-steps-fn
