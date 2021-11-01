# Read in the configs
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/config.sh

HOST_NAME="$( hostname -i )"
PORT=${ports[$HOST_NAME]}

# Initialise the cluster
cockroach init \
--certs-dir=$SCRIPT_DIR/root-cert \
--host=$HOST_NAME:$PORT
