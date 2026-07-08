#!/usr/bin/env python3
"""
Fetch official agent skills from the awesome-agent-skills README.
Downloads SKILL.md + all reference files for each skill.

Strategy:
  - officialskills.sh URLs → scrape page to find actual GitHub URL
  - Direct GitHub URLs → parse directly
  - Fetch git trees per unique repo
  - Download all files under each skill's directory

Usage:
    GITHUB_TOKEN=ghp_xxx python3 scripts/fetch-official-skills.py [path/to/README.md]
"""

import os
import re
import sys
import time
import json
import shutil
from pathlib import Path
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed

import requests

# ── Configuration ────────────────────────────────────────────────────

README_PATH = sys.argv[1] if len(sys.argv) > 1 else "/home/k0walski/other/awesome-agent-skills/README.md"
SCRIPT_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = SCRIPT_DIR.parent / "skillsrc" / "data"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")
RAW_BASE = "https://raw.githubusercontent.com"
API_BASE = "https://api.github.com"

API_INTERVAL = 0.4
PAGE_INTERVAL = 0.15
RAW_INTERVAL = 0.05
MAX_RETRIES = 3
MAX_FILE_SIZE = 2_000_000

SKIP_SECTIONS_LOWER = {"redhat"}

VENDOR_CATEGORIES = {
    "anthropics": "Documents & Content",
    "voltagent": "Developer Tools",
    "testmu-ai": "Testing & QA",
    "zero": "Backend & APIs",
    "angular": "Frontend & UI",
    "composiohq": "Backend & APIs",
    "supabase": "Backend & APIs",
    "google-gemini": "AI & Machine Learning",
    "stripe": "Backend & APIs",
    "trycourier": "Backend & APIs",
    "callstackincubator": "Frontend & UI",
    "better-auth": "Backend & APIs",
    "tinybirdco": "Databases & Data",
    "hashicorp": "Cloud & Infrastructure",
    "sanity-io": "Backend & APIs",
    "firecrawl": "Search & Web",
    "neondatabase": "Databases & Data",
    "clickhouse": "Databases & Data",
    "remotion-dev": "Documents & Content",
    "replicate": "AI & Machine Learning",
    "typefully": "Backend & APIs",
    "veniceai": "AI & Machine Learning",
    "vercel-labs": "Cloud & Infrastructure",
    "cloudflare": "Cloud & Infrastructure",
    "netlify": "Cloud & Infrastructure",
    "google-labs-code": "Frontend & UI",
    "googleworkspace": "Productivity & Collaboration",
    "expo": "Mobile & Desktop",
    "huggingface": "AI & Machine Learning",
    "trailofbits": "Security",
    "getsentry": "DevOps & Monitoring",
    "microsoft": "Developer Tools",
    "fal-ai-community": "AI & Machine Learning",
    "wordpress": "Mobile & Desktop",
    "openai": "AI & Machine Learning",
    "figma": "Frontend & UI",
    "coreyhaines31": "Product & Strategy",
    "realkimbarrett": "Product & Strategy",
    "binance": "Backend & APIs",
    "apollographql": "Backend & APIs",
    "auth0": "Backend & APIs",
    "brave": "Search & Web",
    "browserbase": "Testing & QA",
    "coderabbitai": "DevOps & Monitoring",
    "coinbase": "Backend & APIs",
    "datadog-labs": "DevOps & Monitoring",
    "firebase": "Cloud & Infrastructure",
    "flutter": "Mobile & Desktop",
    "deanpeters": "Product & Strategy",
    "phuryn": "Product & Strategy",
    "minimax-ai": "AI & Machine Learning",
    "duckdb": "Databases & Data",
    "greensock": "Frontend & UI",
    "garrytan": "Developer Tools",
    "makenotion": "Productivity & Collaboration",
    "resend": "Backend & APIs",
    "addyosmani": "Frontend & UI",
    "mongodb": "Databases & Data",
    "redis": "Databases & Data",
    "nvidia": "AI & Machine Learning",
    "google": "Cloud & Infrastructure",
    "cypress-io": "Testing & QA",
    "officialzeroxyz": "Backend & APIs",
    "lambdatest": "Testing & QA",
}

CACHE_DIR = SCRIPT_DIR.parent / "skillsrc"
PAGE_CACHE_FILE = CACHE_DIR / ".page_cache.json"
TREE_CACHE_FILE = CACHE_DIR / ".tree_cache.json"

# ── State ────────────────────────────────────────────────────────────

