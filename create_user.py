#!/usr/bin/env python

import argparse
from subprocess import Popen, PIPE, STDOUT

def bash_cmd(cmd, cwd=None, dry_run=False):
    print cmd
    if dry_run:
        return
    out = ""
    try:
        p = Popen(cmd, stdout=PIPE, stderr=STDOUT, shell=True, cwd=cwd)
        while p.poll() is None:
            t = p.stdout.readline()
            out += t
            print t,
        t = p.stdout.read()
        out += t
        print t,
        p.wait()
    except KeyboardInterrupt:
        p.kill()
        raise
    return out


def main(args):
    bash_cmd("useradd -c \"%s\" -s /bin/bash -m %s"%(args.full_name, args.username))
    bash_cmd("openssl rand -base64 6 | tee -a /home/{0:s}/my_password | passwd --stdin {0:s}".format(args.username))
    bash_cmd("mkdir /home/%s/.ssh"%args.username)
    bash_cmd("chmod 700 /home/%s/.ssh"%args.username)

    with open('/home/%s/.ssh/authorized_keys'%args.username, 'w') as f:
        f.write("%s\n"%args.pub_key)
    
    bash_cmd("chmod 600 /home/%s/.ssh/authorized_keys"%args.username)
    bash_cmd("chown -R {0:s}:{0:s} /home/{0:s}/.ssh".format(args.username))



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Create an user')
    parser.add_argument(
        '--full-name',
        type=str,
    )
    parser.add_argument(
        '--username',
        type=str,
    )
    parser.add_argument(
        '--pub-key',
        type=str,
    )
    args = parser.parse_args()
    assert(args.full_name is not None)
    assert(args.username is not None)
    assert(args.pub_key is not None)

    main(args)
