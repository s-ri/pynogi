# pynogi
Tools

## Development Environment
---------------
At the bare minimum you'll need the following for your development environment
- [Python](http://www.python.org/)

It is strongly recommended to also install and use the following tools:
- [Pipenv](https://github.com/pypa/pipenv)

### Local Setup

#### 1. Install pipenv
    $ brew install pipenv
    
#### 2. Clone the project
    $ git clone git@github.com:s-ri/pynogi.git pynogi
    cd pynogi
    chmod a+x cli.py

#### 3. Create and initialize virtualenv for the project
    $ pipenv sync --dev

#### 4. Run the development env
Change virtualenv

    $ pipenv shell

Exit virtualenv

    $ exit

#### 5. Setting config.yml

    ssh_config:
        hostname: your remote server host
        username: your remote server username
        key_filename: your remote ssh-key file

    download: your download path



#### 6. Execute commands
Commands

    $ ./cli.py --help
    Usage: cli.py [OPTIONS] COMMAND [ARGS]...

    Options:
        --help  Show this message and exit.

    Commands:
    export             Export data for love event winners
    generate-password  彼氏イベントの応募ページテスト用のアカウント作る :param event: love of event...
    show               Download csv files for love event winners (only file)

generate-password (Create account & password <- fake )

    $ ./cli.py generate-password --help

        Usage: cli.py generate-password [OPTIONS]

        彼氏イベントの応募ページテスト用のアカウント作る :param event: love of event code :param count:
        create account count :param export: whether to export file

        Options:
        -e, --event INTEGER  Event code for love e.g. love11 > 11
        -c, --count INTEGER  Create account count
        --export             export file?
        --help               Show this message and exit.


    e.g.
    $ ./cli.py generate-password -c 10 --export

export (Export database data)

    $ ./cli.py export --help

        Usage: cli.py export [OPTIONS]

        Export data for love event winners

        Options:
        -e, --event INTEGER
        --download
        --help               Show this message and exit.

    e.g.
    $ ./cli.py export -e 12 --download

show (show backup files and download)

    $ ./cli.py show --help
    
        Usage: cli.py show [OPTIONS]

        Download csv files for love event winners (only file)

        Options:
        -e, --event INTEGER
        -f, --filter TEXT
        --download
        --help               Show this message and exit.

    e.g. Only read
    $ ./cli.py show -e 13 

    e.g. Download option
    $ ./cli.py show -e 13 --download

    e.g. Filtering option
    $ ./cli.py show -e 13 -f 20181225 --download
