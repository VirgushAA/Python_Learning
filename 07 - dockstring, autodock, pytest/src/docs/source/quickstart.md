# Quickstart Guide

## Installation
Ensure you have Python installed, then install dependencies:
```sh
bash setup_venv
```
## Run
```
python main.py
```
#After each answer, a set of variables should be manually entered by a person asking the questions:

Respiration (measured in BPM, usually about 12-16 breaths per minute),

Heart rate (usually around 60 to 100 beats per minute),

Blushing level (categorical, 6 possible levels),

Pupillary dilation (current pupil size, 2 to 8 mm).

After ten questions and variable measurements, the test should print a strict binary decision as to whether a responding subject is a human or a replicant. In this exercise, you can invent your own logic to make this decision.
## Run tests
```
pytest
```
## Doc
```
cd docs
make html
```
For more detailed information look README