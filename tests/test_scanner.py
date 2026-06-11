import os
import pytest
from clean_turkish.core import load_guidelines
from clean_turkish.scanner import TurkishStyleScanner

@pytest.fixture
def scanner():
    # Path to workspace guidelines
    ref_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'guidelines'))
    guidelines_rules = load_guidelines(ref_dir)
    return TurkishStyleScanner(guidelines_rules)

def test_clean_text(scanner):
    clean_text = "Ürün geliştirmek zor. Teknolojiyi yönetebilirsiniz; insanları yönetmek ayrı bir iştir."
    issues = scanner.scan(clean_text)
    score = scanner.evaluate_style_score(issues)
    
    # Clean text should have high score
    assert len(issues) == 0
    assert score == 100

def test_bogaz_temizleme_and_siskinlik(scanner):
    dirty_text = "Şunu belirtmek gerekir ki, ürün geliştirmek oldukça zordur. Bunun teknolojiyle ilgili olduğu düşünülmektedir."
    issues = scanner.scan(dirty_text)
    score = scanner.evaluate_style_score(issues)
    
    # Should flag "Şunu belirtmek gerekir ki", "oldukça", and "-mektedir" pattern
    assert any(issue.matched_text == "Şunu belirtmek gerekir ki" for issue in issues)
    assert any(issue.matched_text == "oldukça" for issue in issues)
    assert any("düşünülmektedir" in issue.matched_text for issue in issues)
    assert score < 100

def test_jargon_and_plaza_speak(scanner):
    dirty_text = "Günümüzün rekabetçi ekosisteminde değer katmak ve fark yaratmak için hızla aksiyon almalı, align olup mindset'imizi güncellemeliyiz."
    issues = scanner.scan(dirty_text)
    
    # Should flag jargon like aksiyon almak, align olmak, mindset, ekosistem
    matched_words = [issue.matched_text.lower() for issue in issues]
    assert "aksiyon almalı" in matched_words or any("aksiyon" in w for w in matched_words)
    assert "align olup" in matched_words or any("align" in w for w in matched_words)
    assert "mindset'imizi" in matched_words or any("mindset" in w for w in matched_words)
    assert "ekosisteminde" in matched_words or any("ekosistem" in w for w in matched_words)

def test_dolgu_kaliplari(scanner):
    dirty_text = "Söz konusu proje bağlamında, ekipler arası uyum noktasında ciddi sorunlar yaşandığı görülmektedir."
    issues = scanner.scan(dirty_text)
    
    matched_words = [issue.matched_text.lower() for issue in issues]
    assert "söz konusu" in matched_words
    assert "bağlamında" in matched_words
    assert "noktasında" in matched_words
    assert any("görülmektedir" in w for w in matched_words)
