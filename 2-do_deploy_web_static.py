#!/usr/bin/python3
"""
Script distributes an archive to web servers
"""
from fabric.api import *
import os

env.user = 'ubuntu'
env.hosts = ['100.24.244.104', '3.89.155.116']
env.key_filename = ['~/.ssh/id_rsa']


def do_deploy(archive_path):
    """
    Distribute an archive to web servers and perform deployment steps.

    Args:
        archive_path (str): Path to the archive to be deployed.

    Returns:
        bool: True if all operations were successful, False otherwise.
    """

    if not os.path.exists(archive_path):
        print("Error: {} not found".format(archive_path))
        return False

    try:
        put(archive_path, '/tmp/')

        ar_file = archive_path.split('/')[-1]

        release_folder = '/data/web_static/releases/{}'.format(
                            ar_file.split(".")[0])

        run("mkdir -p {}".format(release_folder))
        run("tar -xzf /tmp/{} -C {}".format(ar_file, release_folder))
        run("rm /tmp/{}".format(ar_file))
        run("mv {}/web_static/* {}".format(release_folder, release_folder))
        run("rm -rf {}/web_static".format(release_folder))
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(release_folder))

        print("New Version deployed!")
        return True
    except Exception as e:
        print("Error while deploying: {}".format(e))
        return False
