import boto3
import json
import os
import argparse
import configparser


#Add credentials to the credentials file
def add_credentials(credentials, profile):
    config = configparser.ConfigParser()
    homepath = os.path.expanduser('~')
    credentials_path = homepath + '/.aws/credentials'
    if not os.path.isfile(credentials_path):
        print("No credentials file found. It will be created")
        c = open(credentials_path,"w")
        c.close()
    config.read(credentials_path)
    config[profile] = {
        'aws_acces_key_id': credentials["accessKeyId"],
        'aws_secret_access_key': credentials["secretAccessKey"],
        'aws_session_token': credentials["sessionToken"]
    }

    with open(credentials_path, 'w') as configfile:
        config.write(configfile)
  
#Gets profile data from .aws/config
def get_profile_from_config(profile):
    homepath = os.path.expanduser('~')
    config_path = homepath + '/.aws/config'
    config = configparser.ConfigParser()
    config.read(config_path)
    profile_section = config["profile {}".format(profile)]
    if not profile_section:
        print("Profile {} doesn't exit in config file".format(profile))
        exit()
    return profile_section

        

#Gets commandline arguments for this script
def get_arguments():
    parser = argparse.ArgumentParser('Configure sso credentials for cdk')
    parser.add_argument('--profile', help="The profile in your .aws/config file you want to get credentials for")
    args = parser.parse_args()
    if not args.profile:
        parser.print_help()
        exit()
    return args.profile

# Gets access token from the SSO cache directory
def get_access_token():
    homepath = os.path.expanduser('~')
    cache_path = homepath + '/.aws/sso/cache/'
    files = os.listdir(cache_path)
    if not files:
        print("No files in SSO cache. Please log in first")
        exit()
    for file in files:
        if file.endswith(".json"):
            rawfile = open(cache_path + file, "r")
            jsondict = json.load(rawfile)
            print(jsondict)
            if "accessToken" in jsondict:
                print("AccessToken found")
                return jsondict["accessToken"]

def main():
    profile = get_arguments()
    config = get_profile_from_config(profile)
    accessToken = get_access_token()
    if not accessToken:
        print("No accesstoken found. configure sso and login first")
        exit()
    client = boto3.client("sso")
    response = client.get_role_credentials(
        roleName=config['sso_role_name'],
        accountId=config['sso_account_id'],
        accessToken=accessToken
    )
    print(response["roleCredentials"]["accessKeyId"])
    add_credentials(response["roleCredentials"], profile)

if __name__ ==  "__main__":
    main()