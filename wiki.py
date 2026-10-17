import urllib.request
import json
import urllib.parse

def generate_latex_wiki_list(subdomain):
    base_url = f"https://{subdomain}.fandom.com/api.php"
    apcontinue = None
    
    with open("wiki_list.tex", "w", encoding="utf-8") as f:
        f.write("\\begin{itemize}\n")
        
        while True:
            params = {
                "action": "query",
                "list": "allpages",
                "apnamespace": 0,
                "aplimit": 500,
                "format": "json"
            }
            if apcontinue:
                params["apcontinue"] = apcontinue
                
            query_string = urllib.parse.urlencode(params)
            full_url = f"{base_url}?{query_string}"
            
            req = urllib.request.Request(full_url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req) as response:
                data = json.loads(response.read().decode('utf-8'))
                
            pages = data.get("query", {}).get("allpages", [])
            
            for page in pages:
                title = page["title"]
                safe_title = (
                    title.replace("&", "\\&")
                         .replace("%", "\\%")
                         .replace("_", "\\_")
                         .replace("#", "\\#")
                )
                url_title = urllib.parse.quote(title.replace(" ", "_"))
                link = f"https://{subdomain}.fandom.com/wiki/{url_title}"
                
                f.write(f"  \\item \\href{{{link}}}{{{safe_title}}}\n")
                
            if "continue" in data and "apcontinue" in data["continue"]:
                apcontinue = data["continue"]["apcontinue"]
            else:
                break
                
        f.write("\\end{itemize}\n")

generate_latex_wiki_list("providence")
print("Successfully generated wiki_list.tex!")
