# import os
# import ConfigParser
# config = ConfigParser.ConfigParser()
# config.read(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.ini'))
# print open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'config.ini')).read()
from web import app
# from db import database
# from scanner import win_mac, Scan

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5320, debug=True)