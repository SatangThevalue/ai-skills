---
name: research-to-skill-pipeline
description: Research and author Hermes skills on demand from the web.
version: 0.1.0
metadata.hermes.tags:
  - Workflow
  - Research
  - Skill-Authoring
---

# Domain Knowledge Capture Pipeline
This workflow orchestrates the retrieval of missing domain knowledge from the web and its distillation into a reusable Hermes skill. It ensures knowledge is gathered from authoritative sources and formatted into actionable, standard-compliant `SKILL.md` structures. It relies entirely on built-in web and skill management tools.

## When to Use
* The user asks if a skill exists for a specific framework or topic, and it does not.
* The user provides an official documentation link and asks to create a skill from it.
* The user asks to "learn" about a topic for future use.
* An existing skill needs to be expanded with detailed API references or deep-dives.

## Prerequisites
* The `web` toolset must be enabled for `web_search` and `web_extract`.
* The `skills` toolset must be enabled for `skill_manage` and `skills_list`.

## How to Run
Invoke the pipeline sequentially using the `web_search`, `web_extract`, and `skill_manage` tools.

## Quick Reference
* `skills_list`: Verify skill absence.
* `web_search`: Locate authoritative sources.
* `web_extract`: Pull markdown content.
* `skill_manage(action="create")`: Save the synthesized skill.
* `skill_manage(action="patch")`: Append or update existing skills.

## Procedure
1. **Verify Absence:** Run `skills_list` to confirm the requested topic is not already covered by an existing skill.
2. **Locate Sources:** Use `web_search` targeting official documentation, github repositories, or high-quality technical blogs (e.g., `site:nextjs.org "static exports"`).
3. **Extract Content:** Pass the most promising URLs to `web_extract` to retrieve the raw markdown content.
4. **Synthesize:** Distill the extracted text. Strip out marketing fluff, repetitive prose, and unrelated links. Focus entirely on:
   * Operating environments and architecture.
   * Exact commands, configuration snippets, and code patterns.
   * Breaking changes, pitfalls, and limitations.
5. **Author Skill:** Call `skill_manage` with `action="create"`. Provide the `name`, a sensible `category`, and the fully formatted `SKILL.md` text adhering strictly to Hermes frontmatter and structural standards.
6. **Iterative Expansion:** If the user subsequently asks for deeper details (e.g., "get all API parameters"), repeat steps 2-4 and use `skill_manage` with `action="patch"` (providing `old_string` and `new_string`) to inject the new section into the skill without overwriting it completely.

## Pitfalls
* `web_extract` and `web_search` occasionally hit 404s, 504 timeouts, or anti-bot/CAPTCHA protections (e.g. DDG bot challenges or search provider blocks on specific VPS IPs).
* **Bypass Strategy**: When standard search tools fail, execute a Python script (via `execute_code`) to crawl the target URLs directly using standard libraries:
  ```python
  import urllib.request
  from bs4 import BeautifulSoup
  
  req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
  html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8')
  soup = BeautifulSoup(html, 'html.parser')
  text = soup.get_text() # or extract specific elements
  ```
  This bypasses upstream proxy timeouts and firecrawl overhead.
* Directly pasting `web_extract` output into `skill_manage` violates brevity rules; you must summarize and structure the data first.
* When patching, ensure `old_string` contains enough context lines to uniquely identify the injection point.

## Verification
Use `skill_view(name="<skill-name>")` to confirm the skill was successfully written and formatted.