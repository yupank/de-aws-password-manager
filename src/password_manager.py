import src.utils as utils
import boto3


def password_manager():

    function_caller = input(
        'Please specify [e]ntry, [r]etrieval, [d]eletion, [l]isting or e[x]it:')
    if function_caller == 'x':
        print('Thank you. Goodbye.')
        return None
    elif function_caller == 'l':
        utils.list_secrets()
    elif function_caller == 'd':
        utils.delete_secret()
    elif function_caller == 'e':
        utils.enter_secret()
    elif function_caller == 'r':
        utils.retrieve_secret()
    else:
       print('invalid command')

    if __name__ == '__main__':
        password_manager()


if __name__ == '__main__':
    password_manager()
