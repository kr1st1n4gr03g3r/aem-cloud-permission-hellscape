#!/usr/bin/env python3
from pathlib import Path
import re
import json

GROUPS_PATH = Path("home-package-dump/home/groups")
JSON_FILE = Path("group-info.json")
HTML_FILE = Path("openInBrowser.html")

# Regex patterns
uuid_pattern = re.compile(r'jcr:uuid="([^"]+)"')
authid_pattern = re.compile(r'rep:authorizableId="([^"]+)"')

def collect_groups():
    group_list = []

    if not GROUPS_PATH.exists():
        print(f"❌ Groups folder not found at {GROUPS_PATH.resolve()}")
        return group_list

    for t_folder in GROUPS_PATH.iterdir():
        if not t_folder.is_dir():
            continue
        for group_dir in t_folder.iterdir():
            content_xml = group_dir / ".content.xml"
            if content_xml.exists():
                try:
                    xml_text = content_xml.read_text(encoding="utf-8")
                    uuid_match = uuid_pattern.search(xml_text)
                    authid_match = authid_pattern.search(xml_text)
                    jcr_uuid = uuid_match.group(1) if uuid_match else None
                    authorizable_id = authid_match.group(1) if authid_match else None
                    group_list.append({
                        "jcr:uuid": jcr_uuid,
                        "rep:authorizableId": authorizable_id
                    })
                except Exception as e:
                    print(f"{group_dir.name}: ⚠️ Error reading/parsing file: {e}")
    return group_list

def write_json(group_list):
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(group_list, f, indent=2)
    print(f"\n✅ JSON array saved to {JSON_FILE}")
    print(f"🎉 {len(group_list)} groups found!")

def write_html(group_list):
    html = [
        "<!DOCTYPE html>",
        "<html><head>",
        "<meta charset='utf-8'>",
        "<title>AEM Cloud Permission Hellscape — Group Info Visualization</title>",
        "<style>",
        "body { font-family: sans-serif; margin: 2em; }",
        "table { border-collapse: collapse; width: 100%; max-width: 800px; }",
        "th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }",
        "th { background: #f5f5f5; }",
        "tr:nth-child(even) { background: #fafafa; }",
        "</style>",
        "</head><body>",
        "<h1>🔥 AEM Cloud Permission Hellscape — Group Info Visualization 🔥</h1>",
        f"<p><b>{len(group_list)} groups found.</b></p>",
        "<table>",
        "<tr><th>#</th><th>jcr:uuid</th><th>rep:authorizableId</th></tr>"
    ]
    for i, group in enumerate(group_list, 1):
        html.append(
            f"<tr><td>{i}</td>"
            f"<td>{group.get('jcr:uuid','')}</td>"
            f"<td>{group.get('rep:authorizableId','')}</td></tr>"
        )
    html.extend(["</table>", "</body></html>"])

    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    print(f"✅ Table written to {HTML_FILE}")

def main():
    print("🔎 Crawling groups and extracting info...")
    group_list = collect_groups()
    write_json(group_list)
    write_html(group_list)
    print("\n✨ All done! Open openInBrowser.html in your browser to view the table.")

if __name__ == "__main__":
    main()
