Hello, here are the basic functionality for the front end.

WS - Winshares 
Definition: Win Shares is a player statistic which attempts to divvy up credit 
            for team success to the individuals on the team.
range: between 0 - 25.4 (all-time ws record)


2PA - 2 Point Attempts
Definition: The number of 2-point field goals that a player attempts that season. Shots
            taken within the three-point arc.
range: between 0 - 1300

FGA - Field Goal Attempts
Definition: The number of 2-point field goals and 3-point field goals that a player attempts
that season.
range: between 0 - 1700

2P - 2 Pointers Made
Definition: The number of 2-point field goals that a player makes that season. Shots
            taken within the three-point arc.
range: between 0 - 800

PTS - Points Made
Definition: The total number of points a player makes that season.
range: between 0 - 2800

FG - Field Goals Made
Definition: The number of 2-pointers and 3-pointers a player made that season.
range: between 0 - 900

# Instructions

## Front-end demo

Make sure there is `model` and `scaler` file under the folder. By defult they are provided, but you can run `polynomial_regressor.ipynb` to get these two files. They are ML models and scaler that we use pickle to store them locally for front-end page to run them.

Since we used flask, you would have to have the latest version of flask installed.
When in the project directory, run "flask --app app run". This will pull up the 
local host server where you can input the data and allow it to fetch.

Just enter the range corresponding to each catagory and hit submit to find the salray prediction!

## Code that we used to to write the report

We separated our models into three files: `classifiers.ipynb`, `mlp_regressor.ipynb` and `polynomial_regressor.ipynb`. Running each file from the beginning should produce