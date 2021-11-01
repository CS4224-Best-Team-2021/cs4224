# cs4224
Using Apache Cassandra and CockroachDB to experiment with distributed database management systems.

## Project organization
### Folder structure
This repository has three folders, one for each DDBMS and one for common files (e.g. raw data/queries/bash scripts for setup).

### Branch structure
This repository has three branches. 
- `main` branch contains the latest stable release of the two branches. 
- The other two is for each group to do their development, so that breaking changes in the common files folder don't affect both groups at the same time.

## Setup instructions
### First steps
- Install CockroachDB and Apache Cassandra.
- Run `setup.sh` to run all setup scripts.

## Specific steps for troubleshooting
### To download a fresh set of project files:
- Run `bash download_data.sh` inside `common/scripts` on `xcnc20`.
- Check that the folder `common/project_files_4` exists on `xcnc20`.

> Note that all bash files can be run from anywhere, the file resolution will work fine (e.g. you can run `bash` from `cs4224/` or inside the directory containing the script, both will work).


### To start a CockroachDB cluster:
- Run `pkill cockroach` on all servers to kill any existing cluster.
  > On `xcnc20` you will see that some processes cannot be terminated by us. That's ok as long as you see the message from Cockroach about gracefully shutting down the server.
- Run `rm -rf store*` inside `temp/cs4224/cockroach/` on `xcnc20` and `xcnc24` to remove old session data. (Only do this if you want to remove your existing database!)
  > If you see a message like `resource busy`, run `netstat -ltnp` and check for any PIDs of old Cockroach processes, and then run `kill -9 <pid number>` on all of them.
- Run `bash start.sh` (scripts are inside `cockroach/`) to start CockroachDB on `xcnc20`.
- Run `bash init.sh` on just 1 server to initialise a cluster. (You only need to run this if you removed all the `store*` folders in step 2).
- Run `bash status.sh` on the same server to check that the cluster is live.
- On the other four servers, run `bash start.sh` to start CockroachDB on every other machine. They will try to join the cluster automatically.
- Run `bash status.sh` on any server to check that the cluster contains 5 machines inside the cluster.
- If you removed all the `store*` folders in step 2, run `bash create-db.sh` to initialise the database. You can rerun this script anytime to reset the database. 
- The script will ask for `a/b`, so choose a or b depending on your workload.
- To start/restart the load balancer, run `bash start_load_balancer.sh`, this script calls `haproxy_config_setup.sh` automatically to re-check which servers are in the cluster and configure the load balancer for those servers.
- If you want to rebuild the `haproxy.cfg` file at any time, run the `haproxy_config_setup.sh` script alone.
 ### To install/reset `wholesaledb`:
- Ensure that the project files have been downloaded.
- Start the CockroachDB cluster.
- Run `bash create-db.sh` on any machine with the project files to create the database `wholesaledb`.
  
### To start a SQL session:
- Start the CockroachDB cluster.
- Run `bash sql_cli.sh` on any machine.
