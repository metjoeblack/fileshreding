
import subprocess
from argparse import ArgumentParser
import time
import shlex


def get_options():
    parser = ArgumentParser(
        prog="Using Subprocess Modlue",
        description="This is a description.",
        allow_abbrev=True,
        epilog="Thanks for using."
    )
    parser.add_argument("times", type=int)
    return parser.parse_args()


def main():
    args = get_options()
    print(f"Starting timer of {args.times} seconds.")
    for _ in range(args.times):
        print(".", end="", flush=True)
        time.sleep(1)
    print("\nAll done!")


if __name__ == "__main__":
    main()
    pass
