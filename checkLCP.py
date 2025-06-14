import requests
import time
import json
import os   # NEW

# Load API key from config.json
with open('config.json', 'r') as f:
    api_key = json.load(f)['api_key']

def get_lcp(api_key, url, strategy, retries=3, delay=2):
    attempt = 0
    while attempt < retries:
        try:
            resp = requests.get(
                'https://www.googleapis.com/pagespeedonline/v5/runPagespeed',
                params={'url': url, 'key': api_key, 'strategy': strategy},
                timeout=30               # good practice
            )
            resp.raise_for_status()
            lcp_ms = resp.json()['lighthouseResult']['audits'] \
                               ['largest-contentful-paint']['numericValue']
            return round(lcp_ms / 1000, 2)
        except Exception as e:
            attempt += 1
            time.sleep(delay)
    print(f"All retries failed for {strategy.upper()} - {url}")
    return None

# Open output files in **append** mode, line-buffered
with open('lcp_mobile.txt', 'a', buffering=1) as mobile_file, \
     open('lcp_desktop.txt', 'a', buffering=1) as desktop_file, \
     open('urls.txt', 'r') as url_file:

    for count, line in enumerate(url_file, start=1):
        url = line.strip()
        if not url:
            continue

        time.sleep(1)          # to avoid API rate limits
        mobile_lcp  = get_lcp(api_key, url, 'mobile')
        desktop_lcp = get_lcp(api_key, url, 'desktop')

        # ---- write + flush + fsync ----
        for lcp, fp in ((mobile_lcp, mobile_file), (desktop_lcp, desktop_file)):
            fp.write(f"{lcp if lcp is not None else 'N/A'}\n")
            fp.flush()                   # flush Python buffer
            os.fsync(fp.fileno())        # force OS flush to disk

        print(f"URL {count} done")

print("ALL URLS done")
