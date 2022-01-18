# import os, sys
# sys.path.append(os.getcwd())
import datetime

import requests

from src.frontend.view.inv_cli import InvCLI

if __name__ == '__main__':

    try:
        cli = InvCLI()
        while (choice := cli.display_main_menu()) > 0:
            cli.execute_user_command(choice)
        print()
        print("".join(["*"] * 20))
        print("Terminal shut down.")
        print("".join(["*"] * 20))

    except (requests.ConnectionError, requests.Timeout) as ex:
        print("Connection could not be established to server. Terminating program.")
