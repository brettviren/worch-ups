#!/bin/bash

set -e

testdir=$(dirname $(readlink -f $BASH_SOURCE))
srcdir=$(dirname $testdir)

test_work_dir=test_gnups_coincident
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

if [ ! -d install/hello/v2_8.version ] ; then
    waf --version
    waf --prefix=install --orch-config="$srcdir/examples/gnups-coincident.cfg" configure 
    waf
fi

# coincident can be used in-placed
/bin/bash -c 'source `pwd`/install/setups && ups list -aK+' || exit 1
/bin/bash -c 'source `pwd`/install/setups && setup hello v2_8 -q x0:opt && which hello && hello' || exit 1

$testdir/test_gnups_ups_both.sh

