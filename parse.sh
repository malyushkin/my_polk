#!/bin/bash

export PYTHONIOENCODING=UTF-8
LC_CTYPE="en_US.UTF-8"

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
sleep 60s

python inst_by_tag.py 8
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 9
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 10
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 11
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 12
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 13
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 14
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 15
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 16
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 17
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 18
wait
echo "..Parsing finished. All done"sleep 60s
sleep 60s

python inst_by_tag.py 19
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 20
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 21
wait
echo "..Parsing finished. All done"
sleep 60s

python inst_by_tag.py 22
wait
echo "..Parsing finished. All done"

deactivate
