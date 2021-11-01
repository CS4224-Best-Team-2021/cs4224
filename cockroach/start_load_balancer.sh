# Run the config setup
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
source $SCRIPT_DIR/haproxy_config_setup.sh

# Check if a previous instance of a load balancer is running
PID_FILE=$SCRIPT_DIR/haproxy_pid.txt
if test -f "$PID_FILE"; then
    for i in $(cat $PID_FILE); do kill -9 $i; done
    rm $PID_FILE
fi

# Start HAProxy in the background
/sbin/haproxy -f haproxy.cfg -D -p $PID_FILE