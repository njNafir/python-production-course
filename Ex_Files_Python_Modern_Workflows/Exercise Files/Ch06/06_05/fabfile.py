"""Fabric file for deploying our application"""

from os import walk
from os.path import basename
from shutil import make_archive, rmtree

from fabric import task

from elmer import __version__


def clean_pyc():
    for root, dirs, _ in walk('elmer'):
        for dir_name in dirs:
            if dir_name == '__pycache__':
                rmtree(f'{root}/{dir_name}')


def create_dist():
    clean_pyc()
    base_name = f'/tmp/elmer-{__version__}'
    return make_archive(base_name, 'bztar', 'elmer')


@task
def deploy(c):
    app_dir = f'/elmer/elmer-{__version__}'
    c.run(f'mkdir -p {app_dir}')
    venv = f'{app_dir}/venv'
    c.run(f'/usr/local/bin/virtualenv {venv}')
    py = f'{venv}/bin/python'
    c.put('requirements.txt', app_dir)
    c.run(f'{py} -m pip install -r {app_dir}/requirements.txt')
    dist_file = create_dist()
    c.put(dist_file, app_dir)
    src_dir = f'{app_dir}/elmer'
    c.run(f'mkdir -p {src_dir}')
    c.run(f'tar -C {src_dir} -xjf {app_dir}/{basename(dist_file)}')
    with c.cd(app_dir):
        c.run(f'{venv}/bin/gunicorn -w 8 -b 0.0.0.0:8080 -D elmer.httpd:app')
