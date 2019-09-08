#!/bin/bash

echo 'publishing ...'

eval $(ssh-agent -s)
ssh-add <(echo "$DOC_PRIVATE_KEY")
ssh-keyscan -t rsa $DOC_HOSTNAME > ~/.ssh/known_hosts
scp -r ./pages/* $DOC_USER@$DOC_HOSTNAME:$DOC_LOCATION
