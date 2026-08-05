import datetime
import urllib.request
import xml.etree.ElementTree as ET

def fetch_arxiv_robotics_papers():
    # ArXiv API for Robotics (cs.RO) and Artificial Intelligence (cs.AI)
    url = 'https://export.arxiv.org/api/query?search_query=cat:cs.RO+OR+cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=3'
    
    # Adding User-Agent to avoid HTTP 503 / blocking by ArXiv servers
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    
    with urllib.request.urlopen(req) as response:
        data = response.read().decode('utf-8')
    
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
    # Modern timezone-aware datetime (Fixes DeprecationWarning)
    now = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=5, minutes=30) # IST Time
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%I:%M %p IST")
    month_year_str = now.strftime("%b_%Y") # e.g. Aug_2026
    
    filename = f"Daily_Robotics_Paper_{month_year_str}.md"
    papers = fetch_arxiv_robotics_papers()
    
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
