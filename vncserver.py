#! python
import os
import pwd
import subprocess
import sys

#python test2.py ur.local /home/ur.local vncserver
def main(my_args=None):
    if my_args is None: my_args = sys.argv[1:]
    user_name, cwd = my_args[:2]
    args = my_args[2:]
    pw_record = pwd.getpwnam(user_name)
    user_name      = pw_record.pw_name
    user_home_dir  = pw_record.pw_dir
    user_uid       = pw_record.pw_uid
    user_gid       = pw_record.pw_gid
    env = os.environ.copy()
    env[ 'HOME'     ]  = user_home_dir
    env[ 'LOGNAME'  ]  = user_name
    env[ 'PWD'      ]  = cwd
    env[ 'USER'     ]  = user_name
    report_ids('starting ' + str(args))
    process = subprocess.Popen(
        args, preexec_fn=demote(user_uid, user_gid), cwd=cwd, env=env, 
		stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    process.stdin.write('password\n')
    process.stdin.write('password')
    process.stdin.flush()
    stdout,stderr = process.communicate()  
    print stdout  
    print stderr
    result = process.wait()
    report_ids('finished ' + str(args))
    print 'result', result


def demote(user_uid, user_gid):
    def result():
        report_ids('starting demotion')
        os.setgid(user_gid)
        os.setuid(user_uid)
        report_ids('finished demotion')
    return result


def report_ids(msg):
    print 'uid, gid = %d, %d; %s' % (os.getuid(), os.getgid(), msg)


if __name__ == '__main__':
    main()