from unittest.mock import Mock, patch
from src.password_manager import password_manager
import src.utils as utils


def test_handler_function_sends_correct_initial_message():
    with patch('builtins.input') as mock_input:
        mock_input.return_value = 'l'
        password_manager()
        assert mock_input.call_args.args[0] == 'Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:'


@patch('builtins.input', return_value='l')
def test_calls_list_function(*args):
    with patch('src.utils.list_secrets') as mock_list:
        mock_list.return_value = '0 secret(s) available'
        password_manager()
        mock_list.assert_called_once()


@patch('builtins.input', return_value='d')
def test_calls_delete_function(*args):
    with patch('src.utils.delete_secret') as mock_delete:
        password_manager()
        mock_delete.assert_called_once()


@patch('builtins.input', return_value='e')
def test_calls_entry_function(*args):
    with patch('src.utils.enter_secret') as mock_entry:
        password_manager()
        mock_entry.assert_called_once()


@patch('builtins.input', return_value='r')
def test_calls_retrieval_function(*args):
    with patch('src.utils.retrieve_secret') as mock_retrieval:
        password_manager()
        mock_retrieval.assert_called_once()

@patch('builtins.input', return_value='x')
def test_prints_goobye_message_on_exit(*args):
    with patch('builtins.print') as mock_print:
        password_manager()
        assert mock_print.call_args.args[0] == 'Thank you. Goodbye.'

@patch('builtins.input', return_value='z')
def test_calls_error_handler_on_invalid_input(*args):
    with patch('src.utils.error_handler') as mock_err_handler:
        password_manager()
        mock_err_handler.assert_called_once

