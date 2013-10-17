""" Commandline scripts """
from pyramid.paster import bootstrap
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker

from .models import create_schema, drop_schema, Package


def setup(description):
    """ Parse the config_uri from arguments and bootstrap the script """
    import argparse
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('config_uri')

    args = vars(parser.parse_args())

    return bootstrap(args['config_uri'])


def run_create_schema():
    """ Create the schema for the sqlalchemy database """
    env = setup(run_create_schema.__doc__)
    create_schema(env['registry'])
    print "Success!"


def run_drop_schema():
    """ Drop all tables and schema from the sqlalchemy database """
    env = setup(run_drop_schema.__doc__)
    drop_schema(env['registry'])
    print "Success!"


def run_refresh_packages():
    """ Clear the database and refresh packages from S3 """
    env = setup(run_refresh_packages.__doc__)
    settings = env['registry'].settings
    engine = engine_from_config(settings, prefix='sqlalchemy.')
    session = sessionmaker(bind=engine)()
    session.query(Package).delete()
    session.commit()
    session.close()
    print "Success!"
