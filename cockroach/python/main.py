import time
import random
import logging
import sys
import argparse

import psycopg2

from transactions import (
    stock_level_transaction,
    popular_item_transaction,
    related_customer_transaction,
    top_balance_transaction,
)

NEW_ORDER = "N"
PAYMENT = "P"
DELIVERY = "D"
ORDER_STATUS = "O"
STOCK_LEVEL = "S"
POPULAR_ITEM = "I"
TOP_BALANCE = "T"
RELATED_CUSTOMER = "R"


def run_transaction(conn, op, max_retries=3):
    """
    Copied from https://www.cockroachlabs.com/docs/stable/build-a-python-app-with-cockroachdb.html
    Execute the operation *op(conn)* retrying serialization failure.

    If the database returns an error asking to retry the transaction, retry it
    *max_retries* times before giving up (and propagate it).
    """
    with conn:
        for retry in range(1, max_retries + 1):
            try:
                op(conn)

                # If we reach this point, we were able to commit, so we break from the retry loop.
                return
            except psycopg2.Error as e:
                logging.debug("got error: %s", e)
                logging.debug("EXECUTE NON-SERIALIZATION_FAILURE BRANCH")
                raise e

        raise ValueError(f"Transaction did not succeed after {max_retries} retries")


def main():
    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument("dsn", help="Database connection string")
    parser.add_argument("client_number")
    opt = parser.parse_args()

    logging.basicConfig(level=logging.DEBUG)
    conn = psycopg2.connect(dsn=opt.dsn)

    line = sys.stdin.readline()
    num_transactions_processed = 0
    processing_times = []

    while line:
        if not line:
            break

        num_transactions_processed += 1
        op = None
        params = []
        tokens = line.split()
        command = tokens[0]

        if command == "N":
            c_id, w_id, d_id, m = tuple(map(int, tokens[1:]))
            for _ in range(m):
                line = sys.stdin.readline()
                if line:
                    params = tuple(map(int, line.split()))

        elif command == "P":
            c_w_id, c_d_id, c_id, payment = tokens[1:]

        elif command == "D":
            w_id, carrier_id = tokens[1:]

        elif command == "O":
            c_w_id, c_d_id, c_id = tokens[1:]

        elif command == "S":
            params = tuple(map(int, tokens[1:]))
            op = stock_level_transaction
        elif command == "I":
            params = tuple(map(int, tokens[1:]))
            op = popular_item_transaction
        elif command == "T":
            op = top_balance_transaction
        elif command == "R":
            params = tuple(map(int, tokens[1:]))
            op = related_customer_transaction

        try:
            start = time.time()
            run_transaction(conn, lambda conn: op(conn, *params))
            transaction_processing_time = int((time.time() - start) * 1000)
            processing_times.append(transaction_processing_time)

        except ValueError as ve:
            logging.debug("run_transaction(conn, op) failed: %s", ve)
            pass

    total_processing_time = sum(processing_times)
    total_processing_time_seconds = total_processing_time / 1e9
    transaction_throughput = num_transactions_processed / total_processing_time_seconds
    average_transaction_latency_millis = (
        total_processing_time / 1e6 / num_transactions_processed
    )
    sorted_processing_times_millis = sorted([n / 1e6 for n in processing_times])
    median_processing_time = sorted_processing_times_millis[
        num_transactions_processed // 2
    ]
    _95_percentile_processing_time = sorted_processing_times_millis[
        int(0.95 * num_transactions_processed)
    ]
    _99_percentile_processing_time = sorted_processing_times_millis[
        int(0.99 * num_transactions_processed)
    ]
    print(
        opt.client_number,
        total_processing_time,
        total_processing_time_seconds,
        transaction_throughput,
        average_transaction_latency_millis,
        median_processing_time,
        _95_percentile_processing_time,
        _99_percentile_processing_time,
    )


if __name__ == "__main__":
    main()
