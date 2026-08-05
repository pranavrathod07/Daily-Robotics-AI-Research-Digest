import datetime
import time
import urllib.request
import urllib.error
import xml.etree.ElementTree as ET

def fetch_arxiv_robotics_papers():
    url = 'https://export.arxiv.org/api/query?search_query=cat:cs.RO+OR+cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=3'
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    # Retry loop: 5 baar try karega agar 503 error aata hai
    max_retries = 5
    for attempt in range(1, max_retries + 1):
        try:
            print(f"Fetching papers from ArXiv (Attempt {attempt}/{max_retries})...")
            with urllib.request.urlopen(req, timeout=15) as response:
                data = response.read().decode('utf-8')
                break # Success! Loop break kar do
        except urllib.error.HTTPError as e:
            print(f"HTTP Error {e.code}: {e.reason}")
            if attempt < max_retries:
                print("Server busy. Waiting 5 seconds before retrying...")
                time.sleep(5)
            else:
                raise e
        except Exception as e:
            print(f"Error: {e}")
            if attempt < max_retries:
                time.sleep(5)
            else:
                raise e
    
    root = ET.fromstring(data)
    ns = {'arxiv': 'http://www.w3.org/2005/Atom'}
    
    papers = []
    for entry in root.findall('arxiv:entry', ns):
        title = entry.find('arxiv:title', ns).text.strip().replace('\n', ' ')
        summary = entry.find('arxiv:summary', ns).text.strip().replace('\n', ' ')[:200] + "..."
        link = entry.find('arxiv:id', ns).text.strip()
        published = entry.find('arxiv:published', ns).text.strip()[:10]
        
        papers.append({
            'title': title,
            'summary': summary,
            'link': link,
            'published': published
        })
    return papers

def update_markdown_digest():
    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=30) # IST Time
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%I:%M %p IST")
    month_year_str = now.strftime("%b_%Y")
    
    filename = f"Daily_Robotics_Paper_{month_year_str}.md"
    
    try:
        papers = fetch_arxiv_robotics_papers()
    except Exception as e:
        print(f"Failed to fetch papers after retries: {e}")
        return # Pipeline fail karne ke bajaye exit karega taaki action block na ho
    
    content = f"\n\n### 🤖 Robotics & AI Digest - Updated at {time_str} ({date_str})\n\n"
    for i, paper in enumerate(papers, 1):
        content += f"#### {i}. {paper['title']}\n"
        content += f"- **Published Date:** {paper['published']}\n"
        content += f"- **Summary:** {paper['summary']}\n"
        content += f"- **Paper Link:** [Read on ArXiv]({paper['link']})\n\n"
    
    content += "---\n"

    try:
        with open(filename, "a", encoding="utf-8") as f:
            f.write(content)
    except FileNotFoundError:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Daily Robotics & AI Research Digest - {month_year_str}\n\n" + content)

if __name__ == "__main__":
    update_markdown_digest()
