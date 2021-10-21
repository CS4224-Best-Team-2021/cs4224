SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/config.sh

cockroach sql \
--certs-dir=$SCRIPT_DIR/root-cert \
--host=$SERVER1:${ports[$SERVER1]}
