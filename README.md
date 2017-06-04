Movie recommendation app created with Flask and Bootstrap, using the Movielens 100k dataset.

Requirements:

`pip install -r requirements.txt`

You will need a Mysql connector and the bootstrap 3 files added to the [app/static](https://github.com/disfear86/Movie-Recommendations/tree/master/app/static) directory.

Set up the config.py file to inlude your database URI.

Run `python db_create.py` command from the terminal to initialize the database and `python create_combined_csv.py` to create a single csv file of all the data needed.
