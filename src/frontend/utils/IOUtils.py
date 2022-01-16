def get_yn(prompt):
    response = input(prompt).lower()
    if response == 'yes' or response == 'y':
        return True
    else:
        return False