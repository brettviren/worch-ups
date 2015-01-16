#!/bin/bash

set -e

testdir=$(dirname $(readlink -f $BASH_SOURCE))
srcdir=$(dirname $testdir)

test_work_dir=test_gnups_distinct
echo "Working in $test_work_dir"

if [ ! -d "$test_work_dir" ] ; then
   mkdir -p "$test_work_dir"
   virtualenv $test_work_dir/venv
fi
source $test_work_dir/venv/bin/activate
if [ -n "$(pip list | grep worch-ups)" ] ; then
    pip uninstall -y worch-ups
fi
python setup.py sdist
pip install $(ls -t dist/worch-ups-*.tar.gz | head -1)

cd "$test_work_dir"

if [ ! -f wscript ] ; then
    cp $srcdir/wscript .
fi

if [ ! -x install/generic/hello/2.8/bin/hello ] ; then
    waf --version
    waf --prefix=install --orch-config="$srcdir/examples/gnups-distinct.cfg" configure 
    waf
fi

$testdir/test_gnups_ups_both.sh
