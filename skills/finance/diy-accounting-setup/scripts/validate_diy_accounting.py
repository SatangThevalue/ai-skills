import os
import re

def validate_skill_structure(skill_path):
    print(f"Validating SKILL.md at {skill_path}...")
    if not os.path.exists(skill_path):
        print(f"Error: {skill_path} not found.")
        return False
        
    with open(skill_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check frontmatter
    if not content.startswith("---"):
        print("Error: SKILL.md must start with '---'")
        return False
        
    end_fm = content.find("---", 3)
    if end_fm == -1:
        print("Error: Frontmatter closing '---' not found.")
        return False
        
    frontmatter = content[3:end_fm]
    
    # Simple check for name and description in frontmatter
    if "name:" not in frontmatter:
        print("Error: 'name:' field is missing in frontmatter.")
        return False
        
    if "description:" not in frontmatter:
        print("Error: 'description:' field is missing in frontmatter.")
        return False
        
    # Check headers
    required_headers = [
        r"^#\s+", 
        r"^##\s+1\.\s+วัตถุประสงค์",
        r"^##\s+2\.\s+ขั้นตอน",
        r"^##\s+3\.\s+Common Pitfalls",
        r"^##\s+4\.\s+Verification Checklist"
    ]
    
    for header in required_headers:
        if not re.search(header, content, re.MULTILINE):
            print(f"Warning: Expected header match '{header}' was not found in content.")
            
    print("SKILL.md validation completed successfully.")
    return True

if __name__ == "__main__":
    skill_file = "/home/thaieasyvps/.hermes/skills/finance/diy-accounting-setup/SKILL.md"
    validate_skill_structure(skill_file)
