"""
Execute ffmpeg CLI commands via subprocess calls

Ethan Wright - 6/11/20
"""
import subprocess


def print_message(severity, verbose_level, message):
    if verbose_level >= severity:
        print(message)


def call_ffmpeg(command, verbose=0, commit=False):
    print_message(1, verbose, 'Running ffmpeg CLI command:\n' + str(command))
    if not commit:
        print_message(0, verbose, f'~~~ NOT Committing Changes ~~~')
        return None, None
    result, stdout = execute_ffmpeg_cli_command(command)
    print_message(2, verbose, result)
    print_message(2, verbose, stdout)
    print_message(1, verbose, '--- Done!\n')
    return result, stdout


def execute_ffmpeg_cli_command(command):
    # import pdb;pdb.set_trace()
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    result, stdout = p.communicate()

    stdout = stdout.decode('utf-8', 'replace')
    if p.returncode != 0:
        print(stdout)
        raise Exception(stdout.strip().split('\n')[-1])

    return result.decode('utf-8', 'replace'), stdout


def get_metadata(file_name, verbose=0):
    command = ['ffmpeg', '-i', file_name, '-f', 'ffmetadata', '-']
    # windows_command = ' '.join(command)
    return call_ffmpeg(command, verbose=verbose, commit=True)
