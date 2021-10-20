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

### For CockroachDB dev testing:
> Note that all bash files can be run from anywhere, the file resolution will work fine (e.g. you can run `bash` from `cs4224/` or inside the directory containing the script, both will work).
- If you want a fresh set of files, run `bash download_data.sh` inside `common/scripts`.
- Run `rm -rf store*` inside `temp/cs4224/cockroach/` to remove old session data.
- Run `pkill cockroach` to kill any existing cluster.
- Run `bash start.sh` (scripts are inside `cockroach/`) to start CockroachDB on `xcnc20`.
- Run `bash init.sh` on `xcnc20` to initialise a cluster.
- Run `bash status.sh` on `xcnc20` to check that the cluster is live.
- On `xcnc21-24`, run `bash start.sh` to start CockroachDB on every other machine. They will try to join the cluster automatically.
- Run `bash status.sh` on `xcnc20` to check that the cluster contains 5 machines inside the cluster.
- Run `bash create-db.sh` on `xcnc20` to create the database `wholesaledb`.
  