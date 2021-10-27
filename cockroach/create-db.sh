# Ask for the workload type
workload="c"
while [[ "$workload" != "a" && "$workload" != "b" ]]
do
    read -p "Enter workload (a/b): " workload
done

# Read in the configs
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/config.sh

# Creates an empty database using init_db_a.sql or init_db_b.sql 
if [[ $workload == "a" ]]
then
    cockroach sql -f=$SCRIPT_DIR/schema/init_db_a.sql --certs-dir=$SCRIPT_DIR/root-cert --host=$SERVER1:${ports[$SERVER1]}
else
    cockroach sql -f=$SCRIPT_DIR/schema/init_db_b.sql --certs-dir=$SCRIPT_DIR/root-cert --host=$SERVER1:${ports[$SERVER1]}
fi

# Import each CSV file into the database
cockroach sql -e="use wholesaledb; IMPORT INTO warehouse CSV DATA ('nodelocal://self/warehouse.csv');" --certs-dir=$SCRIPT_DIR/root-cert --host=$SERVER1:${ports[$SERVER1]}
cockroach sql -e="use wholesaledb; IMPORT INTO district CSV DATA ('nodelocal://self/district.csv');" --certs-dir=$SCRIPT_DIR/root-cert --host=$SERVER1:${ports[$SERVER1]}
cockroach sql -e="use wholesaledb; IMPORT INTO customer CSV DATA ('nodelocal://self/customer.csv');" --certs-dir=$SCRIPT_DIR/root-cert --host=$SERVER1:${ports[$SERVER1]}
cockroach sql -e="use wholesaledb; IMPORT INTO wholesaledb.order CSV DATA ('nodelocal://self/order.csv') WITH nullif = 'null';" --certs-dir=$SCRIPT_DIR/root-cert --host=$SERVER1:${ports[$SERVER1]}
cockroach sql -e="use wholesaledb; IMPORT INTO item CSV DATA ('nodelocal://self/item.csv');" --certs-dir=$SCRIPT_DIR/root-cert --host=$SERVER1:${ports[$SERVER1]}
cockroach sql -e="use wholesaledb; IMPORT INTO order_line CSV DATA ('nodelocal://self/order-line.csv') WITH nullif = 'null';" --certs-dir=$SCRIPT_DIR/root-cert --host=$SERVER1:${ports[$SERVER1]}
cockroach sql -e="use wholesaledb; IMPORT INTO stock CSV DATA ('nodelocal://self/stock.csv');" --certs-dir=$SCRIPT_DIR/root-cert --host=$SERVER1:${ports[$SERVER1]}

cockroach sql -f=$SCRIPT_DIR/schema/views.sql --certs-dir=$SCRIPT_DIR/root-cert --host=$SERVER1:${ports[$SERVER1]}
