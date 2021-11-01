# Run the config setup
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/haproxy_config_setup.sh

# Start HAProxy in the background
/sbin/haproxy -f haproxy.cfg -D