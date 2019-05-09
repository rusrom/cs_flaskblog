# set environment variables for web apps
# https://help.pythonanywhere.com/pages/environment-variables-for-web-apps/
import os
from dotenv import load_dotenv

# activate environment variables inside .env file
project_folder = os.path.expanduser('~/cs_flaskblog')
load_dotenv(os.path.join(project_folder, '.env'))



# This file contains the WSGI configuration required to serve up your
# web application at http://<your-username>.pythonanywhere.com/
# It works by setting the variable 'application' to a WSGI handler of some
# description.
#
# The below has been auto-generated for your Flask project

import sys

# add your project directory to the sys.path
project_home = u'/home/runiro/cs_flaskblog'
if project_home not in sys.path:
    sys.path = [project_home] + sys.path

# import flask app but need to call it "application" for WSGI to work
from run import app as application  # noqa
