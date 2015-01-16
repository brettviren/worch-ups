
upsproducts=`pwd`/upsproducts
mkdir -p $upsproducts
for tarball in tmp/upspack/*.tar.bz2
do
    echo "$tarball --> $upsproducts"
    tar -C $upsproducts -xf $tarball 
done

/bin/bash -c "source $upsproducts/setups && ups list -aK+" || exit 1
/bin/bash -c "source $upsproducts/setups && setup hello v2_8 -q x0:opt && which hello && hello" || exit 1
