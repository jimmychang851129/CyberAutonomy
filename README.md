# Cyber Autonomy

## setup
用virtualenv 建立python3.6
virtualenv使用教學請看[note](https://hackmd.io/gnNUv5YOQdin9mHmafaEqg?both)
用python3.6 pip install requirements.txt

## environment

python == 3.6

pip3 install requirements.txt

## Django tutorial & note

[note](https://hackmd.io/gnNUv5YOQdin9mHmafaEqg?both)

[tutorial](https://www.youtube.com/watch?v=F5mRW0jo-U4)

## File introduction

all Django application source code are in src/ directory

### Content provider

- src/CPAnalysis : Content provider related code
	- views.py : define behavior when an request sent to CPAnalysis

### Homepage

- src/homepage : homepage of this government website crawling project
	- views.py : homepage request behavior


### templates

stored all html files

### govwebsite

default directory for this project
define the template path and all routing path, etc

