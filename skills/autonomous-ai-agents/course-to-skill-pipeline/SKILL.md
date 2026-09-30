---
name: course-to-skill-pipeline
description: Convert course syllabi into actionable skills with rubrics.
version: 0.1.0
metadata:
  hermes:
    tags: [Education, Curriculum, Skill-Authoring, SOP]
---

# Course to Skill Pipeline

Extracts course syllabi, tutorial curricula, and repository roadmaps to synthesize standardized Hermes skills with actionable SOPs and evaluation rubrics. It transforms theoretical lectures into executable commands and code checks, omitting passive video viewing or academic essay grading. Relies on Python standard library and Hermes built-in tools.

## When to Use
- "ดึงความรู้จาก Udemy มาสร้างเป็นสกิล"
- "แกะโครงสร้างคอร์สออนไลน์เป็น SOP และขั้นตอนทำงาน"
- Converting educational course outlines or workshop curricula into agent procedures.
- Synthesizing repository roadmaps into standardized execution skills with testable rubrics.

## Prerequisites
- `web_extract` and `web_search` available for syllabus retrieval.
- `skill_manage` tool enabled for saving and patching skills.
- Target skill category determined within `~/.hermes/skills/<category>/`.

## How to Run
Retrieve course outlines with `web_extract` or `read_file`. Synthesize the roadmap and rubrics into a standardized `SKILL.md` using `skill_manage(action="create")`. Verify deployment with `skill_view`.

## Quick Reference
```bash
python3 ~/.hermes/skills/hermes-agent/multi-profile-skills-sync/scripts/sync_skills_index.py
rsync -av --delete ~/.hermes/skills/ ~/ai-skills/skills/
cd ~/ai-skills && git add . && git commit -m "feat(skills): add <skill-name>" && git push origin main
```

## Procedure

1. **Extract Course Structure**
   Fetch curriculum data, module titles, and lecture descriptions using `web_extract` or inspect local markdown/JSON outlines with `read_file`.

2. **Deconstruct Knowledge Architecture**
   Break the curriculum into four operational layers:
   - **Learning Roadmap**: Progression phases (Foundations -> Implementation -> Production).
   - **Actionable SOP**: Step-by-step terminal commands, function signatures, and exact configuration blocks.
   - **Artifact Specification**: Concrete deliverable produced (script, service daemon, database table).
   - **Evaluation Rubrics**: Quantitative benchmarks, expected output formats, and error boundaries.

3. **Filter and Synthesize Content**
   Strip out theoretical introductions, personal anecdotes, marketing pitches, and passive quizzes. Retain only copy-paste-exact procedures, reproducible code snippets, and operational pitfalls.

4. **Author Standardized Skill**
   Call `skill_manage` with `action="create"` providing the lowercase-hyphenated name, target category, and standard frontmatter. Ensure the body adheres to the mandatory 8-section layout.

5. **Sync to Profile Network and Repository**
   Ensure all secondary profiles reflect the newly added skill by maintaining profile symlinks:
   ```bash
   [ -L ~/.hermes/profiles/<profile>/skills ] || ln -s /home/thaieasyvps/.hermes/skills ~/.hermes/profiles/<profile>/skills
   ```
   Re-index the catalog and commit changes to the Git repository via the `terminal` tool:
   ```bash
   python3 ~/.hermes/skills/hermes-agent/multi-profile-skills-sync/scripts/sync_skills_index.py
   rsync -av --delete ~/.hermes/skills/ ~/ai-skills/skills/
   cd ~/ai-skills && git add . && git commit -m "feat(skills): sync new course skill" && git push origin main
   ```

## Pitfalls
- **Academic Fluff**: Retaining passive discussion questions instead of executable tool checks violates the agent operational model. Every procedure must produce a verifiable artifact.
- **Missing Verifications**: A skill without an automated test command or exit code check cannot be validated by autonomous agents.
- **Unlinked Secondary Profiles**: When creating new profiles with `hermes profile create --clone`, the skills directory is copied rather than symlinked, causing skill drift.

## Verification
Confirm the skill exists in the library and passes frontmatter parsing:
```bash
grep -q "Convert course syllabi" ~/.hermes/skills/autonomous-ai-agents/course-to-skill-pipeline/SKILL.md && echo "SUCCESS: Skill loaded"
```
