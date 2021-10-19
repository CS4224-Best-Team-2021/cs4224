# Read in the configs
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/config.sh

# Initialise the cluster
cockroach init \
--certs-dir=root-cert \
--host=$SERVER1:$PORT_1 \
--user=root