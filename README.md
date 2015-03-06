# Cave Iconography Database

## Getting Started

[Download it as a zip file](https://github.com/airportyh/caves/archive/master.zip) and extract it by double clicking on the downloaded zip file. Then `cd` into the extracted directory:

    cd ~/Downloads/caves-master

See the database schema: [cave.sql](https://github.com/airportyh/caves/blob/master/cave.sql). Load it into a new sqlite database called `cave.sqlite`:

    sqlite3 cave.sqlite < cave.sql

See the data dump: [data.sql(https://github.com/airportyh/caves/blob/master/data.sql). Load it into the same database:

    sqlite3 cave.sqlite < data.sql

If this takes a few seconds: *that means it's working!*

Now, you can explore the data!

    sqlite3 cave.sqlite
    >

And type queries into the shell. Or alternatively, write a query in a `.sql` file and run it by

    sqlite3 cave.sqlite < query.sql

I wrote a list of questions that you'll be able to ask about the data: [QUESTIONS](https://github.com/airportyh/caves/blob/master/QUESTIONS), and I wrote some queries to answer those questions. I am sure you'll come up with your own more interesting questions.

## Your Assignment

1. Come up with your own questions to ask. Write them down.
2. Write SQL queries to answer them. Then get the answer by running the query.

You assignment is to 
