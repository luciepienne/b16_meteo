d#!/bin/bash

# Change to the specified directory
cd ~/simplon/briefs/b16_meteo/github/

# Authenticate to the Azure Container Registry
docker login lpb16mateo.azurecr.io -u 

# Build and push the b16-connect image
cd b16mateo/conndb
dbt b16-connect .
docker tag b16-connect lpb16mateo.azurecr.io/connect:activateposgres
docker push lpb16mateo.azurecr.io/connect:activateposgres

# Wait for integration of FQDN
# Insert the FQDN manually in the instance created
echo "Please integrate the FQDN in the instance created. Waiting for 4 minutes..."
sleep 240

# Build and push the b16-load image
cd ../load
dbt b16-load .
docker tag b16-load lpb16mateo.azurecr.io/load:loadcitiesandforecasts
docker push lpb16mateo.azurecr.io/load:loadcitiesandforecasts

# Build and push the b16-api image
cd ../api
dbt b16-api .
docker tag b16-api lpb16mateo.azurecr.io/api:nlpwithforecasts
docker push lpb16mateo.azurecr.io/api:nlpwithforecasts

# Return to the original directory
cd ../../

