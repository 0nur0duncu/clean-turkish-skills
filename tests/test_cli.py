import os
import tempfile
import zipfile
import pytest
from click.testing import CliRunner
from clean_turkish.cli import main_cli

@pytest.fixture
def runner():
    return CliRunner()

@pytest.fixture
def workspace_dir():
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

def test_cli_lint(runner, workspace_dir):
    result = runner.invoke(main_cli, ['lint', '--source-directory', workspace_dir])
    assert result.exit_code == 0
    assert "Doğrulama Başarılı" in result.output

def test_cli_build(runner, workspace_dir):
    with tempfile.TemporaryDirectory() as tmpdir:
        output_skill = os.path.join(tmpdir, 'clean-turkish.skill')
        result = runner.invoke(main_cli, ['build', '--source-directory', workspace_dir, '--output-file', output_skill])
        assert result.exit_code == 0
        assert "başarıyla" in result.output
        assert os.path.exists(output_skill)
        
        # Verify zip contents
        with zipfile.ZipFile(output_skill, 'r') as zipf:
            namelist = zipf.namelist()
            assert 'SKILL.md' in namelist
            assert 'guidelines/expressions.md' in namelist
            assert 'guidelines/structures.md' in namelist
            assert 'guidelines/examples.md' in namelist

def test_cli_install(runner, workspace_dir):
    with tempfile.TemporaryDirectory() as tmpdir:
        target_path = os.path.join(tmpdir, 'target-skill')
        result = runner.invoke(main_cli, ['install', '--source-directory', workspace_dir, '--target-path', target_path])
        assert result.exit_code == 0
        assert "başarıyla kuruldu" in result.output
        
        # Verify files are copied
        assert os.path.exists(os.path.join(target_path, 'SKILL.md'))
        assert os.path.exists(os.path.join(target_path, 'guidelines', 'expressions.md'))

def test_cli_scan_file(runner, workspace_dir):
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create a clean file
        clean_file = os.path.join(tmpdir, 'clean.txt')
        with open(clean_file, 'w', encoding='utf-8') as f:
            f.write("Hız, kalite, maliyet: ikisini seçin.")
            
        result = runner.invoke(main_cli, ['scan', clean_file, '--source-directory', workspace_dir])
        assert result.exit_code == 0
        assert "Skor: 100/100" in result.output
        
        # Create a dirty file
        dirty_file = os.path.join(tmpdir, 'dirty.txt')
        with open(dirty_file, 'w', encoding='utf-8') as f:
            f.write(
                "Şunu belirtmek gerekir ki, ürün geliştirmek oldukça zordur. "
                "Söz konusu proje bağlamında, ekipler arası uyum noktasında ciddi sorunlar yaşandığı görülmektedir. "
                "Günümüzün rekabetçi ekosisteminde değer katmak ve fark yaratmak için hızla aksiyon almalı, "
                "align olup mindset'imizi güncellemeliyiz. "
                "Bu yazıda liderliğin neden zor olduğunu adım adım ele alacağız. "
                "Sonuçları son derece önemlidir."
            )
            
        result = runner.invoke(main_cli, ['scan', dirty_file, '--source-directory', workspace_dir])
        # Should exit with non-zero code since score < 50
        assert result.exit_code != 0
        assert "Skor:" in result.output
        assert "söz konusu" in result.output.lower()
