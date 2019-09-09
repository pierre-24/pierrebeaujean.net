#!/usr/bin/env bash

echo "Deploying..."

NAME="pierre-24"
REPO="pierrebeaujean.net"
HTML_DOC_DIR="pages"

# config GIT
git config --global user.email "travis@travis-ci.org"
git config --global user.name "travis-ci"

# push doc
git add $HTML_DOC_DIR -f
git commit -m "Deploy"
git subtree split --branch build_doc --prefix $HTML_DOC_DIR
git push https://$NAME:$GITHUB_API_KEY@github.com/$NAME/$REPO build_doc:gh-pages -fq > /dev/null 2>&1

echo "... Done!"
