SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/config.sh

# Get the hostname of this server
HOST_NAME="$( hostname -i )"
PORT=${ports[$HOST_NAME]}

cockroach sql \
--certs-dir=$SCRIPT_DIR/root-cert \
--host=$HOST_NAME:$PORT \
--database=wholesaledb

