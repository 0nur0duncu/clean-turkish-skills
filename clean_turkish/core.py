import os
import re
import yaml

class SkillMetadata:
    def __init__(self, name, description, trigger=None, author=None, language=None):
        self.name = name
        self.description = description
        self.trigger = trigger
        self.author = author
        self.language = language

def parse_skill_md(skill_md_path):
    """Parses frontmatter of SKILL.md and returns metadata and content."""
    if not os.path.exists(skill_md_path):
        raise FileNotFoundError(f"SKILL.md not found at {skill_md_path}")
        
    with open(skill_md_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Extract YAML frontmatter between ---
    frontmatter_match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not frontmatter_match:
        raise ValueError("SKILL.md is missing valid YAML frontmatter")
        
    yaml_data = yaml.safe_load(frontmatter_match.group(1))
    
    metadata = SkillMetadata(
        name=yaml_data.get('name'),
        description=yaml_data.get('description'),
        trigger=yaml_data.get('metadata', {}).get('trigger'),
        author=yaml_data.get('metadata', {}).get('author'),
        language=yaml_data.get('metadata', {}).get('language')
    )
    
    return metadata, content[frontmatter_match.end():]

def parse_expression_list(file_path):
    """Extracts phrases listed as bullet points (usually quoted) from a markdown file."""
    phrases = []
    if not os.path.exists(file_path):
        return phrases
        
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Match - "phrase" or - 'phrase' or - phrase
            match = re.match(r'^\s*-\s*["\']([^"\']+)["\']', line)
            if match:
                phrases.append(match.group(1).strip())
            else:
                match_plain = re.match(r'^\s*-\s*([^"\'\s].*)$', line)
                if match_plain:
                    # Ignore list items that are comments or explanations
                    val = match_plain.group(1).strip()
                    if not val.startswith(('Bunun yerine:', 'Not:', 'Bir cümle')):
                        phrases.append(val)
    return phrases

def parse_replacement_table(file_path):
    """Extracts replacements from markdown tables."""
    replacement_rules = {}
    if not os.path.exists(file_path):
        return replacement_rules
        
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line.startswith('|'):
                continue
            # Split and clean columns
            cols = [col.strip() for col in line.split('|')[1:-1]]
            if len(cols) < 2:
                continue
            # Skip header or separator
            if all(c == '-' or c == ':' or not c for c in cols[0]) or cols[0].lower() in ('kaçının', 'şişkin', 'dolgu', 'kalıp', 'boyut'):
                continue
            
            # Remove backticks or quotes if any
            key = cols[0].strip('"`\'')
            # Strip parenthetical notes like (mecazi) or (toplantı)
            key = re.sub(r'\s*\([^)]*\)', '', key).strip('"`\'')
            val = cols[1]
            if key:
                replacement_rules[key] = val
    return replacement_rules

def load_guidelines(guidelines_dir):
    """Loads all forbidden expressions, replacement rules, and structural warnings from guidelines."""
    guidelines = {
        'forbidden_expressions': [],
        'replacement_rules': {},
        'structural_patterns': {}
    }
    
    if not os.path.exists(guidelines_dir):
        return guidelines
        
    expressions_path = os.path.join(guidelines_dir, 'expressions.md')
    structures_path = os.path.join(guidelines_dir, 'structures.md')
    
    # Load forbidden expressions from list structures
    guidelines['forbidden_expressions'].extend(parse_expression_list(expressions_path))
    
    # Load replacement rules from tables
    guidelines['replacement_rules'].update(parse_replacement_table(expressions_path))
    guidelines['replacement_rules'].update(parse_replacement_table(structures_path))
    
    # Load structural patterns separately
    if os.path.exists(structures_path):
        # We can extract rows of the tables in structures.md as structural warnings
        with open(structures_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line.startswith('|'):
                    continue
                cols = [col.strip() for col in line.split('|')[1:-1]]
                if len(cols) < 2:
                    continue
                if all(c == '-' or c == ':' or not c for c in cols[0]) or cols[0].lower() in ('kalıp', 'şişkin', 'dolgu', 'kaçının'):
                    continue
                key = cols[0].strip('"`\'')
                # Strip parenthetical notes
                key = re.sub(r'\s*\([^)]*\)', '', key).strip('"`\'')
                val = cols[1]
                guidelines['structural_patterns'][key] = val
                
    return guidelines
