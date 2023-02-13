import requests, json,re
from bs4 import BeautifulSoup as bs
import pandas as pd
from string import digits
from datetime import datetime
from urllib.parse import urlparse
import cloudscraper
def nftdropscalendar():
    def details(url):

        url = f"https://www.nftdropscalendar.com/upcoming-nfts?36a35725_page={url}"

        payload = ""
        headers = {
            "authority": "www.nftdropscalendar.com",
            "accept": "*/*",
            "accept-language": "en;q=0.6",
            "cache-control": "no-cache",
            "pragma": "no-cache",
            "referer": "https://www.nftdropscalendar.com/upcoming-nfts",
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-origin",
            "sec-gpc": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        print(response, url)
        return response
    def nft_page(url):
        

        url = f"https://www.nftdropscalendar.com{url}"

        payload = ""
        headers = {
            "authority": "www.nftdropscalendar.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en;q=0.6",
            "cache-control": "max-age=0",
            "referer": "https://www.nftdropscalendar.com/upcoming-nfts",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        print(response, url)
        return response
    
    li = list()
    number = 1 
    while True:
        dd = details(number)
        html = bs(dd.content, 'html.parser')
        all_ = html.find_all('div',class_='collection-list-9 w-dyn-items')[-1].find_all('div', class_='product-detail')
        if len(all_) <= 3:
            li.extend(all_)
            print(len(all_), len(li))
            break
        li.extend(all_)
        number += 1
    listings = list()
    for listing in li:
        url = listing.find('a',class_='link-block-19').get('href')
        try:
            data = nft_page(url)
        except:
            continue
        if data.status_code != 200:
            continue

        html = bs(data.content, 'html.parser')

        name = html.find('h1', class_='nft-project-title').text.strip() if html.find('h1', class_='nft-project-title') else 'NA'
        supply = html.find('div',class_='div-next-drops-info collection nftinfocard cc').text.strip() if html.find_all('div',class_='div-next-drops-info collection nftinfocard cc') else 'NA'
        price = listing.find('div', class_='tag-text mintprice lobx').text.strip() if listing.find('div', class_='tag-text mintprice lobx') else 'NA'
        date = html.find('div', class_='blockchain-nextdrop subtitle date nftinfocard').text.strip() if html.find('div', class_='blockchain-nextdrop subtitle date nftinfocard') else 'NA'
        description = html.find('p',class_='nft-description nftinfocard nftinfopage').text.strip() if html.find('p',class_='nft-description nftinfocard nftinfopage') else 'NA'
        source = 'nftdropscalendar.com'
        image = html.find('div',class_='left-column nftinfocard').find('img').get('src') if html.find('div',class_='left-column nftinfocard') else 'NA'
        urls = html.find('div', class_='project-links')
        source_url = f"https://www.nftdropscalendar.com{url}"
        blockchaine = listing.find('img', class_='bkcn imgrow').get('alt') if listing.find('img', class_='bkcn imgrow') else 'NA'
        for url in urls.find_all('a'):
            if 'twitter' in url.text.lower():
                twitter = url.get('href')
            if 'discord' in url.text.lower():
                discord = url.get('href')
            if 'website' in url.text.lower():
                website = url.get('href')

        # print(supply[0].text.json())
        data = {
        'projectName': name,
        'source':source,
        'projectImg':image,
        'source_url':source_url,
        'mintPrice':price,
        'mintSupply':supply,
        'blockchain':blockchaine,
        'description':description,
        'twitterURL':twitter,
        'website':website,
        'preSale':date,
        'discordURL':discord,}
        listings.append(data)
    return listings
def nftevening():
    listings = list()
    number = 1
    
    while True:
        url = f"https://nftevening.com/calendar/page/{number}"
        payload = ""
        response = requests.request("GET", url, data=payload)
        print(response, url)
        html = bs(response.content, 'html.parser')
        next_page = html.find('div', class_='events-nav').find('li')
        if not next_page:
            break
        
        listings.extend(html.find_all('div', class_='event'))
        number += 1
    print(len(listings))
    all_ = list()
    for listing in listings:
        name = listing.find('h2', class_='title').text.strip() if listing.find('h2', class_='title') else 'NA'
        if name == 'NA':
            continue
        image = listing.find('img', class_='img').get('lazy-src') if listing.find('img', class_='img') else 'NA'
        # print(listing.find('img', class_='img'))
        source = 'nftevening.com'
        source_url = f"https://calendar.nftevening.com{listing.find('div', class_='read-more').find('a').get('href')}" if listing.find('div', class_='read-more') else 'NA'
        for item in listing.find_all('tr'):
            
            if 'blockhain' in item.text.strip().lower():
                blockchaine = item.text.lower().replace('blockhain', '').strip()
            if 'supply' in item.text.strip().lower():
                supply = item.text.lower().replace('supply', '').strip()
            if 'price' in item.text.strip().lower():
                price = item.text.lower().replace('price', '').strip()
        for url in listing.find('ul', class_='social').find_all('li'):
            if 'twitter' in url.find('a').get('href'):
                twitter = url.find('a').get('href').lower()
            if 'discord' in url.find('a').get('href'):
                discord = url.find('a').get('href').lower()
        date = listing.find('div', class_='counter').get('drop_date') if listing.find('div', class_='counter') else 'NA'
        website = listing.find('ul', class_='social').find_all('li')[-1].find('a').get('href') if len(listing.find('ul', class_='social').find_all('li')) > 2 else 'NA'
        description = listing.find('div', class_='content').text.strip() if listing.find('div', class_='content') else 'NA'
        data = {
        'projectName': name,
        'source':source,
        'projectImg':image,
        'source_url':source_url,
        'mintPrice':price,
        'mintSupply':supply,
        'blockchain':blockchaine,
        'description':description,
        'twitterURL':twitter,
        'website':website,
        'preSale':date,
        'discordURL':discord,}
        data['preSale'] = datetime.strptime(date.split(' ')[0],"%Y-%m-%d").strftime("%B %d, %Y")
        all_.append(data)
    return all_
def nftiming():
    def req(pag):
        url = 'https://www.nftiming.com/'
        cookies = {
        'wpdiscuz_hide_bubble_hint': '1',
    }

        headers = {
            'authority': 'www.nftiming.com',
            'accept': '*/*',
            'accept-language': 'en;q=0.9',
            'content-type': 'multipart/form-data; boundary=----WebKitFormBoundary625u96ovDhOPUCl4',
            # 'cookie': 'wpdiscuz_hide_bubble_hint=1',
            'origin': 'https://www.nftiming.com',
            'referer': 'https://www.nftiming.com/nft-calendar/?_elements_per_page=50&_pagination_v1=2',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'sec-gpc': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36',
        }

        params = {
            'wpgb-ajax': 'refresh',
            '_elements_per_page': '50',
            '_pagination_v1': f'{pag}',
        }

        data = '------WebKitFormBoundary625u96ovDhOPUCl4\r\nContent-Disposition: form-data; name="wpgb"\r\n\r\n{"is_main_query":false,"main_query":[],"permalink":"https://www.nftiming.com/nft-calendar/","facets":[11,16,17,19,20,21],"lang":"","id":"oxygen-element-3149","is_template":"Oxygen","post_id":{"0":25371,"2":15,"9":20313},"paged":1}\r\n------WebKitFormBoundary625u96ovDhOPUCl4--\r\n'

        response = requests.post(url, params=params, cookies=cookies, headers=headers, data=data)

        print(response, url)
        return response.json()
    def detail(url):
        url = url

        payload = ""
        headers = {
            "authority": "www.nftiming.com",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en;q=0.9",
            "cookie": "wpdiscuz_hide_bubble_hint=1",
            "referer": "https://www.nftiming.com/nft-calendar/?_elements_per_page=50&_pagination_v1=1",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }

        response = requests.request("GET", url, data=payload, headers=headers)
        print(response, url)
        html = bs(response.content, 'html.parser')
        return html
    number = 1
    all_the_listing = list()
    while True:
        response = req(number)
        print(response['total'], number)
        
        html = bs(response['posts'], 'html.parser')
        all_the_listing.extend(html.find_all('div', id='div_block-3150-8964'))
        print(len(all_the_listing))
        if len(all_the_listing) >= response['total']:
            break
        else:
            number += 1
    df = list()
    for listing in all_the_listing:
        name = listing.find('div', id='text_block-5812-8964').text if listing.find('div', id='text_block-5812-8964') else "NA"
        source = 'nftiming.com'
        image = listing.find('div', id='div_block-3153-8964').get('style').replace('(','*').replace(')', '*').split('*')[1] if listing.find('div', id='div_block-3153-8964') else 'NA'
        url = listing.find('a',id='link-3152-8964').get('href') if listing.find('a',id='link-3152-8964') else 'NA'
        price = listing.find('span', id='span-3186-8964').text.strip() if listing.find('span', id='span-3186-8964') else 'NA'
        supply = listing.find('span', id='span-3194-8964').text.strip() if listing.find('span', id='span-3194-8964') else 'NA' 
        blockchaine = listing.find('div', id='code_block-3179-8964').text.strip() if listing.find('div', id='code_block-3179-8964') else 'NA'
        # description = listing.find('span', id='span-5818-8964').text.strip() if listing.find('span', id='span-5818-8964') else 'NA'
        listing_detail = detail(url)
        description = listing_detail.find('span', id='span-424-392').text.strip() if listing_detail.find('span', id='span-424-392') else 'NA'
        twitter = listing_detail.find('a', id='link-252-392').get('href') if listing_detail.find('a', id='link-252-392') else 'NA'
        website = listing_detail.find('a', id='link-254-392').get('href') if listing_detail.find('a', id='link-254-392') else 'NA'
        date = listing_detail.find('span', id='span-301-392').text.strip() if listing_detail.find('span', id='span-301-392') else 'NA'
        discrod = listing_detail.find('a',id='div_block-247-392').get('href') if listing_detail.find('a',id='div_block-247-392') else 'NA'
        # date_today = datetime.strftime("%d.%m.%Y")
        # pp = datetime.strptime(date,"%d.%m.%Y")
        pp = datetime.strptime(date,"%d.%m.%Y").strftime("%B %d, %Y")
        date = pp
        data = {
        'projectName': name,
        'source':source,
        'projectImg':image,
        'source_url':url,
        'mintPrice':price,
        'mintSupply':supply,
        'blockchain':blockchaine,
        'description':description,
        'twitterURL':twitter,
        'website':website,
        'preSale':date,
        'discordURL':discrod,}
        df.append(data)
    return df
def nftdroppers():
    def details(url):
        url = url
        payload = ""
        headers = {
            "authority": "nftdroppers.io",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "accept-language": "en;q=0.8",
            "cache-control": "no-cache",
            "cookie": "twk_idm_key=yE-oz4-cBDHl-PuBPkk9r; TawkConnectionTime=0; twk_uuid_62e137b754f06e12d88b9a77=%7B%22uuid%22%3A%221.7xXIwPhuiwODffebLUzhKrlzV1qClBK0NFJUduaa5K9svZ5069D73YDE5lCQefwKWkhHjRLvS0FQEbbRzlXqZ1IflW7WBDQfOjC3EECue3hBPRz8ejO144s1%22%2C%22version%22%3A3%2C%22domain%22%3A%22nftdroppers.io%22%2C%22ts%22%3A1674602491542%7D",
            "pragma": "no-cache",
            "referer": "https://nftdroppers.io/nft-collections/",
            "sec-fetch-dest": "document",
            "sec-fetch-mode": "navigate",
            "sec-fetch-site": "same-origin",
            "sec-fetch-user": "?1",
            "sec-gpc": "1",
            "upgrade-insecure-requests": "1",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
        }

        response = requests.request("GET", url, data=payload, headers=headers)

        print(response, url)
        return response

    # url = "https://nftdroppers.io/wp-admin/admin-ajax.php"
    url = 'https://nftdroppers.io/upcoming-nfts/'

    payload = "action=filter_auction&filters%5Bkeyword%5D=&filters%5BsortBy%5D=rand&settings%5Blayout%5D=&settings%5Bsource%5D=default&settings%5Bcategory%5D=&settings%5Bcolumn%5D=4&settings%5Bbutton_text%5D=Read%2BMore&settings%5Bposts_per_page%5D=10000&paged=0"
    headers = {
        "authority": "nftdroppers.io",
        "accept": "*/*",
        "accept-language": "en;q=0.9",
        "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
        "origin": "https://nftdroppers.io",
        "referer": "https://nftdroppers.io/nft-collections/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-origin",
        "sec-gpc": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36",
        "x-requested-with": "XMLHttpRequest"
    }

    response = requests.request("POST", url, data=payload, headers=headers)

   
    html = bs(response.content, 'html.parser')
    urls = html.find('div', class_='elementor-tab-content').find_all('a')
    res = list()
    for ur in urls:
        if ur.get('href') not in res:
            res.append(ur.get('href'))
    
    all_urls = list()
    for url in res:
        detail = details(url)
        if detail.status_code != 200:
            continue 
        dd = bs(detail.content, 'html.parser')
        data = {
            "projectName": dd.find('h1', class_='auction-title').text.strip() if dd.find('h1', class_='auction-title') is not None else '',
            "source":'nftdroppers.io',
            "projectImg": dd.find('div', class_='auction-feature-image').find('img').get('data-src') if dd.find('div', class_='auction-feature-image') is not None else '',
            "source_url": url
        }
        try:
            span = dd.find('div', class_='auction_inner_details').find('p')
        except AttributeError:
            span = ''
        ddf = str(span).replace('<br/>', '\n')
        ddf = bs(ddf,'html.parser').text
        
        
        for row in ddf.split('\n'):
            if 'price' in row.lower():
                data['mintPrice'] = row.strip().split(':')[-1]
                continue
            if 'collection count' in row.lower():
                data['mintSupply'] = row.lower().split(':')[-1]
                continue
            if 'presale 'in row.lower() or 'date' in row.lower():
                data['preSale'] = row.lower().split(':')[-1]
                continue
        links = dd.find('ul',class_='inr_main')
        
        if links:
            for link in links.find_all('a'):
                if 'website' in link.text.lower():
                    data['website'] = link.get('href')
                if 'discord'in link.get('href').lower():
                    data['discordURL'] = link.get('href')
                if 'twitter' in link.get('href').lower():
                    data['twitterURL'] = link.get('href')
            
        block = dd.find('div',class_='auction_meta_list')
        if block:
            for blo in block.find_all('div',class_='meta_mint'):
                if 'blockchain' in blo.find('h4').text.lower():
                    data['blockchain'] = blo.find('span').text.lower()
        data['description'] = dd.find('div',class_='tt-single-tab__content').text.replace('\n', ' ')
        try:
            data['preSale'] = datetime.strptime(data['preSale'].strip(),"%d/%m/%Y").strftime("%B %d, %Y")
        except:
            ''
        all_urls.append(data)
        
    for i in all_urls:
        url = i.get('website')
        if str(url) != 'nan':
            website_url = urlparse(url).hostname
            if website_url == 'nftcalendar.io':
                scraper = cloudscraper.create_scraper()
                dd = scraper.get(url)
                html = bs(dd.text, 'html.parser')
                site = html.find('span', class_='text-gray-500 dark:text-yellow-100')
                i['website'] = site.text.strip()

    return all_urls
def clean(data):
    for row in data:
        if str(row['twitterURL']) != 'nan':
            row['twitterURL'] = row['twitterURL'].strip('/').split('/')[-1]
        elif row['twitterURL'] == '#':
            row['twitterURL'] = 'NA'
        else:
            row['twitterURL'] = 'NA' 

        if str(row['description']) != 'nan':
            text = row['description']
            text = re.sub(r'[^\w\s%&]','',text)
            row['description'] = text.strip()
        else:
            row['description'] = 'NA' 

        if str(row['discordURL']) == 'nan':
            row['discordURL'] = 'NA'
        if str(row['blockchain']) == 'nan': 
            row['blockchain'] = 'NA'
        if str(row['preSale']) == 'nan': 
            row['preSale'] = 'NA'
        if str(row['website']) == 'nan': 
            row['website'] = 'NA'
        if str(row['projectImg']) == 'nan': 
            row['projectImg'] = 'NA'
        if str(row['projectName']) == 'nan': 
            row['projectName'] = 'NA'
        if row['discordURL'] == "https://discord.gg/brewiesnft":
            row['discordURL'] = 'NA'
        if row['discordURL'] == '#':
            row['discordURL'] = 'NA'
        if len(row['preSale'].split('–')) > 1:
            row['preSale'] = row['preSale'].strip().split('–')[0]
        if str(row['mintPrice']).strip() != 'nan':
            if type(row['mintPrice']) != float and str(row['mintPrice'].lower().strip()) == 'free mint':
                row['mintPrice'] = '0'
            row['mintPrice'] = ''.join(c for c in str(row['mintPrice']) if c in digits or c == '.') 
            if row['mintPrice'] == '':
                row['mintPrice'] = 'NA'
        else:
            row['mintPrice'] = 'NA'

        if str(row['mintSupply']) != 'nan':
                row['mintSupply'] = ''.join(c for c in str(row['mintSupply']) if c in digits)
        else:
            row['mintSupply'] = 'NA'  
        if row['mintSupply'] == '':
            row['mintSupply'] = 'NA'
        if row['website'] == '#':
            row['website'] = 'NA'

        if row['preSale'] != 'NA':
            row['date'] = datetime.strptime(row['preSale'].strip(),"%B %d, %Y").strftime("%Y-%m-%d")
        else:
            row['date'] = 'NA'
    return data
def main():
    li = list()
    one = nftdropscalendar()
    two = nftevening()
    three = nftiming()
    four = nftdroppers()
    li.extend(one)
    li.extend(two)
    li.extend(three)
    li.extend(four)
    p = pd.DataFrame(li).to_csv('combine_data.csv', index=False)
    dd = pd.read_csv('combine_data.csv').to_dict('records')
    dd = clean(dd)
    p = pd.DataFrame(dd).to_csv('combine_data.csv', index=False)

if __name__ == '__main__':
    main()