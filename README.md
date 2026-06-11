# Clean Turkish

Türkçe metinlerden yapay zeka yazım kalıplarını temizleyen bir skill ve geliştirici aracı.

## Bu nedir?

Yapay zeka metinlerinin kalıpları vardır: öngörülebilir ifadeler, bürokratik ekler, dolgu kelimeler, gizlenen özne. Bu skill, Claude'a (veya herhangi bir LLM'e) bu kalıpları **Türkçede** yakalayıp temizlemeyi öğretir.

Bu, açık kaynak [Stop Slop](https://github.com/hardikpandya/stop-slop) skill'inin (MIT) Türkçe uyarlamasıdır. Çeviri değil, yeniden tasarım: İngilizcedeki AI belirtilerinin çoğu (em dash, "-ly" zarfları, Wh- ile başlama) Türkçeye oturmaz. Türkçenin kendi kalıpları vardır — `-mektedir/-maktadır` ekleri, gereksiz `-dir` ek-fiili, "söz konusu / bağlamında / noktasında" dolguları, "Gelin yakından bakalım" açılışları.

## Örnek

**Öncesi:**

> "Söz konusu proje bağlamında, ekipler arası uyum noktasında ciddi sorunlar yaşandığı görülmektedir."

**Sonrası:**

> "Bu projede ekipler birbiriyle anlaşamıyor."

Daha fazla öncesi/sonrası dönüşüm için: [guidelines/examples.md](guidelines/examples.md).

## Yapı

```
clean-turkish/
├── SKILL.md              # Çekirdek talimatlar
├── guidelines/
│   ├── expressions.md    # Atılacak kelime ve kalıplar
│   ├── structures.md     # Kaçınılacak yapısal kalıplar
│   └── examples.md       # Öncesi/sonrası dönüşümler
├── README.md
├── CHANGELOG.md
└── LICENSE
```

## Hızlı başlangıç

### Yöntem 1 — `.skill` dosyasıyla (önerilen)

[Releases](https://github.com/0nur0duncu/clean-turkish-skills/releases) sayfasından `clean-turkish.skill` dosyasını indirin. `.skill` dosyaları sıradan bir zip arşividir; Claude Code'un skills klasörüne açmanız yeterli:

**Mac / Linux:**

```bold
unzip clean-turkish.skill -d ~/.claude/skills/clean-turkish
```

**Windows (PowerShell):**

```powershell
Expand-Archive clean-turkish.skill -DestinationPath "$env:USERPROFILE\.claude\skills\clean-turkish"
```

Yalnızca tek bir projede kullanmak için `~/.claude/skills/` yerine o projedeki `.claude/skills/` altına açın.

### Yöntem 2 — Git ile klonlayın

```bash
git clone https://github.com/0nur0duncu/clean-turkish-skills.git ~/.claude/skills/clean-turkish
```

Bu yöntem güncellemeleri `git pull` ile almanızı sağlar.

### Yöntem 3 — Python CLI ile Kurulum (Önerilen)

Eğer sisteminizde Python ve `uv` kuruluysa, projeyi doğrudan bir Python paketi olarak kurabilir ve yerleşik CLI araçlarını kullanabilirsiniz:

```bash
# Bağımlılıkları kurun ve CLI'ı geliştirici modunda bağlayın
uv pip install -e .
```

Kurulumdan sonra `clean-tr` komutu terminalinizde kullanılabilir olacaktır.

---

## CLI ve Geliştirici Araçları

Proje; kuralları doğrulamak, skill arşivini paketlemek, kurmak ve yerel metinleri taramak için gelişmiş bir Python CLI aracı (`clean-tr`) içerir.

### 1. Skill Doğrulama (Lint)

Yazım kurallarını ve meta verileri doğrulamak için:

```bash
clean-tr lint
```

### 2. Skill Paketleme (Build)

`SKILL.md` ve kılavuzları `clean-turkish.skill` zip dosyasına otomatik paketler:

```bash
clean-tr build
```

### 3. Otomatik Kurulum (Install)

Skill'i doğrudan Claude Code'un skill dizinine kopyalar:

```bash
# Global olarak kurar (~/.claude/skills/clean-turkish)
clean-tr install

# Yerel projeye kurar (.claude/skills/clean-turkish)
clean-tr install --local
```

### 4. Metin Tarayıcı (Scan)

Herhangi bir metin dosyasını veya standart girdiyi (stdin) Türkçe yapay zeka kalıplarına karşı tarar, renklendirilmiş bir çıktı sunar ve 100 üzerinden puanlar:

```bash
# Bir dosyayı tarayın
clean-tr scan dosya.txt

# Standart girdiden tarayın (borulama)
echo "Söz konusu proje bağlamında aksiyon alacağız." | clean-tr scan
```

---

## Geliştirici Notları ve Testler

Geliştirme yaparken testleri çalıştırmak için `pytest` kullanabilirsiniz:

```bash
# Bağımlılıkları yükleyin ve testleri çalıştırın
uv run pytest
```

---

**Claude Projects:** `SKILL.md` ve referans dosyalarını proje bilgisine yükleyin.

**Özel talimatlar:** `SKILL.md`'deki çekirdek kuralları kopyalayın.

**API çağrıları:** `SKILL.md`'yi sistem isteminize ekleyin. Referans dosyaları gerektiğinde yüklenir.

Kurulumdan sonra Claude'a şöyle diyin:

> "Şu metni Clean Turkish ile temizle: …"

## Hedef üslup

**Resmi ama temiz.** "Siz" dili ve saygı tonu korunur. Atılan şey resmiyet değil, **şişkinliktir**: bürokratik ekler, ek-fiil yığını, dolgu kalıpları, gizlenen özne.

## Neyi yakalar?

**Yasaklı kelime ve kalıplar** — Boğaz temizleme açılışları, plaza/karışık jargon, gereksiz zarflar, meta-yorum, **resmi şişkinlik ekleri** (`-mektedir`, `-dir`), **dolgu isim ve kalıplar** (söz konusu, bağlamında). Bkz. `guidelines/expressions.md`.

**Yapısal klişeler** — İkili karşıtlık, olumsuz listeleme, dramatik parçalama, sahte özne, uzaktan anlatıcı, **edilgen/kişisiz çatı**. Bkz. `guidelines/structures.md`.

**Türkçeye özgü kurallar** — Wh- yerine "Gelin/Peki/Şöyle ki" açılış takıntıları, sade zaman tercihi, uzun çizginin yalnızca diyalogda meşru olması.

## Puanlama

Her boyutu 1-10 arası puanlayın:

| Boyut       | Soru                                                 |
| ----------- | ---------------------------------------------------- |
| Doğrudanlık | İfade mi, duyuru mu?                                 |
| Ritim       | Çeşitli mi, metronom gibi mi?                        |
| Güven       | Okurun zekâsına güveniyor mu?                        |
| Doğallık    | İnsan eli değmiş gibi mi? Resmi ama şişkin değil mi? |
| Yoğunluk    | Kesilecek bir şey var mı?                            |

35/50 altı: revize edin.

## Yazar

[Ömer Doğan](https://omerdogan.dev/)

[Stop Slop](https://github.com/hardikpandya/stop-slop) (MIT) temel alınarak hazırlanmıştır.

## Lisans

MIT. Özgürce kullanın, geniş paylaşın.
