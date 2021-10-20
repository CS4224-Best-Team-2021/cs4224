# Creates an empty database using init_db.sql 
# TODO if testing on local machine, change certs dir to the file your client cert is in
cockroach sql -f=cockroach/schema/init_db.sql --certs-dir=root-cert

# Upload all CSV files to userfile
SCRIPT_DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
for f in $(ls $SCRIPT_DIR/../common/project_files_4/data_files)
do 
    cockroach userfile delete $f --certs-dir=root-cert
    cockroach userfile upload $SCRIPT_DIR/../common/project_files_4/data_files/$f --certs-dir=root-cert
done

# Import each CSV file into the database
cockroach sql -e="use wholesaledb; IMPORT INTO warehouse CSV DATA ('userfile:///warehouse.csv');" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO district CSV DATA ('userfile:///district.csv');" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO customer CSV DATA ('userfile:///customer.csv');" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO wholesaledb.order CSV DATA ('userfile:///order.csv') WITH nullif = 'null';" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO item CSV DATA ('userfile:///item.csv');" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO order_line CSV DATA ('userfile:///order-line.csv') WITH nullif = 'null';" --certs-dir=root-cert
cockroach sql -e="use wholesaledb; IMPORT INTO stock CSV DATA ('userfile:///stock.csv');" --certs-dir=root-cert

