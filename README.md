# Description

Simple implementation for scheduling game data across different shifts. The algorithm loops through each shift, assigns 
games that have happened in the last 16 hours (for a 10am start) or 8 hours(for a 6pm start) plus anything that 
is left over from the previous shift. Games are scheduled at the start of the shift, and anything that comes in during
the shift is ignored and left for the next shift. Games are scheduled as full matches taking 8 or 10 hours, without 
splitting the games as two separate matches of 4 or 5 hours. 

Each game is assigned to a squad based on its looming deadline (time the match finished plus given hours for that games
competition priority). If the game has a preferred squad - they're assigned, otherwise the game goes to the squad
that has the most availability in that particular shift. 

The output is a csv file that gives us all our scheduled games plus any that haven't been assigned yet. 

* schedule.csv is the schedule for the games given in our input, eg:

        Date,Squad,Game ID,Late
        2019-04-01 10:00:00,E,49521,
    
    each row has a shift for it to be assigned to (Date), the game ID, a squad to work on both teams and if it is late, 
    how late that particular game is (Late).

* unassigned.csv is the schedule for the games given in our input, eg:

        Game ID,Deadline
        10002,2019-04-28 15:50:00
    
    each row has a game ID plus the deadline associated with the game.


# Setup

    python3 -m venv /path/to/new/virtual/env
    mac:
        source /path/to/new/virtual/env/bin/activate
    windows:
        /path/to/new/virtual/env/bin/activate
    pip install -r requirements.txt

# Endpoint 

post

http://127.0.0.1:5000/schedules

body (form-data):

    key: game_data (type file)
    value: competitiions.csv, matches.csv, preferences.csv, priorities.csv, schedule.csv
    
output:

    {
        "schedule": path/to/schedule.csv,
        "unfinished": "path/to/unfinished.csv
    }
    


# Run server on windows

in root directory

    $env:FLASK_APP = "server/views.py"  
    $env:FLASK_ENV= "development"
    python -m flask run
 
# Run server on mac
 
in root directory

    FLASK_ENV=development FLASK_APP="server/views.py" flask run  

 

