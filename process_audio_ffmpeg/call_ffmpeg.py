"""
Execute ffmpeg CLI commands via subprocess calls

Ethan Wright - 6/11/20
"""
import subprocess


def call_ffmpeg(command, verbose=0, commit=False):
    print('Running ffmpeg CLI command:\n' + command)
    if not commit:
        print(f'~~~ NOT Committing Changes ~~~')
        return None, None
    result, stdout = execute_ffmpeg_cli_command(command)
    if verbose:
        print(result)
        print(stdout)
    print('--- Done!\n')
    return result, stdout


def execute_ffmpeg_cli_command(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    result, stdout = p.communicate()

    stdout = stdout.decode('utf-8', 'replace')
    if p.returncode != 0:
        print(stdout)
        raise Exception(stdout.strip().split('\n')[-1])

    return result.decode('utf-8', 'replace'), stdout


def get_metadata(file_name, verbose=0, commit=False):
    command = f'ffmpeg -i "{file_name}" -f ffmetadata -'
    return call_ffmpeg(command, verbose=verbose, commit=commit)
