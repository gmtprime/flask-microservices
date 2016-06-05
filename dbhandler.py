from sqlalchemy.ext.automap import automap_base
from sqlalchemy import MetaData, create_engine
from flask_sqlalchemy import SQLAlchemy
import config


def name_for_scalar_relationship(base, local_cls, referred_cls, constraint):
    name = referred_cls.__name__.lower() + '_ref'
    return name


def name_for_collection_relationship(base, local_cls, referred_cls,
                                     constraint):
    name = referred_cls.__name__.lower() + '_col'
    return name


class DBHandler:
    def __init__(self, db_url, echo=False, exception_handler=None):
        """Initializes the database connection.

        Args:
            db_url (str): DB url (dialect+driver://username:password@host:port/database)
            echo (boolean): Enable SQLAlchemy's engine logger

        """
        self.url = db_url
        self.engine = create_engine(self.url, echo=echo, pool_size=20,
                                    max_overflow=30)
        self.metadata = MetaData()
        self.exception_handler = exception_handler
        self.Base = None
        self.Session = None

    def __getattr__(self, name):
        if self.Base is not None:
            return getattr(self.Base.classes, name)


    def initialize(self, app, only=None):
        """Initializes the schema.

        Args:
            app (Flask): Flask application
            only (list(str)): List of table names.

        Returns:
            A SQLAlchemy (flask-sqlalchemy) object

        """
        app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASES['default']
        self.db = SQLAlchemy(app)
        self.only = only
        self.metadata.reflect(self.engine, only=only)
        self.Base = automap_base(metadata=self.metadata)
        self.Base.prepare(name_for_scalar_relationship=name_for_scalar_relationship,
                          name_for_collection_relationship=name_for_collection_relationship)

        return self.db

    def get_postgres_url(self, username, password, hostname, port, database):
        """Generates the URL to connect to postgresql DB.

        Args:
            username (str): DB username.
            password (str): DB password.
            hostname (str): DB hostname.
            port (int): DB port.
            database (str): Database name.

        Returns:
            (str): URL to connect to the database.
        """
        args = (username, password, hostname, port, database)
        return 'postgresql://%s:%s@%s:%d/%s' % args
