import os
from dotenv import load_dotenv
project_folder = os.path.expanduser('~/RetweetBot')
load_dotenv(os.path.join(project_folder, '.env'))

import sys
path = '/home/sahaay/Sahaay-Bot'
if path not in sys.path:
   sys.path.insert(0, path)

from bot import app as application
