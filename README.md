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