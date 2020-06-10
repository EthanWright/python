import subprocess


def call_ffmpeg(command):
    p = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
    result, stdout = p.communicate()

    stdout = stdout.decode('utf-8', 'replace')
    if p.returncode != 0:
        raise Exception(stdout.strip().split('\n')[-1])

    return result.decode('utf-8', 'replace'), stdout


def get_metadata(file_name):
    return call_ffmpeg(f'ffmpeg -i "{file_name}" -f ffmetadata -')
