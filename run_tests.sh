#!/bin/bash

# Use AWS CLI to configure the credentials
aws configure set aws_access_key_id "$AWS_ACCESS_KEY_ID"
aws configure set aws_secret_access_key "$AWS_SECRET_ACCESS_KEY"
aws configure set region "$AWS_REGION"
aws configure set output "$AWS_OUTPUT_FORMAT"

# Verify configuration
aws configure list

# Change kubectl context
aws eks update-kubeconfig --region "$AWS_REGION" --name "$CLUSTER_NAME"

cd tests/

if [ $# -eq 0 ]; then
    echo "No test files specified. Running pytest on all tests."
    pytest -v -s --html=report.html --capture=tee-sys --self-contained-html --junitxml=results/test-results.xml
else
    echo "Running tests in files: $@"
    pytest -v -s "$@" --html=report.html --capture=tee-sys --self-contained-html --junitxml=results/test-results.xml
fi
