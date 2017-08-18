#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_DIR=$DIR/..
cd $PROJECT_DIR

py.test -v --alluredir=$PROJECT_DIR/reports $PROJECT_DIR
allure serve $PROJECT_DIR/reports/
