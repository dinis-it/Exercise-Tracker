# Exercise Tracker

Web app to track your workouts.



## Requirements

Python 3.8 or newer

## Setup

-Clone the repository
    git clone https://github.com/dinis-it/Exercise-Tracker.git

# Change into project directory
cd <project_name>

# Make virtual environment
mkvirtualenv <project_name>

# Activate virtual environment
workon <project_name>

# Install requirements
pip install -r requirements.txt

# Setup (if necessary)
fab loc setup

# Start the development server
python manage.py runserver

For user-specific settings, do not modify the loc.py file. Rather, create a .py settings file that imports the local settings. It is recommended that you push your user-specific settings into version control along with everything else, but should not include any secrets. To run the development server with your user-specific settings:

python manage.py runserver --settings=core.settings.<your username>

###DEPLOYMENT

Projects are deployed to the application user's home directory in: /home/apps/sites

Deployment is by direct clone from git. The name of the git repository will be the name of the directory in sites that is created by the git clone command.

# Do this once before the intial deployment (replace `stg` with `prd` for production)
fab stg setup

# Do this to deploy (replace `stg` with `prd` for production)
fab stg deploy

###REQUIRED ENVIRONMENT VARIABLES:

    DJANGO_SETTINGS_MODULE
    DJANGO_SECRET_KEY
    WORKON_HOME (set manually if not using mkvirtualenv)

