import argparse
from pycronserver.local import get_local_pycronserver


def command_line_parser():
    """
    Main function primarly used for the command line interface
    """
    parser = argparse.ArgumentParser(prog="pycronserver")
    parser.add_argument(
        "crontab",
        help="Crontab timestamp",
    )
    pcs = get_local_pycronserver()
    pcs.execute_tasks(parser.crontab)


if __name__ == "__main__":
    command_line_parser()
