#!/bin/bash
PID=`ps -ef | grep client_linux_amd64 | grep -v grep | awk '{print $2}'`
if [ "" != "$PID" ]; then
 echo "killing $PID"
 kill -9 $PID
else
 echo "Kcptun not running!"
fi