_tree_cache: dict[str, list[str] | None] = {}
_page_cache: dict[str, list[str] | None] = {}
_last_api_call = 0.0
_last_page_call = 0.0
_last_raw_call = 0.0
_stats = {"ok": 0, "fail": 0, "skip": 0, "files": 0}
_failures: dict[str, list[str]] = {}


def load_caches():
    global _page_cache, _tree_cache
    if PAGE_CACHE_FILE.exists():
        with open(PAGE_CACHE_FILE) as f:
            raw = json.load(f)
        _page_cache.clear()
        for k, v in raw.items():
            _page_cache[k] = v
        log(f"[info] Loaded {len(_page_cache)} page cache entries")
    if TREE_CACHE_FILE.exists():
        with open(TREE_CACHE_FILE) as f:
            raw = json.load(f)
        _tree_cache.clear()
        for k, v in raw.items():
            _tree_cache[k] = v
        log(f"[info] Loaded {len(_tree_cache)} tree cache entries")


def save_caches():
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    with open(PAGE_CACHE_FILE, "w") as f:
        json.dump({k: list(v) if v else None for k, v in _page_cache.items()}, f)
    with open(TREE_CACHE_FILE, "w") as f:
        json.dump(_tree_cache, f)
    log(f"[info] Saved caches ({len(_page_cache)} pages, {len(_tree_cache)} trees)")

# ── Helpers ──────────────────────────────────────────────────────────


def log(msg: str):
    print(msg, flush=True)


def yaml_escape(s: str) -> str:
    s = s.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{s}"'


def gh_api_headers() -> dict:
    h = {"Accept": "application/vnd.github+json"}
    if GITHUB_TOKEN:
        h["Authorization"] = f"Bearer {GITHUB_TOKEN}"
    return h


# ── HTTP with rate limiting ──────────────────────────────────────────


def api_get(url: str) -> requests.Response | None:
    global _last_api_call
    for attempt in range(MAX_RETRIES):
        elapsed = time.time() - _last_api_call
        if elapsed < API_INTERVAL:
            time.sleep(API_INTERVAL - elapsed)
        try:
            resp = requests.get(url, headers=gh_api_headers(), timeout=30)
            _last_api_call = time.time()

            remaining = resp.headers.get("X-RateLimit-Remaining")
            if remaining is not None and int(remaining) < 5:
                reset_ts = int(resp.headers.get("X-RateLimit-Reset", 0))
                wait = max(reset_ts - int(time.time()), 1)
                log(f"  [rate-limit] {remaining} remaining, waiting {wait}s …")
                time.sleep(wait + 1)
                continue

            return resp
        except requests.RequestException as exc:
            wait = 2 ** (attempt + 1)
            log(f"  [retry {attempt+1}/{MAX_RETRIES}] {exc} — waiting {wait}s")
            time.sleep(wait)
    return None


def page_get(url: str) -> str | None:
    global _last_page_call
    for attempt in range(2):
        elapsed = time.time() - _last_page_call
        if elapsed < PAGE_INTERVAL:
            time.sleep(PAGE_INTERVAL - elapsed)
        try:
            resp = requests.get(url, timeout=15, headers={"User-Agent": "dotagen-fetcher/1.0"})
            _last_page_call = time.time()
            if resp.status_code == 200:
                return resp.text
            return None
        except requests.RequestException:
            time.sleep(1)
    return None


def raw_get(url: str) -> bytes | None:
    for attempt in range(MAX_RETRIES):
        try:
            resp = requests.get(url, timeout=30)
            if resp.status_code == 200:
                return resp.content
            if resp.status_code == 404:
                return None
        except requests.RequestException:
            time.sleep(0.5)
    return None


# ── Git tree fetching ────────────────────────────────────────────────


def fetch_tree(org: str, repo: str, branch: str = "main") -> list[str] | None:
    cache_key = f"{org.lower()}/{repo.lower()}@{branch}"
    if cache_key in _tree_cache:
        return _tree_cache[cache_key]

    url = f"{API_BASE}/repos/{org}/{repo}/git/trees/{branch}?recursive=1"
    resp = api_get(url)
    if resp is None:
        _tree_cache[cache_key] = None
        return None

    if resp.status_code == 404 and branch == "main":
        _tree_cache[cache_key] = None
        result = fetch_tree(org, repo, "master")
        return result

    if resp.status_code != 200:
        _tree_cache[cache_key] = None
        return None

    data = resp.json()
    if data.get("truncated"):
        log(f"    [warn] tree for {org}/{repo} is TRUNCATED")

    paths = [e["path"] for e in data.get("tree", []) if e["type"] == "blob"]
    _tree_cache[cache_key] = paths
    return paths


# ── officialskills.sh page scraping ──────────────────────────────────


