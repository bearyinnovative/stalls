# -*- coding: utf-8 -*-

import os

from flask_script import Manager, Server

from poll.app import create_app


app_root = os.path.dirname(os.path.realpath(__name__))

application = create_app('Applet-Poll')
server = Server(port=5000)
manager = Manager(application)
manager.add_command("runserver", server)


@manager.option('-p', dest='port', help='Port to host', default=13800)
def run(port):
    """Run app at 0.0.0.0"""
    application.run(host='0.0.0.0', port=port, debug=True)


if __name__ == '__main__':
    manager.run()
