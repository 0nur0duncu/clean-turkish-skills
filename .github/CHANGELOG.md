# Changelog — Clean Turkish

## 2026-06-11 — Sürüm v1.1.0 (Profesyonel Geliştirici Sürümü)

### Eklenenler

- **Python CLI Aracı (`clean-tr`)**: Projeyi yönetmek ve entegrasyonlar için geliştirilmiş komut satırı aracı.
  - `clean-tr lint`: Guidelines dosyalarının yapısını ve geçerliliğini doğrular.
  - `clean-tr build`: `SKILL.md` ve guidelines dizinini `clean-turkish.skill` zip arşivine otomatik paketler.
  - `clean-tr install`: Claude Code yerel veya global skill klasörlerine kolay kurulum sağlar.
  - `clean-tr scan`: Dosyaları veya standart girdiyi yerel olarak Türkçe yapay zeka kalıplarına karşı analiz eder.
- **Yerel Metin Tarayıcı (Scanner Engine)**:
  - Türkçe çekim eklerini algılayabilen esnek kelime tespiti (örneğin: `aksiyon almak` kuralının `aksiyon almalı` varyasyonlarını yakalaması).
  - Türkçe isim çekim eklerini (`-inde`, `-ler`) destekleyen akıllı tekil kelime eşleştirme (`ekosistem` -> `ekosisteminde` eşleşmesi).
  - Bounded wildcards ve non-greedy parser ile çakışan veya fazla genişleyen regex eşleşmelerini engelleme.
  - 100 üzerinden yerel skorlama ve ANSI/Rich terminal renklendirmeli detaylı hata & öneri raporlaması.
- **Geliştirici Altyapısı**:
  - `pyproject.toml` ile modern paket yönetimi (`uv` uyumlu).
  - `pytest` tabanlı test paketi (`tests/` dizini altında CLI ve Scanner birim testleri).
  - GitHub Actions CI/CD ve Otomatik Release paketleme entegrasyonu (`.github/workflows/`).

## 2026-05-30

### İlk sürüm

Açık kaynak "Stop Slop" skill'inin Türkçe uyarlaması. Çeviri değil; Türkçeye özgü yapay zeka yazım kalıpları için yeniden tasarlandı.

**Hedef üslup:** Resmi-temiz / siz dili. Saygı tonu korunur, bürokratik şişkinlik atılır.

**Türkçeye özgü eklenenler**

- Resmi şişkinlik ekleri: `-mektedir/-maktadır`, `-dir` ek-fiili (önemlidir, gereklidir), aşırı edilgen (yapılmaktadır, görülmektedir)
- Dolgu isim ve kalıplar: söz konusu, bağlamında, noktasında, açısından, itibariyle, nezdinde
- Türkçe açılış ve meta kalıpları: "Gelin... bakalım", "Peki ya...?", "Bu yazıda ele alacağız", "Düşünün:", "Unutmayın:"
- Plaza/karışık jargon: aksiyon almak, feedback vermek, mindset, deep dive, değer katmak, align olmak
- Türkçe zarf listesi: aslında, gerçekten, kesinlikle, oldukça, adeta, resmen, tam anlamıyla

**Uyarlanan veya kaldırılan İngilizce kurallar**

- "Wh- ile başlama yasağı" kaldırıldı (Türkçe SOV ve serbest dizimli); yerine Türkçe açılış takıntıları kondu
- "-ly zarf" tespiti Türkçe zarf morfolojisiyle değiştirildi
- "Hiç em dash yok" kuralı yumuşatıldı: diyalogda meşru, dramatik vurguda yasak
- `-dir` ek-fiili tanım ve genelgeçer olgularda serbest bırakıldı

**Dosyalar:** SKILL.md, guidelines/expressions.md, guidelines/structures.md, guidelines/examples.md
