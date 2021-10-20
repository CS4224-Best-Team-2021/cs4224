# Read in the configs
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/config.sh

# Creates an empty database using init_db.sql 
# TODO if testing on local machine, change certs dir to the file your client cert is in
cockroach sql -f=$SCRIPT_DIR/schema/init_db.sql --certs-dir=root-cert

# Import each CSV file into the database
cockroach sql -e="use wholesaledb; IMPORT INTO warehouse CSV DATA ('nodelocal://self/warehouse.csv');" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO district CSV DATA ('nodelocal://self/district.csv');" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO customer CSV DATA ('nodelocal://self/customer.csv');" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO wholesaledb.order CSV DATA ('nodelocal://self/order.csv') WITH nullif = 'null';" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO item CSV DATA ('nodelocal://self/item.csv');" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO order_line CSV DATA ('nodelocal://self/order-line.csv') WITH nullif = 'null';" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO stock CSV DATA ('nodelocal://self/stock.csv');" --certs-dir=root-cert
