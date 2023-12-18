import os

from flask import Flask

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.abspath(os.path.join(app.instance_path, 'Formula1.sqlite')),
    )

    # if test_config is None:  #bu kısım test ile alakalı
    #     # load the instance config, if it exists, when not testing
    #     app.config.from_pyfile('config.py', silent=True)
    # else:
    #     # load the test config if passed in
    #     app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/hello')
    def hello():
        return 'Welcome to the project owned by\n Eda Işık, Semih Gençten, Yasin İbiş'

    from . import db
    db.init_app(app)

    from . import drivers
    app.register_blueprint(drivers.bp)
    app.add_url_rule('/drivers', endpoint='drivers')


    from . import constructors
    app.register_blueprint(constructors.bp)
    app.add_url_rule('/constructors', endpoint='constructors')

    from . import auth
    app.register_blueprint(auth.bp)

    from . import races
    app.register_blueprint(races.bp)
    app.add_url_rule('/races', endpoint='races')
    
    from . import home
    app.register_blueprint(home.bp)
    app.add_url_rule('/', endpoint='index')




    return app