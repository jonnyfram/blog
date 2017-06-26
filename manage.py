import os
from flask_script import Manager

from blog import app

manager = Manager(app)

#creates a command so below you can run this file as: python3 manage.py run
@manager.command
def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
    
if __name__ == "__main__":
    manager.run()