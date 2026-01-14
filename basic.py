

import subprocess
import shlex
from tempfile import TemporaryFile


def main():
    try:
        subprocess.run(
            shlex.split("python use_subprocess.py 5"),
            check=True,
            timeout=6,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except FileNotFoundError as exc:
        print(f"Process failed. The executable could not be found.\n{exc}")
    except subprocess.CalledProcessError as exc:
        print(
            f"Process failed because it didn't return a sucessful return code."
            f"Returned code {exc.returncode}\n{exc}"
        )
    except subprocess.TimeoutExpired as exc:
        print(f"Process timed out.\n{exc}")


def store_content():
    with TemporaryFile() as tf:
        ls_process = subprocess.run(["python3", "magic_number.py"], stdout=tf)
        tf.seek(0)
        print(tf.read().decode("utf-8"))


def simulate_pipe():
    """simulate ls /usr/bin | grep python"""
    ls_process = subprocess.run(["ls", "/usr/bin"], stdout=subprocess.PIPE)
    grep_process = subprocess.run(
        ["grep", "python"],
        input=ls_process.stdout, 
        stdout=subprocess.PIPE,
    )
    print(grep_process.stdout.decode("utf-8"))


def simulate_pip_using_file():
    with TemporaryFile() as tf:
        ls_process = subprocess.run(["ls", "/usr/bin"], stdout=tf)
        tf.seek(0)
        grep_process = subprocess.run(
            ["grep", "python"], stdin=tf, stdout=subprocess.PIPE,
        )
        print(grep_process.stdout.decode("utf-8"))


if __name__ == "__main__":
    # simulate_pipe()
    simulate_pip_using_file()
    pass

