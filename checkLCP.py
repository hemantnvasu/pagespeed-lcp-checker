import requests
import time
import json

# Load API key from config.json
with open('config.json', 'r') as f:
    config = json.load(f)
api_key = config['api_key']

# def get_lcp(api_key, url, strategy):
#     try:
#         response = requests.get(
#             'https://www.googleapis.com/pagespeedonline/v5/runPagespeed',
#             params={
#                 'url': url,
#                 'key': api_key,
#                 'strategy': strategy
#             }
#         )
#         response.raise_for_status()
#         data = response.json()
#         lcp_ms = data['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']
#         return round(lcp_ms / 1000, 2)
#     except Exception as e:
#         print(f"Error for {strategy} - {url}: {e}")
#         return None

def get_lcp(api_key, url, strategy, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            # print(f"Attempt {attempt+1} for {strategy.upper()} - {url}")
            response = requests.get(
                'https://www.googleapis.com/pagespeedonline/v5/runPagespeed',
                params={
                    'url': url,
                    'key': api_key,
                    'strategy': strategy
                }
            )
            response.raise_for_status()
            data = response.json()
            lcp_ms = data['lighthouseResult']['audits']['largest-contentful-paint']['numericValue']
            return round(lcp_ms / 1000, 2)
        except Exception as e:
            # print(f"Error on attempt {attempt+1} for {strategy.upper()} - {url}: {e}")
            attempt += 1
            time.sleep(delay)

    print(f"All retries failed for {strategy.upper()} - {url}")
    return None


# API key
api_key = 'AIzaSyDPt5HnJj6TCjUzixEtFZ4lB1DO5WrQIXo'

# Open output files
with open('lcp_mobile.txt', 'w') as mobile_file, open('lcp_desktop.txt', 'w') as desktop_file:
    # Read URLs
    with open('urls.txt', 'r') as url_file:
        count = 1
        for line in url_file:
            time.sleep(1) # delays to avoid rate limiting
            url = line.strip()
            if not url:
                continue

            # Get LCPs
            mobile_lcp = get_lcp(api_key, url, 'mobile')
            desktop_lcp = get_lcp(api_key, url, 'desktop')

            # Write to respective files
            if mobile_lcp is not None:
                # mobile_file.write(f"{url}: {mobile_lcp} s\n")
                mobile_file.write(f"{mobile_lcp}\n")
            else:
                mobile_file.write("N/A\n")
            if desktop_lcp is not None:
                # desktop_file.write(f"{url}: {desktop_lcp} s\n")
                desktop_file.write(f"{desktop_lcp}\n")
            else:
                desktop_file.write("N/A\n")
            
            # if mobile_lcp is None or desktop_lcp is None:
            #     print("Found NONE in between. Aborting the program")
            #     break
            
            print(f"URL: {count} done")
            count += 1

print("ALL URLS done")