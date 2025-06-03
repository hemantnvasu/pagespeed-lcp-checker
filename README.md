# PageSpeed LCP Checker

This project uses the Google PageSpeed Insights API to fetch the **Largest Contentful Paint (LCP)** scores for a list of URLs. It runs audits for both **mobile** and **desktop** strategies and writes the results to output files.

---

## 📁 Project Structure
<pre>
├── checkLCP.py # Main script
├── urls.txt # Input file: list of URLs (one per line)
├── lcp_mobile.txt # Output file: mobile LCP scores
├── lcp_desktop.txt # Output file: desktop LCP scores
├── .gitignore # Files to exclude from version control
├── requirements.txt # Python package dependencies
└── README.md # Project documentation
</pre>

## 🔧 Setup

1. Create a key file (JSON file) (do not upload this to GitHub):\
   <pre>
   {
       "api_key": "YOUR_GOOGLE_API_KEY_HERE"
   }
   </pre>
   Save it as config.json or key.json, and make sure it's listed in .gitignore.
3. Add URLs to urls.txt\
   One URL per line.
4. Run the script.

## 📄 Output:

**lcp_mobile.txt** – LCP scores (in seconds) for mobile\
**lcp_desktop.txt** – LCP scores (in seconds) for desktop\
If the script fails to fetch a score, it writes N/A.

## ⚠️ Notes
The script includes retry logic and rate limiting (1 second delay).\
Your API key is sensitive — never commit it to GitHub.
