# import os, sys
# sys.path.append(os.getcwd())
import datetime

import requests

from src.frontend.view.inv_cli import InvCLI

if __name__ == '__main__':
    cli = InvCLI()
    try:
        cli.checkConnection()
        while (choice := cli.display_main_menu()) > 0:
            cli.execute_user_command(choice)
        print(["X"] * 20)
        print("Terminal shut down.")
        print(["X"] * 20)

    except (requests.ConnectionError, requests.Timeout) as ex:
        print("Connection could not be established to server. Terminating program.")


# print(uuid4(now))
