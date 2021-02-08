__author__ = 'richard'
from fabric.api import *
from fabric.colors import green

env.user = 'root'
env.host_string = '209.97.136.148'
env.password = '010518"#@**RED'
env.key_filename = "/Users/richardcancino/Desktop/privatekey.pem"
home_path = "/home/ubuntu"
settings_staging = "--settings='corebackend.settings.staging'"
activate_env_staging = "source {}/envs/abbottenv/bin/activate".format(
    home_path)
manage = "python manage.py"


def deploy_staging():
    print("Beginning Deploy:")
    with cd("{}/account-backend".format(home_path)):
        run("git pull")
        # run("{} && pip install -r requirements.txt".format(activate_env_staging))
        run("{} && {} collectstatic --noinput {}".format(activate_env_staging,
                                                         manage,
                                                         settings_staging))
        run("{} && {} migrate {}".format(activate_env_staging, manage,
                                         settings_staging))
        sudo("service nginx restart", pty=False)
        sudo("supervisorctl restart gunicorn_abbott-backend ", pty=False)

    print(green("Deploy tuki successful"))


def createsuperuser_staging():
    with cd("{}/account-backend".format(home_path)):
        run("{} && {} createsuperuser {}".format(activate_env_staging, manage,
                                                 settings_staging))
    print(green("Createsuperuser successful"))
