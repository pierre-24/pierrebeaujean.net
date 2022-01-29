#!/usr/bin/env bash

echo "Deploying..."

# git
git config --local user.email "action@github.com"
git config --local user.name "GitHub Action"

# make
make gen

# go to gh-page
git checkout gh-pages

# cleanup everything
git rm -rf .

# move new stuffs
mv build/* .
rm -R build/
git add .
git commit --allow-empty -m "Add change"

echo "... Done!"
