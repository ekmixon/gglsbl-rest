import logging.config
from os import environ, path

from gglsbl import SafeBrowsingList

# basic app configuration and options
gsb_api_key = environ['GSB_API_KEY']
dbfile = path.join(environ.get('GSB_DB_DIR', '/tmp'), 'sqlite.db')
logger = logging.getLogger('update')


# function that updates the hash prefix cache if necessary
def update_hash_prefix_cache():
    logger.info(f'opening database at {dbfile}')
    sbl = SafeBrowsingList(gsb_api_key, dbfile, True)

    logger.info(f'updating database at {dbfile}')
    sbl.update_hash_prefix_cache()

    logger.info(f'checkpointing database at {dbfile}')
    with sbl.storage.get_cursor() as dbc:
        dbc.execute('PRAGMA wal_checkpoint(FULL)')
    sbl.storage.db.commit()

    logger.info("all done!")


if __name__ == '__main__':
    logging.config.fileConfig(environ.get("LOGGING_CONFIG", 'logging.conf'))
    update_hash_prefix_cache()
