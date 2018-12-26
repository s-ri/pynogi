# coding: utf-8


import os
import sys
from datetime import datetime
from contextlib import contextmanager
import hashlib
import csv
import click
import paramiko
import yaml

ROOT = os.path.dirname(__file__)


def loads():
    config = os.path.join(ROOT, 'config.yml')

    with open(config) as f:
        parser = yaml.load(f)
    return parser


SSH_CONFIG = loads().get('ssh_config')
DOWNLOAD_DIR = loads().get('download')


def generate_password_hash(event=None, user_id=None):
    """Genrate website(nogikoi) password hash.
    :param event: love event code e.g. love11 -> 11
    :param user_id: website account id
    """

    suffix_key = f'password{event}'
    hexkey = str.encode(f'{user_id}{suffix_key}')

    # md5 value[1:10] + 1
    passwd = '{0}{1}'.format(hashlib.md5(hexkey).hexdigest()[1:10], 1)

    return passwd


def export2csv(filename, headers, data):
    """Export to csv file
    :param filename: filename (absolute path)
    :param headers: header
    :param data: content
    """
    click.secho('Do you really want to export file ([y]/n)? ',
                nl=False,
                fg='red')

    c = click.getchar()
    click.echo()

    if str.upper(c) != 'Y':
        sys.exit()

    today = datetime.now().strftime("%y%m%d%H%M%S")
    filename = f'{DOWNLOAD_DIR}/{filename}_{today}.csv'

    click.echo(filename)

    with open(filename, 'w', newline='') as csvfile:
        write = csv.DictWriter(csvfile, fieldnames=headers)
        write.writeheader()

        with click.progressbar(data, label='exporing {}'.format(filename)) as items:  # noqa
            for item in items:
                write.writerow(item)


@contextmanager
def _ssh_connect():
    """Using SSH connect remote server"""
    client = paramiko.SSHClient()
    client.load_system_host_keys()
    client.set_missing_host_key_policy(paramiko.WarningPolicy)

    client.connect(**SSH_CONFIG)
    yield client

    client.close()


def _ssh_error_report(stderr, echo_error_report=True):
    """Execute remote server command and error report."""
    rv = False
    for e in stderr:
        if echo_error_report:
            print(e)
        rv = True

    return rv


def ssh_exec_command(command):
    """Execute remote server (linux) command"""
    with _ssh_connect() as ssh:
        stdin, stdout, stderr = ssh.exec_command(command)

        if _ssh_error_report(stderr):
            sys.exit()

        rv = []
        for line in stdout.read().splitlines():
            rv.append(line.decode())

        return rv


def ssh_download_files(data):
    """Connect SFTP and download file"""
    with _ssh_connect() as ssh:
        with ssh.open_sftp() as sftp:
            with click.progressbar(data, label='downloads') as items:  # noqa
                for item in items:
                    _, filename = os.path.split(item)
                    sftp.get(item, f'{DOWNLOAD_DIR}/{filename}')
