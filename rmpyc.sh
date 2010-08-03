#!/bin/bash

rm -R -f `find . | grep .pyc$`
rm -R -f `find . | grep .svn$`
git rm -- `git ls-files --deleted` 
