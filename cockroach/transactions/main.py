import time
import random
import logging

import psycopg2
from psycopg2.errors import SerializationFailure

from stock_level import stock_level_transaction
from popular_item import popular_item_transaction
from top_balance import top_balance_transaction
from related_customer import related_customer_transaction

def run_transaction(conn, op, max_retries=3):
    """
    Execute the operation *op(conn)* retrying serialization failure.

    If the database returns an error asking to retry the transaction, retry it
    *max_retries* times before giving up (and propagate it).
    """
    # leaving this block the transaction will commit or rollback
    # (if leaving with an exception)
    with conn:
        for retry in range(1, max_retries + 1):
            try:
                op(conn)

                # If we reach this point, we were able to commit, so we break
                # from the retry loop.
                return

            except SerializationFailure as e:
                # This is a retry error, so we roll back the current
                # transaction and sleep for a bit before retrying. The
                # sleep time increases for each failed transaction.
                logging.debug("got error: %s", e)
                conn.rollback()
                logging.debug("EXECUTE SERIALIZATION_FAILURE BRANCH")
                sleep_ms = (2 ** retry) * 0.1 * (random.random() + 0.5)
                logging.debug("Sleeping %s seconds", sleep_ms)
                time.sleep(sleep_ms)

            except psycopg2.Error as e:
                logging.debug("got error: %s", e)
                logging.debug("EXECUTE NON-SERIALIZATION_FAILURE BRANCH")
                raise e

        raise ValueError(f"Transaction did not succeed after {max_retries} retries")


def main():
    '''
    conn = psycopg2.connect(opt.dsn)
    try:
        run_transaction(conn, lambda conn: some_transaction(conn, fromId, toId, amount))
    except ValueError as ve:
        logging.debug("run_transaction(conn, op) failed: %s", ve)
        pass
    '''
    pass
