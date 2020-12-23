#!/bin/bash

#conda activate falcon # activating virtual environment required to run the project
echo 'Running pre-processor'
python pre_processor.py
sleep 2

echo ''
echo 'Running equalizer'
python equalizer.py
sleep 2

echo ''
echo 'Running regressor'
python regressor.py
sleep 2

echo ''
echo 'Running plotter'
python plotter.py
sleep 2
#python plotter.py
