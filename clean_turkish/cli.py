import os
import sys
import zipfile
import shutil
import click
from rich.console import Console
from rich.panel import Panel
from clean_turkish.core import parse_skill_md, load_guidelines
from clean_turkish.scanner import TurkishStyleScanner

# Reconfigure stdout/stderr on Windows to use UTF-8, avoiding Turkish character rendering crashes
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except AttributeError:
        pass

console = Console()

@click.group()
@click.version_option(package_name="clean-turkish")
def main_cli():
    """Clean Turkish - Türkçe Yapay Zeka Yazım Kalıbı Temizleme CLI Aracı."""
    pass

@main_cli.command(name='build')
@click.option('--output-file', '-o', default='clean-turkish.skill', help='Oluşturulacak .skill dosyasının adı.')
@click.option('--source-directory', '-s', default='.', help='Kaynak dizin (SKILL.md ve guidelines dizininin olduğu yer).')
def build_skill(output_file, source_directory):
    """SKILL.md ve guidelines dizinini clean-turkish.skill dosyasına paketler."""
    source_dir = os.path.abspath(source_directory)
    skill_md = os.path.join(source_dir, 'SKILL.md')
    guidelines_dir = os.path.join(source_dir, 'guidelines')
    
    if not os.path.exists(skill_md):
        console.print(f"[bold red]Hata:[/bold red] {skill_md} dosyası bulunamadı. Lütfen doğru kaynak dizinini belirtin.")
        sys.exit(1)
        
    try:
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Add SKILL.md
            zipf.write(skill_md, 'SKILL.md')
            # Add guidelines/
            if os.path.exists(guidelines_dir):
                for root, dirs, files in os.walk(guidelines_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, source_dir)
                        zipf.write(file_path, arcname)
            
        console.print(f"[bold green]Başarılı:[/bold green] Skill başarıyla '{output_file}' olarak paketlendi.")
    except Exception as e:
        console.print(f"[bold red]Hata:[/bold red] Skill paketlenirken sorun oluştu: {e}")
        sys.exit(1)

@main_cli.command(name='install')
@click.option('--global/--local', 'is_global_install', default=True, help='Skill\'i global (~/.claude/skills) ya da lokal (.claude/skills) dizine kurar.')
@click.option('--target-path', '-p', type=click.Path(), help='Özel hedef kurulum dizini.')
@click.option('--source-directory', '-s', default='.', help='Kaynak dizin.')
def install_skill(is_global_install, target_path, source_directory):
    """Clean Turkish skill'ini Claude Code dizinine kurar."""
    source_dir = os.path.abspath(source_directory)
    skill_md = os.path.join(source_dir, 'SKILL.md')
    guidelines_dir = os.path.join(source_dir, 'guidelines')
    
    if not os.path.exists(skill_md):
        console.print(f"[bold red]Hata:[/bold red] Kurulum için {skill_md} dosyası bulunamadı.")
        sys.exit(1)
        
    # Determine target directory
    if target_path:
        target_dir = os.path.abspath(target_path)
    elif is_global_install:
        target_dir = os.path.join(os.path.expanduser('~'), '.claude', 'skills', 'clean-turkish')
    else:
        target_dir = os.path.abspath(os.path.join('.claude', 'skills', 'clean-turkish'))
        
    try:
        os.makedirs(target_dir, exist_ok=True)
        # Copy SKILL.md
        shutil.copy2(skill_md, os.path.join(target_dir, 'SKILL.md'))
        
        # Copy guidelines directory
        dest_guidelines = os.path.join(target_dir, 'guidelines')
        if os.path.exists(dest_guidelines):
            shutil.rmtree(dest_guidelines)
        if os.path.exists(guidelines_dir):
            shutil.copytree(guidelines_dir, dest_guidelines)
            
        console.print(f"[bold green]Başarılı:[/bold green] Skill '{target_dir}' konumuna başarıyla kuruldu.")
    except Exception as e:
        console.print(f"[bold red]Hata:[/bold red] Kurulum sırasında hata oluştu: {e}")
        sys.exit(1)

