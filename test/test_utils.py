import boto3
from src.utils import *
from unittest.mock import Mock, patch
from src.password_manager import password_manager
import pytest
from botocore.exceptions import ClientError
import io

#sm = boto3.client('secretsmanager')
mock_response = {'SecretList': []}


@patch.object(sm, 'list_secrets', return_value=mock_response)
def test_list_secrets_prints_zero_when_no_secrets(*args):
    with patch('builtins.print') as mock_print:
        sm.list_secrets.return_value = mock_response
        list_secrets()
        assert mock_print.call_args.args[0] == '0 secret(s) available\n'


@patch.object(sm, 'list_secrets', return_value=mock_response)
def test_list_secrets_prints_list_of_secrets_names(*args):
    mock_response = {'SecretList': [{"Name": "s1"}, {'Name': 's2'}]}
    with patch('builtins.print') as mock_print:
        sm.list_secrets.return_value = mock_response
        list_secrets()
        assert mock_print.call_args.args[0] == '2 secret(s) available\ns1\ns2\n'


@patch.object(sm, 'create_secret', return_value={})
def test_enter_secret_calls_create_secret_with_correct_identifier(*args):
    with patch('builtins.input') as mock_id:
        mock_id.return_value = 'TestSecret'
        enter_secret()
        assert sm.create_secret.call_args.kwargs['Name'] == 'TestSecret'


@patch.object(sm, 'create_secret', return_value={})
def test_enter_secret_calls_create_secret_with_correct_secret_string(*args):
    mock_id = Mock(return_value='TestSecret')
    mock_user = Mock(return_value='TestUser')
    mock_paswd = Mock(return_value='PSWD')
    mock_inputs = Mock()
    mock_inputs.side_effect = [mock_id.return_value,
                               mock_user.return_value, mock_paswd.return_value]
    with patch('builtins.input', mock_inputs):
        print(enter_secret())
        assert sm.create_secret.call_args.kwargs['SecretString'] == "UserId:TestUser,Password:PSWD"


@patch('builtins.input', return_value='zzz')
def test_retrieve_secret_handles_invalid_secret_names(*args):
    with patch('builtins.print') as mock_print:
        retrieve_secret()
        assert mock_print.call_args.args[0] == 'The requested secret was not found'


@patch('builtins.input', return_value='test_secret')
def test_retrieve_secret_passes_correct_secret_name_to_api(*args):
    with patch.object(sm, 'get_secret_value') as mock_retrieval:
        retrieve_secret()
        assert mock_retrieval.call_args.kwargs['SecretId'] == 'test_secret'


@patch('builtins.input', return_value='test_secret')
def test_retrieve_secret_creates_and_writes_in_txt_file(*args):
    mock_response = {"SecretString": "UserId:Yuri,Password:hellojoe"}
    with patch.object(sm, 'get_secret_value') as mock_retrieval:
        mock_retrieval.return_value = mock_response
        retrieve_secret()
        with io.open('secret.txt', 'r') as file:
            assert mock_response['SecretString'] in file.read()

@patch('builtins.input', return_value='test_secret')
def test_delete_secret_deletes_correct_secret(*args):
    with patch.object(sm, 'delete_secret') as mock_delete:
        with patch('builtins.print') as mock_print:
            delete_secret()
            assert mock_delete.call_args.kwargs['SecretId'] == 'test_secret'
            assert mock_print.call_args.args[0] == 'test_secret deleted'

@patch('builtins.input', return_value='zzz')
def test_delete_secret_handles_invalid_secret_names(*args):
    with patch('builtins.print') as mock_print:
        delete_secret()
        assert mock_print.call_args.args[0] == 'The requested secret was not found'