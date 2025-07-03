#!/usr/bin/env python3
from pathlib import Path
import json

JSON_FILE = Path("group-info.json")
HTML_FILE = Path("openInBrowser.html")

def write_html(group_list):
    html = [
        "<!DOCTYPE html>",
        "<html><head>",
        "<meta charset='utf-8'>",
        "<title>AEM Cloud Permission Hellscape — Group Info Visualization</title>",
        "<style>",
        "body { font-family: sans-serif; margin: 2em; }",
        "table { border-collapse: collapse; width: 100%; max-width: 1200px; }",
        "th, td { border: 1px solid #ccc; padding: 8px 12px; text-align: left; }",
        "th { background: #f5f5f5; }",
        "tr:nth-child(even) { background: #fafafa; }",
        "td { max-width: 400px; word-break: break-word; }",
        "</style>",
        "</head><body>",
        "<h1>🔥 AEM Cloud Permission Hellscape — Group Info Visualization 🔥</h1>",
        f"<p><b>{len(group_list)} groups found.</b></p>",
        "<table>",
        "<tr>",
        "<th>#</th>",
        "<th>jcr:uuid</th>",
        "<th>rep:authorizableId</th>",
        "<th>rep:principalName</th>",
        "<th>AEM Path</th>",
        "<th>Group Members (Count)</th>",
        "<th>Users in this Group</th>",
        "</tr>"
    ]
    for i, group in enumerate(group_list, 1):
        html.append(
            f"<tr><td>{i}</td>"
            f"<td>{group.get('jcr:uuid','')}</td>"
            f"<td>{group.get('rep:authorizableId','')}</td>"
            f"<td>{group.get('rep:principalName','')}</td>"
            f"<td><code>{group.get('aem_path','')}</code></td>"
            f"<td>{group.get('group_member_count', 0)}</td>"
            f"<td>{group.get('users_in_this_group', '')}</td></tr>"
        )
    html.extend(["</table>", "</body></html>"])
    with open(HTML_FILE, "w", encoding="utf-8") as f:
        f.write("\n".join(html))
    print(f"✅ Table written to {HTML_FILE}")

def main():
    print("🔎 Reading group-info.json...")
    with open(JSON_FILE, "r", encoding="utf-8") as f:
        group_list = json.load(f)
    write_html(group_list)
    print("\n✨ All done! Open openInBrowser.html in your browser to view the table.")

if __name__ == "__main__":
    main()
