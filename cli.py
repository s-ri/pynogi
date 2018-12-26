#!/usr/bin/env python3
# coding: utf-8

import sys
import click
from faker import Faker
import helpers

fake = Faker()


@click.group()
def cli():
    pass


@cli.command()
@click.option('-e', '--event', type=click.INT, prompt='EVENT CODE', help='Event code for love e.g. love11 > 11')  # noqa
@click.option('-c', '--count', default=1, help='Create account count')
@click.option('--export', is_flag=True, help='export file?')
def generate_password(event, count, export):
    """彼氏イベントの応募ページテスト用のアカウント作る
    :param event: love of event code
    :param count: create account count
    :param export: whether to export file
    """
    click.echo('-' * 30)
    click.echo('USERID\t\tPASSWORD')
    click.echo('-' * 30)

    rv = []
    for item in range(count):
        user_id = fake.ean(length=8)
        password = helpers.generate_password_hash(event, user_id)
        rv.append({'user_id': user_id, 'password': password})
        click.echo(f'{user_id}\t{password}')

    if export:
        header = ['user_id', 'password']
        helpers.export2csv('fake_account', header, rv)


@cli.command()
@click.option('-e', '--event', type=click.INT, prompt='EVENT CODE')
@click.option('-f', '--filter', type=click.STRING)
@click.option('--download', is_flag=True)
def show(event, filter, download):
    """Download csv files for love event winners (only file)"""
    filter = filter or ''
    command = f'find ~/backlog/*love{event}*{filter}.csv'

    rv = helpers.ssh_exec_command(command)

    show_result_from_remote_server(rv)

    if download:
        download_from_remote_server(rv)


@cli.command()
@click.option('-e', '--event', type=click.INT, prompt='EVENT CODE')
@click.option('--download', is_flag=True)
def export(event, download):
    """Export data for love event winners"""
    command = f'./export_csv_for_love_event.sh {event}'

    rv = helpers.ssh_exec_command(command)

    show_result_from_remote_server(rv)

    if download:
        download_from_remote_server(rv)


def show_result_from_remote_server(rv):
    click.echo('-' * 30 + 'RESULT' + '-' * 30)
    for f in rv:
        click.echo(f)
    click.echo('-' * 66 + '\n')


def download_from_remote_server(rv):
    click.secho('Do you really want to download file ([y]/n)? ',
                nl=False,
                fg='red')
    c = click.getchar()
    click.echo()

    if str.upper(c) != 'Y':
        sys.exit()

    helpers.ssh_download_files(rv)


if __name__ == '__main__':
    cli()
