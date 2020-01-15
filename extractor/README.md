
# Horkos Extractor

## Summary

This extractor compares new revision based data to previous data using a variety of statistical techniques. Individual scores are assigned for each technique. Weights are applied to individual scores to provide an overall score for the record. If the overall score is above a user-defined threshold then it is inserted into the database as an "Issue".

### Motivation

The Horkos Extractor was created to quickly identify outliers in revision based data. Once outliers are identified, they are inserted into a database to be reviewed by a user.


### Intended Use
Run periodically to detect outlier in the database based on user entered queries in the connect `horkos` database.

## Architecture
In progress...

### Communication
In progress...

### Technology Stack
* Python 3.6.7
* Virtualenv
* Libraries
    * Math
        * numpy
        * scipy
    * Database
        * pymssql
        * PyMySQL


### Dependencies
Libraries required are found in requirements.txt
The application relies on a connection to the `horkos` database. Target database connections are also required depending on queries being executed.

## Configuration
Curently, config is defined within the app.py file, it will move to an external config file in the future. Only the three database connections need to be defined.

## Local Stand Up
```
source bin/activate
pip install -r requirements.txt
cd horkos_extractor
python app.py
```

## How to Use
Since the application pulls all queries from the database. A user will need to use the `horkos-ui` to make any changes. Run with the --train flag to set the score_thresholds for the statistical queries.

## FAQ
How do I manage queries?
* Queries can be managed in the `horkos-ui`.

How can I see the results?
* Results are displayed in an easy to read table in the `horkos-ui`. For debugging, the results will also be printed to stdout.

