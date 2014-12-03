#!/bin/bash

set -e

testdir=$(dirname $(readlink -f $BASH_SOURCE))
srcdir=$(dirname $testdir)

test_work_dir=test_gnups_distinct
echo "Working in $test_work_dir"

if [ ! -d "$test_work_dir" ] ; then
   mkdir -p "$test_work_dir"
fi
cd "$test_work_dir"

if [ ! -f wscript ] ; then
    cp $srcdir/wscript .
fi

waf="$srcdir/waf"
$waf --version
$waf --prefix=install --orch-config="$srcdir/examples/gnups-distinct.cfg" configure 
$waf



upsproducts=`pwd`/upsproducts

# this should be in PATH in virtualenv since worch-ups depends on ups-utils
urman -z $upsproducts init || exit 1

for tarball in tmp/upspack/*.tar.bz2
do
    echo "$tarball --> $upsproducts"
    tar -C $upsproducts -xf $tarball 
done

/bin/bash -c "source $upsproducts/setups && ups list -aK+" || exit 1
/bin/bash -c "source $upsproducts/setups && setup hello v2_8 -q x0:opt && which hello && hello" || exit 1
