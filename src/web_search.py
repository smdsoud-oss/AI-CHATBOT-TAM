import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()
client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def search_web(query):
    try:
        response = client.search(
            query=query,
            search_depth="basic",
            max_results=3
        )
        results = response.get('results', [])
        if not results:
            return None

        answer = f"🌐 Web Search Results for: '<b>{query}</b>'\n\n"
        for i, result in enumerate(results, 1):
            title = result['title']
            content = result['content'][:200]
            url = result['url']
            answer += f"{i}. <b>{title}</b>\n"
            answer += f"   {content}...\n"
            answer += f"   <a href='{url}' target='_blank' style='color:#7aa2f7;'>🔗 {url}</a>\n\n"

        return answer
    except Exception:
        return None