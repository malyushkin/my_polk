#!/bin/bash

# pip
cd /home/uno/my_polk
source env/bin/activate

cd parsing

python inst_by_tag.py 'бессмертныйполкспб'
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 'бессмертныйполкмосква'
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 'бессмертныйполккраснодар'
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 'бессмертныйполкказань'
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 'бессмертныйполкуфа'
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 'бессмертныйполктюмень'
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 'бессмертныйполксочи'
wait
echo "..Parsing finished. Wait for next..."
sleep 60s

python inst_by_tag.py 'бессмертныйполкомск'
wait
echo "..Parsing finished. All done"

deactivate
