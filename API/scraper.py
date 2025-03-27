from bs4 import BeautifulSoup
import json
import numpy as np
import os
import pandas as pd
import re
import requests
import sys

def find_rounds_in_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    pages = {}
    for tr in soup.find_all('tr'):
        try:
            link = tr.find('a', class_='topic_title')['href']
            if ('neuauflage' in link.split('-')) or ('forenliga' in link.split('-')):
                pages[int(link[:-1].split('runde-')[-1].split('-')[0])] = link
        except:
            pass

    return pages

def fix_player_name_typos(df):
    # typos with player names:
    typo_dict = {'BlackHole: Black Lotus, Black Lotus, Pristine Angel': 'BlackHole',
                 'bongoking': 'Bongoking',
                 'GoDji8': 'GoDJi8',
                 'Haakon': 'Haakon, Geißel der anderen',
                 'Master_of_Desastser': 'Master_of_Desaster',
                 'P0LTLERGEIST': 'P0LTERGEIST',
                 'TheBeast': 'The Beast',
                 'the green one': 'The green one',
                 'Lollonator': 'lollonator',
                 'Hoempes': 'hoempes'}

    for name_typo, name_correct in typo_dict.items():
        df.replace(name_typo, name_correct, inplace=True)

    return df

def check_results(res):
    # should be square
    if res.shape[0] != res.shape[1]:
        return False

    # check if results table is consistent; possible results: 6-0, 4-1, 3-3, ...
    valid_results = {('00', '06'), ('06', '00'),
                     ('01', '04'), ('04', '01'),
                     ('02', '02'), ('03', '03')}

    #I, J = np.triu_indices(res.shape[0], k=1)
    #is_valid = [(res[i, j], res[j, i]) in valid_results for i, j in zip(I, J)]

    is_valid = True
    for i in range(res.shape[0]):
        for j in range(i+1, res.shape[1]):
            if (res[i,j], res[j,i]) not in valid_results:
                print(f"{i+1} {j+1}: {res[i,j]}-{res[j,i]}")
                is_valid = False

    return is_valid # np.all(is_valid)

def check_card_name(cardName):
    # check if the given card name exists, otherwise flag a problem
    # try to get a response from scryfall API
    response = requests.get(f"https://api.scryfall.com/cards/named?exact={cardName}")
    response_dict = json.loads(response.text)

    if response_dict['object'] == 'card': # found something
        # some card names with typos still find the card, so return the correct card name
        # e.g. "Lions Eye Diamond" does find "Lion's Eye Diamond"
        return response_dict['name']
    elif response_dict['object'] == 'error': # not a valid card name
        return False

def find_data_in_round(url, round_number):
    # round 18: emblem included as card, instead of the actual first card
    # round 28: "super lotus" makes it so many decks only have 2 real cards
    # round 39: 2-4 cards per deck!
    # round 45: formatting messed by illegal deck
    # round 48: deck lines in span, not div; missing line breaks
    # round 56: ???
    # round 80: fake cards again
    # round 107: illegal deck -> <strike> tags around deck and in tables (maybe can ignore those, as I use the text anyway?)

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    for post in soup.find_all('div', class_='post_wrap'):
        #print(post.find('h3', class_='row2').find('span', class_='author vcard').find('a').find('span').text)
        if post.find('h3', class_='row2').find('span', class_='author vcard').find('a').find('span').text == 'Namse':
            # check author -> Namse has the results
            pass
        else:
            continue # skip other peoples posts

        post_body = post.find('div', class_='post_body').find('div', class_='post entry-content')
        deck_lines = []
        table_lines = []

        for el in post_body.find_all('div') + post_body.find_all('span'):
            if (el.text[0]=='#') and (len(el.find_all('a', class_=re.compile('cardlink*')))>=2): # round 39 allows 2-4 cards
                deck_lines += [el]

        for line in post_body.text.splitlines():
            if (len(line.split('|')) > len(deck_lines)): # exact layout of table changes
                table_lines += [line]

        if len(deck_lines) + 1 == len(table_lines): # this is the results post
            results_post_body = post_body
            print(post.find('h3', class_='row2').find('a', itemprop='replyToUrl')['href'])
            break
        else:
            continue

    # parse actual content / save to file
    player_names = []
    decks = []
    results = []
    try:
        for div in deck_lines:
            player_names += [div.text[4:].split(' - ')[0].strip()]
            d = []

            for element in BeautifulSoup(str(div).split(' - ')[-1], 'html.parser').descendants:
                if isinstance(element, str) and element.strip(', '):
                    d.append(element.strip(', '))

            decks += [d] # can be 2 or 4

        for line in table_lines:
            if line.split('|')[0] != 'xx': # skip the table header
                # skip the sum column - I can generate that from the results and sometimes there are comments too
                results += [[s for s in line.split('|')[1:-1] if s != '']] # placement of '|' not always the same

        data_dict = {'player': player_names}
        decks = np.array(decks).astype('U256') # to accomodate arbitrary length strings

        # check / fix all card names
        for i in range(decks.shape[0]):
            for j in range(decks.shape[1]):
                card_name = check_card_name(decks[i, j])
                if card_name:
                    decks[i, j] = card_name
                else:
                    print(f"Problem with card {decks[i, j]}")

        for i in range(3): # might need to go further in some cases
            data_dict[f"card_{i+1}"] = decks[:, i]
        results = np.array(results)
        if not check_results(results):
            print(f"Problem with results in round {round_number}")
            return False
        results[results=='xx'] = '00'
        for i in range(results.shape[1]):
            data_dict[f"result_{i}"] = results[:, i]
        data_dict['round'] = np.ones(len(player_names), dtype=int) * round_number
        data = pd.DataFrame(data_dict)
        print(data.sample(5))

        data = fix_player_name_typos(data)

        # sort the results before saving? should be able to reconstruct who won against whom!
        data.to_csv(f"data/raw/round_{round_number}.csv", index=False, sep=';')
        return True
    except:
        print(f"No results found in {url}")
        return False

def scrape_banned_list(url='https://www.mtg-forum.de/topic/71910-cb-bannedliste/?p=619742'):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    card_lists = soup.find_all('div', class_='bb_deck')
    ban_list = {'regular': [c.text for c in card_lists[0].find_all('a', class_=re.compile('cardlink*'))]}
    ban_list['introducing'] = [c.text for c in card_lists[1].find_all('a', class_=re.compile('cardlink*'))]

    with open('data/banned_list.json', 'w', encoding='utf-8') as file:
        json.dump(ban_list, file, ensure_ascii=False, indent=4)

# find all rounds threads URLs
rounds = {}
for page_num in range(1, 7):
    url = f"https://www.mtg-forum.de/forum/194-card-blind-turniere/page-{page_num}"
    rounds.update(find_rounds_in_page(url))

# links to all threads
with open('data/urls.json', 'w', encoding='utf-8') as file:
    json.dump(rounds, file, ensure_ascii=False, indent=4)

# banned list
scrape_banned_list()

try: # scrape specified round
    n = int(sys.argv[1])
    success = find_data_in_round(rounds[n], n)
    if not success:
        # catch if the results are on the second page (only old rounds)
        success = find_data_in_round(f"{rounds[n]}page-2", n)
except: # scrape all rounds
    for n, url in rounds.items():
        success = find_data_in_round(url, n)
        if not success:
            # catch if the results are on the second page (only old rounds)
            success = find_data_in_round(f"{url}page-2", n)
