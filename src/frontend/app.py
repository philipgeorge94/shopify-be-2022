from src.frontend.view.inv_cli import InvCLI

if __name__ == 'main':
    app = InvCLI()
    while (choice := app.display_main_menu()) > 0:
        app.execute_user_command(choice)
    print(["X"] * 20)
    print("Terminal shut down.")
    print(["X"] * 20)
# print(uuid4(now))
