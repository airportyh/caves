#! /bin/bash

python run.py
sqlite3 caves.sqlite < cave.toby.sql
sqlite3 caves.sqlite < data.sql