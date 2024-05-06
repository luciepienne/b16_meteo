d#!/bin/bash

# Change to the specified directory
cd ~/simplon/briefs/b16_meteo/github/

# Authenticate to the Azure Container Registry
docker login yourregisterazurename.azurecr.io -u yourregisterazure -p "yourpasswordazure"

# Build and push the b16-connect image
cd b16mateo/1conndb
dbt b16-connect1 .
docker tag b16-connect1 yourregisterazure.azurecr.io/connect1:activatepostgres
docker push yourregisterazure.azurecr.io/connect1:activatepostgres

# Wait for integration of FQDN
# Insert the FQDN manually in the instance created
echo "Please integrate the FQDN in the instance created. 
When you get the domainename of your instance b16-connect1, 
you can copy paste it in the port of your config.py files (x2 in b16mateo/2load ans in b16mateo/3nlpapi)
Waiting for 6 minutes..."
sleep 360

# Build and push the b16-load image
cd ../2load
dbt b16-load2 .
docker tag b16-load2 yourregisterazure.azurecr.io/load2:loadcitiesandforecasts
docker push yourregisterazure.azurecr.io/load2:loadcitiesandforecasts

# Build and push the b16-api image
cd ../3nlpapi
dbt b16-nlpapi3 .
docker tag b16-nlpapi3 yourregisterazure.azurecr.io/nlpapi3:nlpwithforecasts8002
docker push yourregisterazure.azurecr.io/nlpapi3:nlpwithforecasts8002

# Wait for integration of FQDN
# Insert the FQDN manually in the instance created
echo "Please integrate the FQDN in the instance created. 
When you get the domainename of your instance b16-nlpapi3, 
you can copy paste it in the port of your script.js file of your 4front repository and replace in line 47 and 92.
Waiting for 6 minutes..."
sleep 360

# Build and push the b16-front image
cd ../4front
dbt b16-front4 .
docker tag b16-front4 yourregisterazure.azurecr.io/front4:forecastsaudio3002
docker push yourregisterazure.azurecr.io/front4:forecastsaudio3002


# Return to the original directory
cd ../../