GITHUB_URL_RE = re.compile(
    r'https://github\.com/([\w.-]+)/([\w.-]+)/tree/([\w.-]+)/([\w./-]+)'
)


def resolve_officialskills(url: str) -> tuple[str, str, str, str] | None:
    """Scrape officialskills.sh page to extract GitHub coords."""
    if url in _page_cache:
        cached = _page_cache[url]
        return tuple(cached) if cached else None

    html = page_get(url)
    if html is None:
        _page_cache[url] = None
        return None

    # Find the GitHub tree URL in the page
    match = GITHUB_URL_RE.search(html)
    if match:
        org = match.group(1)
        repo = match.group(2).rstrip('"').rstrip("'").rstrip(")")
        branch = match.group(3).rstrip('"').rstrip("'").rstrip(")")
        path = match.group(4).rstrip('"').rstrip("'").rstrip(")")

        coords = [org, repo, branch, path]
        _page_cache[url] = coords
        return tuple(coords)

    _page_cache[url] = None
    return None


# ── README parsing ───────────────────────────────────────────────────

ENTRY_RE = re.compile(r"^-\s+\*\*\[([^\]]+)\]\(([^)]+)\)\*\*\s+-\s+(.+)$")
SECTION_RE = re.compile(r'<h3[^>]*>(.+?)</h3>')


def parse_readme(path: str) -> list[dict]:
    with open(path, encoding="utf-8") as f:
        lines = f.readlines()

    entries: list[dict] = []
    current_section = ""
    skip_section = False

    for line in lines:
        stripped = line.strip()

        if "### Community Skills" in stripped:
            break

        m_sec = SECTION_RE.search(line)
        if m_sec:
            current_section = m_sec.group(1).strip()
            skip_section = any(s in current_section.lower() for s in SKIP_SECTIONS_LOWER)

        if skip_section:
            continue

        m = ENTRY_RE.match(stripped)
        if not m:
            continue

        link_text = m.group(1)
        url = m.group(2)
        description = m.group(3).strip()

        parts = link_text.split("/")
        vendor = parts[0]
        skill_path = "/".join(parts[1:])

        entries.append({
            "vendor": vendor,
            "skill_path": skill_path,
            "link_text": link_text,
            "url": url,
            "description": description,
            "section": current_section,
        })

    return entries


# ── URL resolution ───────────────────────────────────────────────────


def resolve_coords(url: str) -> tuple[str, str, str, str | None] | None:
    """Resolve any README URL to (org, repo, branch, path)."""
    parsed = urlparse(url)
    host = parsed.netloc.lower()
    path_str = parsed.path.strip("/")

    # Direct GitHub URLs
    if "github.com" in host:
        parts = path_str.split("/")
        if len(parts) >= 4 and parts[2] in ("tree", "blob"):
            org, repo, ref_type = parts[0], parts[1], parts[2]
            branch = parts[3]
            file_path = "/".join(parts[4:])
            if ref_type == "blob" and file_path.endswith("SKILL.md"):
                file_path = file_path[: -len("/SKILL.md")]
            return (org, repo, branch, file_path if file_path else None)
        elif len(parts) >= 2:
            return (parts[0], parts[1], "main", None)

    # officialskills.sh — need to scrape page
    if "officialskills.sh" in host:
        return resolve_officialskills(url)

    return None


# ── Skill directory finding ──────────────────────────────────────────


def find_skill_files(tree: list[str], skill_path: str) -> list[str]:
    """Find all files under skill_path in the tree."""
    if not skill_path:
        return list(tree)

    prefix = skill_path + "/"
    files = [p for p in tree if p.startswith(prefix)]

    if files:
        return files

    # Try case-insensitive
    prefix_lower = skill_path.lower() + "/"
    files = [p for p in tree if p.lower().startswith(prefix_lower)]
    return files


# ── Frontmatter ──────────────────────────────────────────────────────


def add_frontmatter(content: str, name: str, description: str,
                    category: str, vendor: str) -> str:
    existing: dict[str, str] = {}
    body = content

    if content.lstrip().startswith("---"):
        match = re.match(r"^---\s*\n(.*?)\n---\s*\n?(.*)", content, re.DOTALL)
        if match:
            fm_raw = match.group(1)
            body = match.group(2)
            for line in fm_raw.split("\n"):
                if ":" in line and not line.startswith(" ") and not line.startswith("-"):
                    k, v = line.split(":", 1)
                    k = k.strip().lower()
                    v = v.strip()
                    if k and v:
                        existing[k] = v

    lines = [
        f"name: {yaml_escape(name)}",
        f"description: {yaml_escape(description)}",
        f"category: {yaml_escape(category)}",
        f"vendor: {yaml_escape(vendor)}",
    ]
    for k, v in existing.items():
        if k not in ("name", "description", "category", "vendor"):
            lines.append(f"{k}: {v}")

    return "---\n" + "\n".join(lines) + "\n---\n\n" + body.lstrip("\n")


