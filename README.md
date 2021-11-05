# cs4224
Using Apache Cassandra and CockroachDB to experiment with distributed database management systems.

## Setup instructions
### First steps
- Install CockroachDB according to the [official instructions](https://www.cockroachlabs.com/docs/v21.1/install-cockroachdb-linux).
- Official repo [here](https://github.com/CS4224-Best-Team-2021/cs4224).

## Specific steps for troubleshooting CockroachDB
### To download a fresh set of project files:
- Run `bash download_data.sh` inside `common/scripts` on any server from `xcnc20-24` (or whichever server you are running this project on).
- Check that the folder `common/project_files_4` exists.

### Setting the configs for CockroachDB
- Inside `cockroach/`, the file called `config.sh` and `load_balancer.sh` contain server specific configurations.
- `config.sh` contains the ip addresses, http ports and tcp ports of the 5 servers.
- `load_balancer.sh` contains the ip addresses and tcp ports of the 5 servers.
- If you are not using `xcnc20-24` as your five servers, you need to change the configs in these 2 files.
### To start a CockroachDB cluster:
If you want to start a completely fresh cluster, start here. Else if a cluster is already live and you just want to reset the database, go do the next section:
- Run `pkill cockroach` on all servers to kill any existing cluster.
  > On `xcnc20` you will see that some processes cannot be terminated by us. That's ok as long as you see the message from Cockroach about gracefully shutting down the server.
- Run `rm -rf store*` inside `cockroach/` on any server to remove old session data. (Only do this if you want to remove your existing database!)
  > If you see a message like `resource busy`, run `netstat -ltnp` and check for any PIDs of old Cockroach processes, and then run `kill -9 <pid number>` on all of them.
- Run `bash start.sh` (scripts are inside `cockroach/`) to start CockroachDB on any server.
- Run `bash init.sh` on just 1 server to initialise a cluster. (You only need to run this if you removed all the `store*` folders in step 2).
- Run `bash status.sh` on the same server to check that the cluster is live.
- On the other four servers, run `bash start.sh` to start CockroachDB on every other machine. They will try to join the cluster automatically.
- Run `bash status.sh` on any server to check that the cluster contains 5 machines inside the cluster.
> If a cluster is already running and you just want to reset the database, go to the next section.
 ### To install/reset `wholesaledb`:
- Ensure that the project files have been downloaded.
- Ensure the cluster is running by running `bash status.sh`. If not go to the previous section.
- Run `bash create-db.sh` on any machine with the project files to create the database `wholesaledb`.
  - The script will ask for `a/b`, so choose a or b depending on your workload.  
### To start a SQL session:
- Start the CockroachDB cluster.
- Run `bash sql_cli.sh` on any machine.

### To run all 40 clients:
- Make sure `wholesaledb` has been initialised.
- Run `bash load_balancer.sh` inside `cockroach/`, selecting a or b for the workload.
- Run `ps aux | grep <your username>` to see if 40 clients have started.
- The results of the 40 clients will be written into `results/`.
- Use `tail -f 0-A.txt` for example to see real-time updates.
- If some python scripts seem to hang, run `bash sql_cli.sh` inside `cockroach`.
- When you are in the sql client, run `show statements;` to see the queries that are running.
- If any query is hanging, look for the query id in the first column, and run `cancel query '<query id>;'` to kill the query.
- The client-side restart loop should take effect in the respective Python client.

### If you get an error stating that the cert files are not executable:
- Run the script `make_certs_exe.sh` inside `cs4224` to duplicate the folders. The error should go away.
