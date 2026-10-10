import json

from src.exceptions.exceptions import DataProcessingError, FileReadError, FileSaveError


def get_raw_user(filename: str):
    try:
        with open(f"data/{filename}", "r") as file:
            users = json.load(file)    
    except FileNotFoundError as e:
        raise FileReadError(f"File not found. Details: {e}")
    except (OSError, json.JSONDecodeError) as e:
        raise FileReadError(f"Cannot read file. Details: {e}")
    else:
        return users

def filter_user(users: list):
    try:
        filtered_user = [] 
        invalid_user= []

        for user in users:
            if user.get('age', 0) >= 18 and '@' in user.get('email', ''):
                filtered_user.append(user)
            else:
                invalid_user.append(user)

    except (TypeError, AttributeError) as e:
        raise DataProcessingError(f"filter_user has an error. Details: {e}")
    else:
        return filtered_user, invalid_user

def save_users(filename: str, users: list):
    try:
        with open(f"data/{filename}", "w") as file:
            json.dump(users, file, indent=4)
    except FileNotFoundError as e:
        raise FileSaveError(f"File not found. Details: {e}")
    except (OSError, TypeError) as e:
        raise FileSaveError(f"Cannot save file. Details: {e}")
    else:
        return True

if __name__ == "__main__":
    try:
        raw_user = get_raw_user("raw_users.json")
        filtered_user, invalid_user = filter_user(raw_user)
        save_users("users.json", filtered_user)
        if invalid_user:
            save_users("invalid_users.json", invalid_user)

    except Exception as e:  # noqa: BLE001
        with open("data/error_logs.txt", "a") as file:
            file.write(f"An error occurred: {e}\n")