#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

docker run automation_test_image py.test -v -m meta --alluredir=/usr/local/automation_tests/reports /usr/local/automation_tests
