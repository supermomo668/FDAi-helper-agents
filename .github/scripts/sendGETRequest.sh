#!/bin/bash

# Extract environment variables passed from the workflow
BASE_URL=$1
QUERY_PARAMS=$2
HEADERS_SECRET=$3

# Decode the headers secret to get the actual headers
HEADERS=$(echo $HEADERS_SECRET | base64 --decode)

# Prepare the URL
URL="${BASE_URL}${QUERY_PARAMS}"

# Make the curl request
RESPONSE=$(curl -s -X GET "$URL" $HEADERS)

# Format the response to be script safe and store it in an environment variable for the workflow
FORMATTED_RESPONSE=$(echo "$RESPONSE" | jq -r '"\(.response)\nContext:\n\(.context | join("\n"))"')

# Output the formatted response so it can be captured by the calling workflow
echo "$FORMATTED_RESPONSE"
