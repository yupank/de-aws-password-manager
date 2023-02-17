import boto3
from botocore.response import StreamingBody
from botocore.exceptions import ClientError
import io

#session = boto3.session.Session()
sm = boto3.client('secretsmanager')


def list_secrets():
    """ prints length of current secret list
        list names of all secrets """
    out_str = ''
    secrets_list = sm.list_secrets()['SecretList']
    out_str += f'{len(secrets_list)} secret(s) available\n'
    for secret in secrets_list:
        out_str += f'{secret["Name"]}\n'
    print(out_str)


def enter_secret():
    """ Inputs: secret identifier, used ID and password 
        uses AWS Secret Manager and boto3 to save input as secret"""
    sec_id = input('Secret identifier:')
    user_id = input('UserId:')
    passwd = input('Password:')
    secret_str = f'UserId:{user_id},Password:{passwd}'
    try:
        sm.create_secret(Name=sec_id, SecretString=secret_str)
        print('Secret saved')
    except ClientError as e:
        raise e


def retrieve_secret():
    sec_id = input('Specify secret to retrieve:')
    try:
        secret = sm.get_secret_value(SecretId=sec_id)
        to_input = secret['SecretString']
        with io.open('secret.txt', 'a') as file:
            file.write(f'{to_input}')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret was not found")
        else :
            print("The server error")


def delete_secret():
    sec_id = input('Specify secret to delete:')
    try:
        sm.delete_secret(SecretId=sec_id)
        print(f'{sec_id} deleted')
    except ClientError as e:
        if e.response['Error']['Code'] == 'ResourceNotFoundException':
            print("The requested secret was not found")
        else :
            print("The server error")
