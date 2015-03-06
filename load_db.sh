#! /bin/bash

python run.py
sqlite3 cave.sqlite < cave.sql
sqlite3 cave.sqlite < data.sql