# If haproxy.cfg is missing or corrupt, run this script to rebuild it.

# Read in the configs
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/config.sh


cockroach gen haproxy \
--certs-dir=$SCRIPT_DIR/root-cert \
--host=$SERVER1:${ports[$SERVER1]} \
--port=7000