# Read in the configs
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/config.sh

# Get the specific variables of this machine
HOST_NAME="$( hostname -i )"
PORT=${ports[$HOST_NAME]}
STORE=${storenames[$HOST_NAME]}
HTTP_PORT=${https[$HOST_NAME]}
CERTS=${certs[$HOST_NAME]}

# Confirm to the user which IP address and port this machine will advertise and listen on
echo "This machine will advertise and listen on the address: $HOST_NAME:$PORT"

# Start the database
cockroach start \
--certs-dir=$SCRIPT_DIR/$CERTS \
--listen-addr=$HOST_NAME:$PORT \
--advertise-addr=$HOST_NAME:$PORT \
--join=$SERVER1:${ports[$SERVER1]},$SERVER2:${ports[$SERVER2]},$SERVER3:${ports[$SERVER3]},$SERVER4:${ports[$SERVER4]},$SERVER5:${ports[$SERVER5]} \
--cache=.25 \
--max-sql-memory=.25 \
--background \
--store=$SCRIPT_DIR/$STORE \
--http-addr=$HOST_NAME:$HTTP_PORT

