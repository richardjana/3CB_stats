import json
import secrets
import sys

# utility for managing API keys:
    # GENERATE new key and save to json file
    # REMOVE a key from the json file

if __name__ == '__main__':
    try:
        match sys.argv[1]:
            case 'GENERATE':
                user_name = sys.argv[2]
                with open('api_keys.json', 'r') as file:
                    key_data = json.load(file)

                new_key = secrets.token_urlsafe(16)
                if sys.argv[2] in key_data:
                    key_data[user_name] += [new_key]
                else:
                    key_data[user_name] = [new_key]

                with open('api_keys.json', 'w', encoding='utf-8') as file:
                    json.dump(key_data, file, ensure_ascii=False, indent=4)

            case 'REMOVE':
                user_name = sys.argv[2]
                with open('api_keys.json', 'r') as file:
                    key_data = json.load(file)

                del key_data[user_name]

                with open('api_keys.json', 'w', encoding='utf-8') as file:
                    json.dump(key_data, file, ensure_ascii=False, indent=4)
            #case _:
            #    print('No option chosen.')
    except:
        print('No / invalid option chosen.')
