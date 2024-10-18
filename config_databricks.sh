#!/bin/bash

# Create the databricks-cli-config dynamically
cat << EOF > /root/.databrickscfg
[DEFAULT]
host = ${DATABRICKS_HOST}
token = ${DATABRICKS_TOKEN}
cluster_id = ${DATABRICKS_CLUSTER_ID}
EOF