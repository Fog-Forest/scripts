#!/bin/bash
cd /root/kcptun/
echo "Stopping Kcptun..."
bash stop.sh
bash start.sh
echo "Kcptun started."
