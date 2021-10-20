SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cockroach node status --host=192.168.48.169:5001 --certs-dir=$SCRIPT_DIR/root-cert