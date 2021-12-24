#!/bin/bash
cd /root/kcptunclient
command=`ls| grep .json`
echo $command
for loop in $command
do
    ./client_linux_amd64 -c /root/kcptunclient/$loop 2>&1 &
done
echo "Kcptun started."