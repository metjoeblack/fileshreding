#!/usr/bin/env python3

import os
import shutil
import subprocess

cwd_path = os.getcwd()  # get the current path!


def shreding_files(content_path_list):
    """
    Python3中常用的执行操作系统命令有os.system()、os.popen()、subprocess.popen()、
    subprocess.call()、subprocess.run()、subprocess.getstatusoutput()六种方法。
    """
    if len(content_path_list) == 0:
        pass
    else:
        prompt_reply = subprocess.run(['zenity',            # an operation prompt waiting for confirmation!
                                       '--question',
                                       '--title=Ramdisk Unmount',
                                       '--timeout=0',
                                       '--text=Do you want to shred these files?',
                                       '--ok-label=Yes',
                                       '--cancel-label=No'
                                       ])
        # please see:https://docs.python.org/3/library/subprocess.html for more!
        if prompt_reply.returncode == 0:
            for item in content_path_list:
                if os.path.isdir(item):
                    shutil.rmtree(item, ignore_errors=False)      # move the dirctory to the Trash
                else:
                    subprocess.run(['shred',                                            # The core program, shred files!
                                    '--force',
                                    '--remove',
                                    '--zero',
                                    '--iterations=10',
                                    str(item)], encoding='utf-8')
            subprocess.run(['zenity',
                            '--info',
                            '--text=The files you choose are shreded!',
                            ])
        else:
            subprocess.run(['zenity',
                            '--info',
                            '--width=400',
                            '--height=200',
                            '--text=The SHRED was cancelled !'
                            ])


def get_content_from_environ():
    """
    (1)os.getenv() does not raise an exception, but returns None
    (2)os.environ.get() similarly returns None
    (3)os.environ[] raises an exception if the environmental variable does not exist
    os.environ.get(), os.getenv(), os.environ[]
    Also can use other approachs:
    (1)
        selected_files = os.environ["NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"]
        selected_files_list = selected_files.split('\n')[:-1]
    (2)
        selected_files = os.getenv("NAUTILUS_SCRIPT_SELECTED_FILE_PATHS")
    """
    environ_variable = "NAUTILUS_SCRIPT_SELECTED_FILE_PATHS"
    selected_content_path = os.environ.get(environ_variable)  # os.environ is a dictionary of the Environment Variables
    return selected_content_path.splitlines(keepends=False)


def main():
    selected_content_path_list = get_content_from_environ()
    shreding_files(selected_content_path_list)


if __name__ == '__main__':
    main()

