# 🔥 AEM Cloud Permission Hellscape 🔥

Have you ever spent hours or days banging your head against the wall over AEM Cloud permissions?  
This application helps **visualize deeply-nested group membership and permissions in AEMaaCS**, so you can get out of permissions hell and see exactly who’s in what group.

---

## 🛠️ **Installation & Setup Instructions**

**Step 1: Extract your AEM `/home` content**

- In CRXDE or Package Manager, create a package containing your entire `/home` directory and download the ZIP.

**Step 2: Prepare your local folder structure**

- Unzip the package you downloaded.
- Inside the package, locate `jcr_root/home`.
- Copy the entire `home` directory (and its contents) to your project folder so the structure is:

  ```
  home-package-dump/home/users
  home-package-dump/home/groups
  home-package-dump/home/_rep_policy.xml
  ```

- Make sure **nothing else is in the `home-package-dump` folder**.

---

## 🚦 **How It Works**

This toolkit is now **split into two simple scripts** for clean modularity:

### 1️⃣ `whereIsEveryoneFFS.py`

- **Scans your AEM groups export** (from `home-package-dump/home/groups`)
- **Extracts** key info: `jcr:uuid`, `rep:authorizableId`, `rep:principalName`, and AEM path.
- **Counts how many other groups are members of each group.**
- **Outputs:**
  - `group-info.json` — a structured JSON array of all groups, ready for analysis or display.

### 2️⃣ `groupInfoToHTML.py`

- **Reads `group-info.json` ONLY** (does not hit the filesystem or re-crawl any XML)
- **Builds a browsable HTML table:**
  - Columns: Group UUID, Authorizable ID, Principal Name, Path, and **Group Members (Count)**
- **Outputs:**
  - `openInBrowser.html` — a human-friendly report you can open in any browser.

---

## 🚀 **Running the Tool**

From your project root (same directory as the scripts):

### **Step 1: Build the JSON snapshot**

```sh
python3 whereIsEveryoneFFS.py
```
