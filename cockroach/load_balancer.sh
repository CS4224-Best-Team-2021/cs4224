# Ask for the workload type
workload="c"
while [[ "$workload" != "a" && "$workload" != "b" ]]
do
    read -p "Enter workload (a/b): " workload
done

# Uppercase the workload type
workload=$(echo "$workload" | tr a-z A-Z)

# Create aliases for all servers
declare -A servers
servers[0]=192.168.48.169 
servers[1]=192.168.48.170 
servers[2]=192.168.48.171 
servers[3]=192.168.48.172 
servers[4]=192.168.48.173

# Set LAN address and ports
declare -A ports
ports[0]=5001
ports[1]=5002
ports[2]=5003
ports[3]=5004
ports[4]=5005

# Clean out the results folder
rm -rf ~/temp/cs4224/cockroach/results && mkdir ~/temp/cs4224/cockroach/results

for c in {0..39}
do
    # Calculate the index of the server
    idx=$[$c % 5]
    # Construct the ip address
    ipaddr=${servers[$idx]}:${ports[$idx]}
    # Run main.py (must do this from cockroach/)
    echo "Sending $c.txt to $ipaddr"
    python3 python/main.py "postgresql://root@$ipaddr/wholesaledb?sslcert=root-cert/client.root.crt&sslkey=root-cert/client.root.key&sslmode=verify-ca&sslrootcert=root-cert/ca.crt" $c < ../common/project_files_4/xact_files_$workload/$c.txt > results/$c-$workload.txt &
done