# ── Naming ───────────────────────────────────────────────────────────


def make_dir_name(vendor: str, skill_path: str) -> str:
    raw = f"{vendor}-{skill_path}".lower().replace("/", "-")
    raw = re.sub(r"[^a-z0-9_-]", "-", raw)
    raw = re.sub(r"-+", "-", raw)
    return f"dotagent-{raw}"


def make_fm_name(vendor: str, skill_path: str) -> str:
    return f"dotagent:{vendor}:{skill_path.replace('/', ':')}"


# ── Main logic ───────────────────────────────────────────────────────


def process_entry(entry: dict, idx: int, total: int):
    vendor = entry["vendor"]
    skill_path = entry["skill_path"]
    skill_name = skill_path.split("/")[-1] if skill_path else vendor
    dir_name = make_dir_name(vendor, skill_path)
    fm_name = make_fm_name(vendor, skill_path)
    category = VENDOR_CATEGORIES.get(vendor.lower(), "Developer Tools")
    description = entry["description"]

    coords = resolve_coords(entry["url"])
    if coords is None:
        _stats["skip"] += 1
        _failures.setdefault(vendor, []).append(f"{dir_name}: cannot resolve URL")
        return

    org, repo, branch, gh_path = coords

    tree = fetch_tree(org, repo, branch)
    if tree is None:
        _stats["fail"] += 1
        _failures.setdefault(vendor, []).append(f"{dir_name}: no tree {org}/{repo}")
        return

    # Find files
    files = find_skill_files(tree, gh_path or "")

    if not files and gh_path:
        # Fallback 1: search by skill name (last path component) as a dir with SKILL.md
        for p in tree:
            if p.endswith(f"/{skill_name}/SKILL.md"):
                gh_path = p[: -len("/SKILL.md")]
                files = find_skill_files(tree, gh_path)
                break

    if not files and gh_path:
        # Fallback 2: normalized match (ignore case, hyphens, underscores)
        norm_name = skill_name.lower().replace("-", "").replace("_", "")
        for p in tree:
            base = p.rsplit("/", 1)[-1] if "/" in p else p
            if base == "SKILL.md":
                dir_part = p.rsplit("/", 1)[0] if "/" in p else ""
                dir_base = dir_part.rsplit("/", 1)[-1] if "/" in dir_part else dir_part
                if dir_base.lower().replace("-", "").replace("_", "") == norm_name:
                    gh_path = dir_part
                    files = find_skill_files(tree, gh_path)
                    break

    if not files:
        _stats["fail"] += 1
        _failures.setdefault(vendor, []).append(
            f"{dir_name}: path '{gh_path}' not in {org}/{repo}")
        return

    # Download files
    out_dir = OUTPUT_DIR / dir_name
    out_dir.mkdir(parents=True, exist_ok=True)

    has_skill_md = False
    downloaded = 0
    prefix = (gh_path + "/") if gh_path else ""

    for file_path in files:
        rel = file_path[len(prefix):] if prefix else file_path
        if not rel:
            rel = "SKILL.md"

        raw_url = f"{RAW_BASE}/{org}/{repo}/{branch}/{file_path}"
        content = raw_get(raw_url)
        if content is None:
            continue
        if len(content) > MAX_FILE_SIZE:
            continue

        _stats["files"] += 1
        downloaded += 1

        if file_path.endswith("SKILL.md"):
            has_skill_md = True
            text = content.decode("utf-8", errors="replace")
            text = add_frontmatter(text, fm_name, description, category, vendor)
            (out_dir / "SKILL.md").write_text(text, encoding="utf-8")
        else:
            out_file = out_dir / rel
            out_file.parent.mkdir(parents=True, exist_ok=True)
            out_file.write_bytes(content)

    if not has_skill_md:
        stub = add_frontmatter(
            f"# {fm_name}\n\n*Skill content was not available at the source.*\n",
            fm_name, description, category, vendor)
        (out_dir / "SKILL.md").write_text(stub, encoding="utf-8")

    _stats["ok"] += 1
    if idx % 100 == 0 or idx == total:
        log(f"  [{idx}/{total}] processed ({_stats['ok']} ok, {_stats['fail']} fail)")