@main_cli.command(name='lint')
@click.option('--source-directory', '-s', default='.', help='Kaynak dizin.')
def lint_guidelines(source_directory):
    """Skill dosyalarının yapısını ve içeriğini doğrular (lint)."""
    source_dir = os.path.abspath(source_directory)
    skill_md = os.path.join(source_dir, 'SKILL.md')
    guidelines_dir = os.path.join(source_dir, 'guidelines')
    errors = 0
    warnings = 0
    
    console.print("[bold cyan]Skill dosyaları doğrulanıyor...[/bold cyan]\n")
    
    # Check SKILL.md
    if not os.path.exists(skill_md):
        console.print("[bold red][HATA][/bold red] SKILL.md dosyası bulunamadı.")
        errors += 1
    else:
        try:
            metadata, _ = parse_skill_md(skill_md)
            console.print(f"[bold green][OK][/bold green] SKILL.md YAML ön bilgileri (frontmatter) geçerli.")
            console.print(f"   Ad: {metadata.name}")
            console.print(f"   Açıklama: {metadata.description}")
            console.print(f"   Yazar: {metadata.author}")
            console.print(f"   Dil: {metadata.language}")
            
            # Check mandatory metadata
            if not metadata.name:
                console.print("[bold red][HATA][/bold red] SKILL.md ön bilgilerinde 'name' eksik.")
                errors += 1
            if not metadata.description:
                console.print("[bold yellow][UYARI][/bold yellow] SKILL.md ön bilgilerinde 'description' eksik.")
                warnings += 1
        except Exception as e:
            console.print(f"[bold red][HATA][/bold red] SKILL.md okunurken hata: {e}")
            errors += 1
            
    # Check guidelines files
    required_files = ['expressions.md', 'structures.md', 'examples.md']
    if not os.path.exists(guidelines_dir):
        console.print("[bold red][HATA][/bold red] 'guidelines' dizini bulunamadı.")
        errors += 1
    else:
        for req_file in required_files:
            file_path = os.path.join(guidelines_dir, req_file)
            if not os.path.exists(file_path):
                console.print(f"[bold red][HATA][/bold red] Kılavuz dosyası eksik: guidelines/{req_file}")
                errors += 1
            else:
                console.print(f"[bold green][OK][/bold green] Kılavuz dosyası mevcut: guidelines/{req_file}")
                
    if errors > 0:
        console.print(f"\n[bold red]Doğrulama Başarısız:[/bold red] {errors} hata, {warnings} uyarı saptandı.")
        sys.exit(1)
    else:
        console.print(f"\n[bold green]Doğrulama Başarılı:[/bold green] Skill yapısı düzgün ({warnings} uyarı).")

@main_cli.command(name='scan')
@click.argument('input_file', type=click.Path(exists=True), required=False)
@click.option('--source-directory', '-s', default='.', help='Skill dosyalarının bulunduğu kaynak dizin.')
def scan_text(input_file, source_directory):
    """Bir dosyayı veya standart girdiyi (stdin) yapay zeka yazım kalıplarına karşı tarar."""
    source_dir = os.path.abspath(source_directory)
    guidelines_dir = os.path.join(source_dir, 'guidelines')
    
    if not os.path.exists(guidelines_dir):
        console.print(f"[bold red]Hata:[/bold red] Kılavuz dizini {guidelines_dir} bulunamadı.")
        sys.exit(1)
        
    # Read input text
    if input_file:
        try:
            with open(input_file, 'r', encoding='utf-8') as f:
                text = f.read()
        except Exception as e:
            console.print(f"[bold red]Hata:[/bold red] Dosya okunurken sorun oluştu: {e}")
            sys.exit(1)
    else:
        # Read from stdin
        if sys.stdin.isatty():
            console.print("[bold yellow]İpucu:[/bold yellow] Dosya belirtilmedi. Lütfen taranacak metni yapıştırıp Enter'a basın (Bitirmek için Ctrl+D veya Ctrl+Z ve ardından Enter yapın):")
        text = sys.stdin.read()
        
    if not text.strip():
        console.print("[bold yellow]Uyarı:[/bold yellow] Taranacak metin boş.")
        sys.exit(0)
        
    try:
        style_rules = load_guidelines(guidelines_dir)
        style_scanner = TurkishStyleScanner(style_rules)
        detected_issues = style_scanner.scan(text)
        style_score = style_scanner.evaluate_style_score(detected_issues)
        
        style_scanner.generate_terminal_report(text, detected_issues, style_score)
        
        # Return exit code 1 if score is too low (<50) to make it CLI friendly (CI integrations)
        if style_score < 50:
            sys.exit(1)
        else:
            sys.exit(0)
            
    except Exception as e:
        console.print(f"[bold red]Hata:[/bold red] Tarama sırasında hata oluştu: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main_cli()
