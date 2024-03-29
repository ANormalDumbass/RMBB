import json

def load_bad_words(file_path):
    with open(file_path, 'r') as file:
        bad_words = [word.strip().lower() for word in file.readlines()]
    return bad_words

def filter_usernames(json_file, bad_words):
    with open(json_file, 'r') as file:
        users = json.load(file)
    
    potentially_inappropriate_users = []
    for user in users:
        username = user.get('username', '').lower()
        found_bad_words = [bad_word for bad_word in bad_words if bad_word in username]
        if found_bad_words:
            user['potentially_inappropriate'] = True
            user['bad_words'] = found_bad_words
            potentially_inappropriate_users.append(user)
        else:
            user['potentially_inappropriate'] = False
    
    return potentially_inappropriate_users

def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

def main():
    json_file = 'group_12199058_members.json'
    bad_words_file = 'BadWords.txt'
    output_file = 'potentially_inappropriate_users.json'

    bad_words = load_bad_words(bad_words_file)
    potentially_inappropriate_users = filter_usernames(json_file, bad_words)

    for user in potentially_inappropriate_users:
        print(f"Username: {user['username']}, Potentially Inappropriate: {user['potentially_inappropriate']}, Bad Words Found: {user['bad_words']}")
    
    save_to_json(potentially_inappropriate_users, output_file)

if __name__ == "__main__":
    main()
