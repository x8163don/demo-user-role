from flask import Flask

import application

app = Flask(__name__)

for bp in application.all_blueprints:
    app.register_blueprint(bp)

if __name__ == '__main__':
    app.run()
