---
name: clean-turkish
description: Türkçe metinlerden yapay zeka yazım kalıplarını temizler. Türkçe taslak yazarken, düzenlerken veya metni AI kalıpları için gözden geçirirken kullanın.
metadata:
  trigger: Türkçe metin yazma, taslak düzenleme, AI kalıpları için içerik denetimi
  author: Onur Oduncu (https://onuroduncu.com/)
  language: tr
  adapted-from: stop-slop (İngilizce)
---

# Clean Turkish

Türkçe metinlerden öngörülebilir yapay zeka yazım kalıplarını temizleyin.

Bu, İngilizce sürümün çevirisi değil; Türkçeye uyarlamasıdır. İngilizce AI belirtilerinin (em dash, "-ly" zarfları, Wh- ile başlama, "Here's the thing") çoğu Türkçeye oturmaz. Türkçenin kendi belirtileri vardır: bürokratik `-mektedir/-maktadır` eki, gereksiz `-dir` ek-fiili, "söz konusu / bağlamında / noktasında" dolguları, "Gelin yakından bakalım" blog açılışı, aşırı edilgen çatı.

## Hedef Üslup

**Resmi ama temiz.** "Siz" dili ve saygı tonu korunur. Atılan şey resmiyet değil, **şişkinliktir**: bürokratik ekler, ek-fiil yığını, dolgu kalıpları, gizlenen özne. Metin saygılı kalır ama nefes alır.

## Çekirdek Kurallar

1. **Dolgu kalıplarını kes.** Boğaz temizleme açılışlarını, vurgu koltuk değneklerini ve gereksiz zarfları sil. Bkz. [guidelines/expressions.md](guidelines/expressions.md).

2. **Kalıplaşmış yapıları kır.** İkili karşıtlıklardan, olumsuz listelemeden, dramatik parçalamadan, retorik kurgulardan ve sahte özneden kaçın. Bkz. [guidelines/structures.md](guidelines/structures.md).

3. **Etken çatı kullan.** Özneyi öne al. Edilgen ve kişisiz yapılardan kaçın ("yapılmaktadır" değil "ekip yaptı"). Cansız nesnelere insan eylemi yükleme ("karar ortaya çıkar" değil "yönetici karar verdi").

4. **Resmi şişkinlikten arın.** `-mektedir/-maktadır` yerine sade geniş/şimdiki zaman. Beyanı şişiren `-dir` ek-fiilini at ("önemlidir" → "önemli"). Siz dili kalır, ekler gider.

5. **Somut ol.** Belirsiz beyanlardan kaçın ("Nedenler yapısaldır"). "söz konusu, bağlamında, noktasında, açısından, itibariyle" dolgularını sil. Belirli şeyi adıyla söyle.

6. **Okuru sahneye koy.** Uzaktan-anlatıcı sesinden kaçın. "Siz" "insanlar"dan iyidir. Somut, soyuttan iyidir.

7. **Ritmi değiştir.** Cümle uzunluklarını karıştır. İki öğe üç öğeden iyidir. Paragrafları farklı bitir. Aşırı bağlaç zincirinden kaçın ("hem... hem de...", "gerek... gerekse...").

8. **Okura güven.** Olguyu doğrudan söyle. Yumuşatmayı, gerekçelendirmeyi, el bebek gül bebek anlatımı geç.

9. **Alıntılık cümleleri kes.** Vurgu alıntısı gibi duruyorsa yeniden yaz.

## Hızlı Kontroller

Metni teslim etmeden önce:

- Gereksiz zarf var mı ("aslında", "gerçekten", "kesinlikle", "oldukça", "adeta", "resmen", "tam anlamıyla")? Sil.
- `-mektedir/-maktadır` var mı ("yapılmaktadır", "görülmektedir")? Sade zamana çevir.
- Beyanı şişiren `-dir` ek-fiili var mı ("önemlidir", "gereklidir", "mümkündür")? At.
- Edilgen/kişisiz çatı var mı ("bilinmektedir", "düşünülmektedir", "karara varıldı")? Özneyi bul, öne al.
- Cansız özne insan eylemi yapıyor mu ("veriler bize söylüyor", "piyasa ödüllendirir")? Kişiyi adlandır.
- Boğaz temizleme açılışı var mı ("Şunu belirtmek gerekir ki", "İşin aslı şu", "Şöyle ki:")? Kes, konuya gir.
- Türkçe açılış takıntısı var mı ("Gelin... bakalım", "Peki ya...?", "Hadi...")? Sil.
- Dolgu kalıbı var mı ("söz konusu", "bağlamında", "noktasında", "açısından", "itibariyle")? Sil veya somutla.
- Meta-yorum var mı ("Bu yazıda... ele alacağız", "İlerleyen bölümlerde")? Sil, metin kendi yürüsün.
- İkili karşıtlık var mı ("X değil, Y")? Y'yi doğrudan söyle.
- Üç ardışık cümle aynı uzunlukta mı? Birini kır.
- Plaza/karışık jargon var mı ("aksiyon almak", "feedback vermek", "mindset", "değer katmak")? Sade Türkçeye çevir.
- Belirsiz beyan var mı ("Etkileri büyüktür", "Sonuçları önemlidir")? Somut etkiyi adlandır.
- Uzaktan anlatıcı var mı ("İnsanlar genellikle...", "Toplum olarak...")? Okuru sahneye koy.

## Puanlama

Her boyutu 1-10 arası puanla:

| Boyut | Soru |
|-------|------|
| Doğrudanlık | İfade mi, duyuru mu? |
| Ritim | Çeşitli mi, metronom gibi mi? |
| Güven | Okurun zekâsına güveniyor mu? |
| Doğallık | İnsan eli değmiş gibi mi? Resmi ama şişkin değil mi? |
| Yoğunluk | Kesilecek bir şey var mı? |

35/50 altı: revize et.

## Örnekler

Öncesi/sonrası dönüşümler için bkz. [guidelines/examples.md](guidelines/examples.md).

## Lisans

MIT
