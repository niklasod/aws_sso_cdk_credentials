# aws_sso_cdk_credentials
Small python script to enable using cdk with aws sso credentials

## Introduction
Since cdk currently doesn't support sso credentials it's necessary to get the credentials manually and add the to the credentials file. This scripts automates the process.
It gets the temporary credentials via a boto3 call and uses the sessionToken in the sso cache folder. When the session expires or when you login in again, you have to run this script again.

## Preconditions
* You are logged in via sso
* Your config and credentials files are in the default location ([home]/.aws/credentials, [home]/.aws/config)
* Your sso cache folder is in the default location ([home]/.aws/sso/cache/)

## Usage
* Backup your existing credentials file. This script appends to the exiting file and shouldn't mess anything up. But better safe than sorry
* Install requirements by running pip install -r requirements.txt
* Run the script: python configure-credentials.py --profile [your sso profile name]. Profile must exist in the current config file. 
