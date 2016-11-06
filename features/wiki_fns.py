import requests
import json
import re
from apiclient.discovery import build


def wiki_extract(select_topic):
    try:
        url = 'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&exintro=&explaintext=&titles='+select_topic+'&format=json'

        response = requests.get(url)
        jtext = response.text

        jobj = json.loads(jtext)
        s = jobj['query']['pages'][jobj['query']['pages'].keys()[0]]['extract']
        s = s.encode('ascii','ignore')

        s = re.sub('\\n', ' ', s) # remove \n
        return s
    except:
        return -1

def wiki_search(search_term):

    url = 'https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch='+search_term+'&prop=extracts&exintro=&explaintext=&format=json'
    response = requests.get(url)
    jtext = response.text
    jobk = json.loads(jtext)

    i = 0
    while i<10:
        exact_title = str(jobk['query']['search'][i]['title'].encode('utf-8'))
        if 'disambiguation' in exact_title:
            i += 1
        elif 'refer' in wiki_extract(exact_title)[0:50]:
            i += 1
        else:
            break

    return wiki_extract(exact_title)


def save_images(search_term, num_images):
    service = build("customsearch", "v1",
               developerKey="AIzaSyDHprXaJe8U1CpF7kYH6IWUktAViHhiWnc")
    res = service.cse().list(
        q=search_term,
        cx='004441307141111453178:v-kf4bu7lsy',
        num=num_images,
        safe='high',
    ).execute()

    good_image_num = 0
    for seq in range(num_images):
        try:
            image_url = res['items'][seq]['pagemap']['cse_image'][0]['src']
            good_image_num += 1
        except:
            try:
                image_url = res['items'][seq]['pagemap']['imageobject'][0]['contenturl']
                good_image_num += 1
            except:
                continue

        response = requests.get(image_url)
        image_name = search_term + str(seq)
        with open('./Images/'+image_name, 'w') as f:
            f.write(response.content)
    return good_image_num