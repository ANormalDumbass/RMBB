import json
import requests

def extract_all_members(group_id):
    url = f"https://groups.roblox.com/v1/groups/{group_id}/users?sortOrder=Asc&limit=100"
    all_members = []

    while url:
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors

            member_data = response.json()
            members_info = []

            # Extract user ID, username, and display name
            for member in member_data['data']:
                user_id = member['user']['userId']
                username = member['user']['username']
                display_name = member['user']['displayName']

                member_info = {
                    'userId': user_id,
                    'username': username,
                    'displayName': display_name
                }

                members_info.append(member_info)

            all_members.extend(members_info)

            # Save member info to file after every successful request
            save_member_info_to_file(members_info, f"group_{group_id}_members_partial.json")

            # Get the next page cursor
            next_page_cursor = member_data.get('nextPageCursor')
            if next_page_cursor:
                url = f"https://groups.roblox.com/v1/groups/{group_id}/users?sortOrder=Asc&limit=100&cursor={next_page_cursor}"
            else:
                url = None

        except requests.exceptions.RequestException as e:
            print("Error fetching member information:", e)
            return None

    return all_members

def save_member_info_to_file(members_info, filename):
    with open(filename, 'a', encoding='utf-8') as file:  # Append mode to avoid overwriting
        json.dump(members_info, file, indent=4)  # Save members_info in JSON format
        file.write('\n')  # Add a newline for readability between each request's data

if __name__ == "__main__":
    group_id = input("Enter the Roblox group ID: ")
    members_info = extract_all_members(group_id)

    if members_info:
        print("Member Information:")
        for member_info in members_info:
            print(f"User ID: {member_info['userId']}")
            print(f"Username: {member_info['username']}")
            print(f"Display Name: {member_info['displayName']}")
            print()  # Print an empty line for readability

        filename = f"group_{group_id}_members.json"  # Change file extension to .json
        save_member_info_to_file(members_info, filename)
        print(f"Member information saved to {filename}")
