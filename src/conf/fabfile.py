from __future__ import with_statement

from fabric.api import *
from fabric.operations import local

# TODO: docstrings and require directives

# Global

env.project_name = 'nrishirts'

# Locals

def localhost():
    env.hosts = ['localhost']
    env.path = '/var/www/%(project_name)s' % env
    env.user = 'marco'
    env.release_type = 'local'

def prod():
    env.hosts = ['www']
    # env.path = '/var/www/%(project_name)s' % env
    # env.user = 'mymodernlife'
    env.release_type = 'prod'

# Tasks

def dotcloud_deploy():
    server = '%s.%s' % (env.project_name, env.host)
    # Assumes this fabfile is in src/conf/ :
    local('../manage.py generatemedia')
    local('ln -s static/nginx.conf ../_generated_media/')
    local('mkdir ../_generated_media/taggit_autocomplete_modified')
    local('cp ../static/lib/taggit_autocomplete_modified/* ../_generated_media/taggit_autocomplete_modified/')
    #local('dotcloud push %s.static ../_generated_media/' % env.project_name)
    #local('dotcloud run %s.static sudo /etc/init.d/nginx restart' % env.project_name)
    local('dotcloud push -b develop %s ../..' % env.project_name)
    local('dotcloud run %s -- python current/src/manage.py syncdb --settings=src.conf.prod.settings' % server)
    local('dotcloud run %s -- python current/src/manage.py migrate --settings=src.conf.prod.settings' % server)
    local('dotcloud run %s sudo /etc/init.d/nginx restart' % server)

def test():
    local('cd ..; python manage.py test', fail='abort')

def setup(server_type='full'):
    if server_type == 'full':
        setup_web()
        setup_db()
    elif server_type == 'web':
        setup_web()
    elif server_type == 'db':
        setup_db()

    # TODO: sync time on the server

    setup_new_project()

@runs_once
def server_update():
    sudo('apt-get update')

@runs_once
def setup_general():
    server_update()

    # Remove the crap that comes pre-installed
    sudo('apt-get remove -y apache2 apache2-mpm-prefork apache2-utils')

    # Python & pip
    sudo('apt-get install -y build-essential python-dev python-setuptools')
    sudo('easy_install -U pip')

    # Process Management with supervisord
    sudo('pip install supervisor')
    sudo('echo; if [ ! -f /etc/supervisord.conf ]; then echo_supervisord_conf > /etc/supervisord.conf; fi', pty=True)
    sudo('echo; if [ ! -d /etc/supervisor ]; then mkdir /etc/supervisor; fi', pty=True)

def setup_web():
    setup_general()

    # Webserver
    sudo('apt-get install nginx')

    # TODO: chef/puppet should handle the main nginx confs, how to ensure it's occured?

    sudo('/etc/init.d/nginx start')

    # virtualenvs
    sudo('pip install virtualenv')
    sudo('pip install virtualenvwrapper')
    sudo('mkdir -p /var/www/.virtualenvs')

    if not exists('~/.bashrc'):
        run('touch ~/.bashrc')

    run('echo "export WORKON_HOME=/var/www/.virtualenvs" >> ~/.bashrc')
    run('. ~/.bashrc')
    sudo('mkvirtualenv --no-site-packages %(project_name)s' % env)

def setup_db():
    setup_general()

    # Database
    sudo('apt-get install -y postgresql libpq-dev')

    # TODO: setup database

def setup_new_project():
    # TODO: create user, group, add user to group, switch to user, copy over
    # ssh key, re-login to server as user, disable root login, change
    # permissions on project directories

    sudo('mkdir -p %s' % env.path)

    if not exists('%(path)s/releases' % env):
        sudo('cd %(path)s; mkdir releases' % env)

    if not exists('%(path)s/logs' % env):
        sudo('cd %(path)s; mkdir logs' % env)

def deploy():
    import time
    env.release = time.strftime('%Y%m%d%H%M%S')

    upload_site()
    install_reqs()
    install_site()
    symlink_release()
    migrate_db()
    reload_webserver()

def deploy_version(version):
    pass

def rollback():
    # TODO: this won't work, because you can't do os operations on a remote server

    import os

    # current is assumed to be a symlink to a directory that's just a number
    # representing the datetime of release in the same folder
    current = os.readlink('%(path)s/releases/current' % env)
    (__, current) = os.path.split(current)
    current = int(current)

    releases_dir = '%(path)s/releases' % env
    names = os.listdir(releases_dir)
    releases = []
    for name in names:
        if not os.path.isdir(os.path.join(releases_dir, name)):
            continue
        if os.path.islink(os.path.join(releases_dir, name)):
            continue
        if str(int(name)) != name:
            continue

        releases.append(int(name))

    releases.sort(reverse=True)

    cur_pos = None
    for i, v in enumerate(releases):
        if v == current:
            cur_pos = i
            break

    cur_pos += 1
    if cur_pos > releases.length:
        abort()

    prev_release = str(releases[cur_pos])

    sudo('cd %s; ln -s %s current' % (releases_dir, prev_release))

    reload_webserver()

def upload_site():
    local('git archive --format=tar master | gzip > %(release)s.tar.gz' % env)
    sudo('mkdir -p %(path)s/releases/%(release)s' % env)
    put('%(release)s.tar.gz' % env, '%(path)s/releases' % env)
    run('cd %(path)s/releases/%(release)s && tar zxf ../%(release)s.tar.gz && rm ../%(release)s.tar.gz' % env)
    local('rm %(release)s.tar.gz' % env)

def install_reqs():
    run('workon %(project_name)s' % env)
    sudo('pip install -r %(path)s/src/conf/common/requirements.txt' % env)
    run('deactivate')

def install_site():
    server_conf = '%(path)s/src/conf/%(release_type)s/nginx.conf' % env

    if not exists(server_conf):
        server_conf = '%(path)s/src/conf/common/nginx.conf' % env

    sudo('ln -s %s /etc/nginx/sites-available/%(project_name)s' % (server_conf, env))
    sudo('ln -s /etc/nginx/sites-available/%(project_name)s /etc/nginx/sites-enabled/%(project_name)s' % env)

def symlink_release():
    # TODO: rotate out old directories
    sudo('cd %(path)s/releases; ln -s %(release)s current' % env)

def migrate_db():
    pass

def reload_webserver():
    sudo('/etc/init.d/nginx reload')

def restart_webserver():
    sudo('/etc/init.d/nginx restart')

# Ripped from simonw's slides
def git_export():
    env.deploy_date = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    env.export_path = '/tmp/export/%s' % (env.deploy_date)
    local('mkdir -p %(export_path)s' % env)
    local(
        'cd .. && git archive --prefix=sitename/ --format=tar ' +
        'master | tar -x -C %(export_path)s' % env
    )

"""
servers.json

{
    "servers": {
        "name": {
            "ip": 192.168.1.1
        }
    },
    "roles": {
        "app": ["name"],
        "db": [],
        "solr": [],
        "redis": [],
        "static": []
    }
}

fabfile.py

_js = json.load(open('servers.json'))
servers = _js.servers
roles = _js.roles

def server(name):
    env.hosts = env.hosts or []
    env.hosts.append('username@%s' % servers[name][ip])

def role(name):
    for server_name in roles[name]:
        server(name)

$ fab role:redis clear_cache
"""
