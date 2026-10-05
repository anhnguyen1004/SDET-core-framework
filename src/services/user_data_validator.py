import json

def get_raw_user(filename: str):
    try:
        with open(f"data/{filename}", "r") as file:
            users = json.load(file)    
    except FileNotFoundError as e:
        raise Exception(f"File not found. Details: {e}")
    except Exception as e:
        raise Exception(f"Cannot read file. Details: {e}")
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

    except Exception as e:
        raise Exception(f"filter_user has an error. Details: {e}")
    else:
        return filtered_user, invalid_user

def save_users(filename: str, users: list):
    try:
        with open(f"data/{filename}", "w") as file:
            json.dump(users, file, indent=4)
    except FileNotFoundError as e:
        raise Exception(f"File not found. Details: {e}")
    except Exception as e:
        raise Exception(f"Cannot save file. Details: {e}")
    else:
        return True

if __name__ == "__main__":
    try:
        raw_user = get_raw_user("raw_users.json")
        filtered_user, invalid_user = filter_user(raw_user)
        save_users("users.json", filtered_user)
        if invalid_user:
            save_users("invalid_users.json", invalid_user)

    except Exception as e:
        with open(f"data/error_logs.txt", "a") as file:
            file.write(f"An error occurred: {e}\n")