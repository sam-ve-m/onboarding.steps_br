#!/bin/bash
fission spec init
fission env create --spec --name onboarding-br-steps-env --image nexus.sigame.com.br/fission-onboarding-br-steps:0.1.0 --poolsize 0 --version 3 --imagepullsecret "nexus-v3" --spec
fission fn create --spec --name onboarding-br-steps-fn --env onboarding-br-steps-env --code fission.py --targetcpu 80 --executortype newdeploy --maxscale 3 --requestsperpod 10000 --spec
fission route create --spec --method GET --url /onboarding/steps_br --function onboarding-br-steps-fn
