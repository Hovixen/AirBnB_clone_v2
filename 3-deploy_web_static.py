#!/usr/bin/python3
"""
Script distributes an archive to web servers
"""
from fabric.api import *
from datetime import datetime
import os

env.user = 'ubuntu'
env.hosts = ['100.24.244.104', '3.89.155.116']


def do_pack():
    """
    Creates a compressed archive from the contents of web_static folder

    Returns:
        str: Archive path if successful, None if otherwise.
    """

    if not os.path.exists("version"):
        local("mkdir -p versions")

    time = datetime.now()
    timestamp = time.strftime("%Y%m%d%H%M%S%")

    ar_file = "web_static_{}.tgz".format(timestamp)

    cmd = 'tar -cvzf versions/{} web_static'.format(ar_file)

    output = local(cmd, capture=True)

    if output.succeeded:
        return 'versions/{}'.format(ar_file)
    else:
        return None


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
    except (Exception, SystemExit) as e:
        print("Error while deploying: {}".format(e))
        return False


def deploy():
    """ DEPLOYS """
    try:
        archive_path = do_pack()
    except Exception:
        return False

    return do_deploy(archive_path)
