# Oʻzbek lotin klaviatura tartibi — macOS

Standart US klaviaturada yangi oʻzbek lotin harflarini **ş ç ğ ö** (va
**Ş Ç Ğ Ö**) **Option (⌥)** tugmasi yordamida yozing. Bu klaviatura tartibi —
orqa fonda hech qanday dastur ishlamaydi.

(macOS da alohida AltGr tugmasi yoʻq, shuning uchun **Option** ishlatiladi — bu
Windows va Linux versiyalaridagi AltGr qatlamining macOS dagi muqobilidir.)

| Tugmalar             | Natija |
|----------------------|--------|
| ⌥ Option + S         | ş  (⌥⇧S → Ş) |
| ⌥ Option + C         | ç  (⌥⇧C → Ç) |
| ⌥ Option + G         | ğ  (⌥⇧G → Ğ) |
| ⌥ Option + O         | ö  (⌥⇧O → Ö) |

Qolgan barcha tugmalar standart US tartibidagidek yozadi.

## Manba fayl

`UzbekLatin.keylayout` — tartibning oʻzi, oddiy matnli XML fayl (macOS yuklaydigan
format). U qoʻlda yozilgan va **macOS da sinovdan oʻtkazilmagan**, shuning uchun
oʻrnatgandan soʻng tekshiring va xatolik boʻlsa xabar bering.

## Oʻrnatish

1. **`UzbekLatin.keylayout`** faylini quyidagi papkaga nusxalang:
   - `~/Library/Keyboard Layouts/` — **tavsiya etiladi** (faqat joriy
     foydalanuvchi uchun; bu ishonchli joy, tartib tizimdan oddiy chiqib
     qayta kirgandan soʻng paydo boʻladi), **yoki**
   - `/Library/Keyboard Layouts/` — barcha foydalanuvchilar uchun (parol
     soʻraladi va odatda tartib paydo boʻlishidan oldin toʻliq **qayta ishga
     tushirish** kerak boʻladi).

   Finder da **Go → Go to Folder…** (⇧⌘G) orqali yoʻlni joylashtiring. Agar
   `Keyboard Layouts` papkasi boʻlmasa, uni yarating.
2. **Tizimdan chiqib, qayta kiring** (yoki qayta ishga tushiring). macOS yangi
   tartiblarni faqat tizimga kirishda qidiradi.
3. **System Settings → Keyboard → Text Input → Input Sources → Edit…** ni oching.
4. **+** ni bosing, **Others** ni tanlang (yoki pastga aylantiring) →
   **Uzbek Latin** → **Add**.
5. Unga menyu qatoridagi kiritish menyusidan yoki **⌃ Space** (Control+Space)
   orqali oʻting.

## Qanday yozish

Kiritish menyusidan **Uzbek Latin** ni tanlang, soʻng **Option (⌥)** ni bosib
turib S / C / G / O ni bosing. Bosh harflar uchun **Shift** qoʻshing. Qolgan
hamma narsa odatdagidek yoziladi.

## Eslatmalar

- **Gatekeeper:** `.keylayout` — bu dastur emas, balki oddiy maʼlumot, shuning
  uchun «aniqlanmagan ishlab chiquvchi» ogohlantirishi yoʻq va notarizatsiya
  ham kerak emas.
- **Option qatlami faqat shu toʻrtta harf uchun moʻljallangan.** Bu tartib faol
  boʻlganda macOS ning standart Option belgilari (å, ∂, Option-c orqali ç,
  diakritik «oʻlik» tugmalar va h.k.) **yozilmaydi**. Ular kerak boʻlganda oddiy
  **U.S.** kiritish manbasiga qayting.

## Oʻchirish

1. **System Settings → Keyboard → Text Input → Input Sources → Edit… →**
   **Uzbek Latin → −** ni tanlab oʻchiring.
2. Oʻzingiz ishlatgan `Keyboard Layouts` papkasidan `UzbekLatin.keylayout`
   faylini oʻchiring.
3. Tizimdan chiqib, qayta kiring.

## Noldan yigʻish (ixtiyoriy)

Tartibni grafik muharrirda qayta yaratish yoki oʻzgartirish uchun **Ukelele**
(bepul) dan foydalaning. Agar macOS ning barcha standart Option belgilarini
saqlab qolgan holda shu toʻrtta harfni qoʻshmoqchi boʻlsangiz, eng oson yoʻl —
tizimdagi **U.S.** tartibni Ukelele da ochib, faqat S, C, G, O tugmalarining
Option / Option+Shift chiqishini oʻzgartirib, eksport qilishdir.
