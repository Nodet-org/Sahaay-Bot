import sys
path = '/home/sahaay/Sahaay-Bot'
if path not in sys.path:
   sys.path.insert(0, path)

from bot import app as application
