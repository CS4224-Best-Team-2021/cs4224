# If haproxy.cfg is missing or corrupt, run this script to rebuild it.

# Read in the configs
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/config.sh

HOST_NAME="$( hostname -i )"
PORT=${ports[$HOST_NAME]}

# Generate the config file for HAProxy
cockroach gen haproxy \
--certs-dir=$SCRIPT_DIR/root-cert \
--host=$HOST_NAME:$PORT 

# Replace the default port of the load balancer with some unused number, e.g. 7000
sed -i 's/26257/7000/g' haproxy.cfg

# Replace the maxconn to 100 to prevent hitting limit on FDs
sed -i 's/maxconn 4096/maxconn 100/g' haproxy.cfg

# Check that the config file is valid
/sbin/haproxy -f haproxy.cfg -c # Cannot use alias here for some reason