def main():
    global _page_cache, _tree_cache

    log("=" * 60)
    log("Official Skills Fetcher v2")
    log("=" * 60)

    if GITHUB_TOKEN:
        log("[info] GITHUB_TOKEN detected — authenticated mode")
    else:
        log("[warn] No GITHUB_TOKEN — rate limited to 60 API calls/h")

    log(f"[info] Output: {OUTPUT_DIR}")

    # Load persisted caches
    load_caches()

    # Parse README
    entries = parse_readme(README_PATH)
    log(f"[info] Parsed {len(entries)} official skill entries")
    if not entries:
        sys.exit(1)

    # Clean output
    log("[info] Cleaning previous output …")
    if OUTPUT_DIR.exists():
        for item in OUTPUT_DIR.iterdir():
            if item.is_dir() and item.name.startswith("dotagent-"):
                shutil.rmtree(item)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # Phase 1: Resolve all officialskills.sh URLs by scraping pages
    oss_entries = [e for e in entries if "officialskills.sh" in e["url"]]
    gh_entries = [e for e in entries if "github.com" in urlparse(e["url"]).netloc]
    other_entries = [e for e in entries if e not in oss_entries and e not in gh_entries]

    unresolved_oss = [e for e in oss_entries if e["url"] not in _page_cache]
    log(f"[info] {len(oss_entries)} officialskills.sh URLs "
        f"({len(unresolved_oss)} need scraping), "
        f"{len(gh_entries)} GitHub URLs")

    if unresolved_oss:
        log(f"[info] Phase 1: Resolving {len(unresolved_oss)} officialskills.sh URLs …")
        for i, entry in enumerate(unresolved_oss, 1):
            resolve_officialskills(entry["url"])
            if i % 100 == 0:
                log(f"  [{i}/{len(unresolved_oss)}] pages scraped")

        resolved = sum(1 for e in oss_entries if _page_cache.get(e["url"]))
        log(f"[info] Resolved {resolved}/{len(oss_entries)} officialskills.sh URLs")
        save_caches()

    # Phase 2: Fetch git trees
    all_coords = set()
    for entry in entries:
        coords = resolve_coords(entry["url"])
        if coords:
            all_coords.add((coords[0], coords[1], coords[2]))

    missing_trees = [(o, r, b) for (o, r, b) in all_coords
                     if f"{o.lower()}/{r.lower()}@{b}" not in _tree_cache]
    log(f"[info] Phase 2: {len(all_coords)} unique repos, {len(missing_trees)} need tree fetch")

    for i, (org, repo, branch) in enumerate(sorted(missing_trees), 1):
        tree = fetch_tree(org, repo, branch)
        count = len(tree) if tree else 0
        if count == 0:
            log(f"  [{i}/{len(missing_trees)}] {org}/{repo}@{branch} — FAILED")
        else:
            log(f"  [{i}/{len(missing_trees)}] {org}/{repo}@{branch} — {count} files")

    # Show all trees
    for org, repo, branch in sorted(all_coords):
        key = f"{org.lower()}/{repo.lower()}@{branch}"
        tree = _tree_cache.get(key)
        if tree:
            log(f"  [tree] {org}/{repo}@{branch} — {len(tree)} files")

    save_caches()

    # Phase 3: Process all entries
    total = len(entries)
    log(f"\n[info] Phase 3: Processing {total} skills …")

    # Use thread pool for parallel processing
    BATCH_SIZE = 20

    def safe_process(entry_idx):
        entry, idx = entry_idx
        try:
            process_entry(entry, idx, total)
        except Exception as exc:
            log(f"  [{idx}/{total}] ERROR: {exc}")
            _stats["fail"] += 1
            _failures.setdefault(entry["vendor"], []).append(
                f"{entry.get('link_text', '?')}: {exc}")

    with ThreadPoolExecutor(max_workers=BATCH_SIZE) as pool:
        list(pool.map(safe_process, [(e, i) for i, e in enumerate(entries, 1)]))

    # Summary
    log("\n" + "=" * 60)
    log("SUMMARY")
    log("=" * 60)
    log(f"  Total entries:   {total}")
    log(f"  Downloaded:      {_stats['ok']}")
    log(f"  Failed:          {_stats['fail']}")
    log(f"  Skipped:         {_stats['skip']}")
    log(f"  Files written:   {_stats['files']}")

    if _failures:
        log("\nFailures by vendor:")
        for vendor in sorted(_failures):
            log(f"  {vendor}: {len(_failures[vendor])} failure(s)")
            for f in _failures[vendor][:3]:
                log(f"    - {f}")
            if len(_failures[vendor]) > 3:
                log(f"    ... and {len(_failures[vendor]) - 3} more")

    log("")


if __name__ == "__main__":
    main()
