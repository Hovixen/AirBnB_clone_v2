#!/usr/bin/python3
"""
Script that generates a .tgz archive from the contents
of the web_static folder
"""
from fabric.api import local
from datetime import datetime
import os


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
