#!/usr/bin/env python3
from pathlib import Path
import re
import json
import subprocess
import sys

GROUPS_PATH = Path("home-package-dump/home/groups")
USERS_PATH = Path("home-package-dump/home/users")
JSON_FILE = Path("group-info.json")

# Regex patterns
uuid_pattern = re.compile(r'jcr:uuid="([^"]+)"')
authid_pattern = re.compile(r'rep:authorizableId="([^"]+)"')
principal_pattern = re.compile(r'rep:principalName="([^"]+)"')
members_pattern = re.compile(r'rep:members="(?:\{WeakReference\})?\[([^\]]*)\]"')
display_name_pattern = re.compile(r'displayName="([^"]*)"')
group_principal_names_pattern = re.compile(r'rep:groupPrincipalNames="([^"]*)"')
external_local_principals_pattern = re.compile(r'rep:externalLocalPrincipalNames="([^"]*)"')

def extract_group_info(content_xml, group_path):
    try:
        xml_text = content_xml.read_text(encoding="utf-8")
        uuid_match = uuid_pattern.search(xml_text)
        authid_match = authid_pattern.search(xml_text)
        principal_match = principal_pattern.search(xml_text)
        members_match = members_pattern.search(xml_text)
        jcr_uuid = uuid_match.group(1) if uuid_match else None
        authorizable_id = authid_match.group(1) if authid_match else None
        principal_name = principal_match.group(1) if principal_match else None
        members = []
        if members_match:
            members = [m.strip() for m in members_match.group(1).split(",") if m.strip()]
        # Only add if jcr:uuid OR rep:authorizableId present
        if jcr_uuid or authorizable_id:
            return {
                "jcr:uuid": jcr_uuid,
                "rep:authorizableId": authorizable_id,
                "rep:principalName": principal_name,
                "aem_path": group_path,
                "group_members": members  # <-- for group count use
            }
        else:
            return None
    except Exception as e:
        print(f"{content_xml}: ⚠️ Error reading/parsing file: {e}")
        return None

def collect_groups():
    group_list = []
    if not GROUPS_PATH.exists():
        print(f"❌ Groups folder not found at {GROUPS_PATH.resolve()}")
        return group_list
    for item in GROUPS_PATH.iterdir():
        if not item.is_dir():
            continue
        # Check for direct group: /home/groups/<group>/.content.xml
        content_xml = item / ".content.xml"
        if content_xml.exists():
            result = extract_group_info(content_xml, f"/home/groups/{item.name}")
            if result:
                group_list.append(result)
        # Now check for nested group: /home/groups/<letter>/<group>/.content.xml
        for subitem in item.iterdir():
            if subitem.is_dir():
                sub_content_xml = subitem / ".content.xml"
                if sub_content_xml.exists():
                    result = extract_group_info(sub_content_xml, f"/home/groups/{item.name}/{subitem.name}")
                    if result:
                        group_list.append(result)
    return group_list

def compute_group_member_counts(group_list):
    """Adds a 'group_member_count' key to each group dict, with the number of member UUIDs that are groups."""
    all_group_uuids = set(g['jcr:uuid'] for g in group_list if g.get('jcr:uuid'))
    for g in group_list:
        members = g.get('group_members', [])
        count = sum(1 for m in members if m in all_group_uuids)
        g['group_member_count'] = count
    return group_list

def collect_users_and_groups():
    """
    Scans all users and builds a mapping: group_authorizableId (case-insensitive) -> set of displayName(s)
    Scans both rep:groupPrincipalNames AND rep:externalLocalPrincipalNames for group membership.
    """
    group_to_users = {}
    if not USERS_PATH.exists():
        print(f"❌ Users folder not found at {USERS_PATH.resolve()}")
        return group_to_users

    for xmlfile in USERS_PATH.rglob(".content.xml"):
        try:
            content = xmlfile.read_text(encoding="utf-8", errors="ignore")

            # Find all displayNames (prefer the longest to avoid empty strings)
            display_names = display_name_pattern.findall(content)
            display_name = ""
            if display_names:
                display_name = max(display_names, key=len).strip()

            all_group_principals = set()

            # Get all rep:groupPrincipalNames in the XML (any node)
            for match in group_principal_names_pattern.findall(content):
                group_names = [g.strip() for g in match.split(",") if g.strip()]
                all_group_principals.update(group_names)

            # Also get all rep:externalLocalPrincipalNames
            for match in external_local_principals_pattern.findall(content):
                group_names = [g.strip() for g in match.split(",") if g.strip()]
                all_group_principals.update(group_names)

            if display_name and all_group_principals:
                for group in all_group_principals:
                    group_to_users.setdefault(group.lower(), set()).add(display_name)
        except Exception as e:
            print(f"{xmlfile}: ⚠️ Error reading file: {e}")
    return group_to_users

def attach_user_display_names(group_list):
    """
    Attach users_in_this_group as a comma-separated string of display names,
    using case-insensitive matching of rep:authorizableId.
    """
    group_to_users = collect_users_and_groups()
    for g in group_list:
        groupname = g.get("rep:authorizableId", "").strip().lower()
        users = group_to_users.get(groupname, set())
        g["users_in_this_group"] = ", ".join(sorted(users)) if users else ""
    return group_list

def write_json(group_list):
    # Remove the helper field 'group_members' for cleanliness
    for g in group_list:
        g.pop('group_members', None)
    with open(JSON_FILE, "w", encoding="utf-8") as f:
        json.dump(group_list, f, indent=2)
    print(f"\n✅ JSON array saved to {JSON_FILE}")
    print(f"🎉 {len(group_list)} groups found!")

def main():
    print("🔎 Crawling groups and extracting info...")
    group_list = collect_groups()
    group_list = compute_group_member_counts(group_list)
    group_list = attach_user_display_names(group_list)
    write_json(group_list)
    print("\n✨ All done! group-info.json is ready for HTML conversion.")
    print("➡️ Generating HTML report via groupInfoToHTML.py ...")
    try:
        subprocess.run([sys.executable, "groupInfoToHTML.py"], check=True)
    except Exception as e:
        print(f"⚠️ Could not execute groupInfoToHTML.py: {e}")

if __name__ == "__main__":
    main()
