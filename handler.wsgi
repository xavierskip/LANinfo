import sys, os, logging
#logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from runserver import app as application
application.debug = True