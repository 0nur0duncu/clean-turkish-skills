import re
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

class StyleIssue:
    def __init__(self, start, end, matched_text, category, replacement=None, description=None):
        self.start = start
        self.end = end
        self.matched_text = matched_text
        self.category = category
        self.replacement = replacement
        self.description = description

class TurkishStyleScanner:
    def __init__(self, guidelines):
        self.guidelines = guidelines
        self._compile_patterns()

    def _compile_patterns(self):
        self.patterns = []
        
        def make_verb_flexible(word):
            # Common Turkish verbs in our rules
            verbs = {
                'almak': r'al\w*',
                'vermek': r'ver\w*',
                'etmek': r'et\w*',
                'yapmak': r'yap\w*',
                'olmak': r'ol\w*',
                'yaratmak': r'yarat\w*',
                'katmak': r'kat\w*',
                'geçirmek': r'geçir\w*',
                'görmek': r'gör\w*',
                'gelmek': r'gel\w*'
            }
            for inf, reg in verbs.items():
                if word.lower() == inf:
                    return reg
            return re.escape(word)

        def placeholder_to_regex(pattern_str):
            pattern_str = pattern_str.strip()
            
            # Check for leading/trailing wildcards and strip them
            is_leading = pattern_str.startswith('...')
            is_trailing = pattern_str.endswith('...')
            
            clean_pat = pattern_str
            if is_leading:
                clean_pat = clean_pat[3:].lstrip()
            if is_trailing:
                clean_pat = clean_pat[:-3].rstrip()
                
            parts = clean_pat.split('...')
            regex_parts = []
            
            for part in parts:
                part = part.strip()
                if not part:
                    continue
                    
                sub_tokens = re.split(r'(\b[XYZ]\b)', part)
                sub_regex = []
                for st in sub_tokens:
                    if st in ('X', 'Y', 'Z'):
                        # Match 1 to 3 words for placeholders
                        sub_regex.append(r'\w+(?:\s+\w+){0,2}')
                    else:
                        words = st.strip().split()
                        word_regexes = []
                        for w in words:
                            # Strip punctuation for verb checking
                            clean_w = re.sub(r'[^\w\s]', '', w)
                            flex_w = make_verb_flexible(clean_w)
                            if flex_w != re.escape(clean_w):
                                word_regexes.append(flex_w)
                            else:
                                esc = re.escape(w)
                                esc = esc.replace(r'\:', r'\s*\:')
                                esc = esc.replace(r'\,', r'\s*\,')
                                esc = esc.replace(r'\.', r'\s*\.')
                                word_regexes.append(esc)
                        sub_regex.append(r'\s+'.join(word_regexes))
                
                regex_parts.append(r'\s+'.join([sr for sr in sub_regex if sr]))
                
            main_regex = r'\s+(?:\S+\s+){0,4}'.join(regex_parts)
            
            # If the clean pattern is a single plain word (letters only),
            # append \w* to allow matching Turkish grammatical suffixes.
            is_single_word = re.match(r'^[a-zA-ZçğıöşüÇĞİÖŞÜ\-\']+$', clean_pat)
            if is_single_word:
                main_regex = main_regex + r'\w*'
            
            return re.compile(rf'(?<!\w){main_regex}(?!\w)', re.IGNORECASE)

        # 1. Suffix pattern for -mektedir/-maktadır
        self.patterns.append({
            'regex': re.compile(r'\b\w+(?:mek|mak)tedir(?:ler)?\b', re.IGNORECASE),
            'category': 'Resmi Şişkinlik Ekleri',
            'replacement': 'sade zaman (yapıyor/yapar)',
            'description': 'Bürokratik ek. Sade şimdiki zaman veya geniş zaman kullanın.'
        })

        # 2. Add all specific replacements
        for forbidden_term, suggested_term in self.guidelines.get('replacement_rules', {}).items():
            category = 'Plaza / Karışık Jargon' if any(j in forbidden_term for j in (
                'aksiyon', 'feedback', 'mindset', 'deep dive', 
                'değer kat', 'fark yarat', 'align', 'set et', 
                'challenge', 'revize', 'hayata geçir', 'sinerji', 
                'ekosistem', 'perspektif', 'domain', 'case', 'asap'
            )) else 'İfade/Kalıp Düzeltme'
            
            self.patterns.append({
                'regex': placeholder_to_regex(forbidden_term),
                'category': category,
                'replacement': suggested_term,
                'description': f"Kaçının, yerine '{suggested_term}' kullanmayı deneyin."
            })

        # 3. Add forbidden expressions
        for expression in self.guidelines.get('forbidden_expressions', []):
            if expression in self.guidelines.get('replacement_rules', {}):
                continue
                
            category = 'Boğaz Temizleme / Dolgu'
            if expression in ('aslında', 'gerçekten', 'kesinlikle', 'oldukça', 'son derece', 'adeta', 'resmen', 'tam anlamıyla'):
                category = 'Zarf (Dolgu Kelime)'
                
            self.patterns.append({
                'regex': placeholder_to_regex(expression),
                'category': category,
                'replacement': 'Silin veya sadeleştirin',
                'description': 'Anlamı şişiren gereksiz dolgu veya açılış.'
            })

        # 4. Add structural patterns
        for struct_pattern, desc in self.guidelines.get('structural_patterns', {}).items():
            if struct_pattern in self.guidelines.get('replacement_rules', {}):
                continue
            self.patterns.append({
                'regex': placeholder_to_regex(struct_pattern),
                'category': 'Kaçınılacak Yapı',
                'replacement': 'Doğrudan/Etken söyleyin',
                'description': desc
            })

    def scan(self, text):
        """Scans the text, returns a list of non-overlapping StyleIssues."""
        issues = []
        for pattern in self.patterns:
            for match_obj in pattern['regex'].finditer(text):
                issues.append(StyleIssue(
                    start=match_obj.start(),
                    end=match_obj.end(),
                    matched_text=match_obj.group(),
                    category=pattern['category'],
                    replacement=pattern['replacement'],
                    description=pattern['description']
                ))

        # Sort matches by start position and resolve overlaps (keep the longer match)
        issues.sort(key=lambda x: (x.start, -(x.end - x.start)))
        
        resolved_issues = []
        last_end = -1
        for issue in issues:
            if issue.start >= last_end:
                resolved_issues.append(issue)
                last_end = issue.end
                
        return resolved_issues

    def evaluate_style_score(self, issues):
        """Calculates a style score out of 100 based on issues found."""
        score = 100
        deductions = {
            'Boğaz Temizleme / Dolgu': 6,
            'Zarf (Dolgu Kelime)': 3,
            'Resmi Şişkinlik Ekleri': 5,
            'Plaza / Karışık Jargon': 6,
            'İfade/Kalıp Düzeltme': 4,
            'Kaçınılacak Yapı': 5
        }
        
        for issue in issues:
            deduction_points = deductions.get(issue.category, 4)
            score -= deduction_points
            
        return max(0, score)

    def generate_terminal_report(self, text, issues, score):
        """Prints a rich terminal report of the scan results."""
        console = Console()
        
        # Build highlighted text
        highlighted_parts = []
        last_idx = 0
        for issue in issues:
            highlighted_parts.append(text[last_idx:issue.start])
            highlighted_parts.append(f"[bold red]{text[issue.start:issue.end]}[/bold red]")
            last_idx = issue.end
        highlighted_parts.append(text[last_idx:])
        
        highlighted_text = "".join(highlighted_parts)
        
        console.print("\n[bold cyan]Scan Results & Highlights[/bold cyan]")
        console.print("-" * 50)
        console.print(Panel(highlighted_text, title="Highlighted Text"))
        
        # Score Panel
        color = "green" if score >= 70 else "yellow" if score >= 50 else "red"
        status = "BAŞARILI (Temiz)" if score >= 70 else "ORTA (Gözden geçirin)" if score >= 50 else "YAPAY ZEKA (Yeniden Yazın)"
        console.print(Panel(
            f"[bold {color}]Skor: {score}/100[/bold {color}] - [bold]{status}[/bold]\n"
            f"Toplam Bulgular: {len(issues)} adet yapay zeka yazım kalıbı veya dolgu saptandı.",
            title="Değerlendirme Raporu",
            border_style=color
        ))
        
        if issues:
            table = Table(title="Saptanan Kalıplar ve Öneriler")
            table.add_column("Konum", justify="center", style="cyan")
            table.add_column("Eşleşen İfade", style="bold red")
            table.add_column("Kategori", style="magenta")
            table.add_column("Öneri / Açıklama", style="green")
            
            for i, issue in enumerate(issues, 1):
                table.add_row(
                    f"#{i}",
                    issue.matched_text,
                    issue.category,
                    issue.replacement if issue.replacement else issue.description
                )
            console.print(table)
        else:
            console.print("[bold green]Tebrikler! Metinde yapay zeka yazım kalıbına veya dolguya rastlanmadı.[/bold green]\n")
