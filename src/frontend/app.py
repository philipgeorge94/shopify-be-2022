# import os, sys
# sys.path.append(os.getcwd())
import datetime
import argparse

import requests

from src.frontend.view.inv_cli import InvCLI
parser = argparse.ArgumentParser(description="Run Command Line Interface for inventory management")
parser.add_argument('-i', '--port', type=int, metavar='', default=8000,
                    help="Specify port on which server is running. Default is 8000")
args = parser.parse_args()
if __name__ == '__main__':

    try:
        cli = InvCLI(args.port)
        while (choice := cli.display_main_menu()) > 0:
            cli.execute_user_command(choice)
        print()
        print("".join(["*"] * 20))
        print("Terminal shut down.")
        print("".join(["*"] * 20))

    except (requests.ConnectionError, requests.Timeout) as ex:
        print("Connection could not be established to server. Terminating program.")
