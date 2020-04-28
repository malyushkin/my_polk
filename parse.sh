#!/bin/bash

# pip
cd /home/uno/my_polk
source env/bin/activate

cd parsing

python inst_by_tag.py 0
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 1
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 2
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 3
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 4
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 5
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 6
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 7
wait
echo "..Parsing finished. All done"

deactivate
