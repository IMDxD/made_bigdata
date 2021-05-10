cassandra_endpoint=$1
keyspace_name=$2

cqlsh ${cassandra_endpoint} -e "CREATE KEYSPACE IF NOT EXISTS ${keyspace_name} WITH REPLICATION = {'class': 'SimpleStrategy', 'replication_factor': 2}"
