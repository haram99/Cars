# نظام تأجير السيارات — الصفحة الرئيسية

- `tokens.json`: نظام التصميم (ألوان، خط، زوايا، مسافات، نصوص الموقع)
- `build.py`: يولّد `docs/index.html` من الرموز (بدون مكتبات خارجية)
- `.github/workflows/pages.yml`: ينشر الصفحة على GitHub Pages عند كل push إلى `main`

## التشغيل محليًا
    python build.py

## النشر
1. أنشئ مستودعًا على GitHub وارفع هذه الملفات إلى فرع `main`.
2. من Settings › Pages اختر Source: **GitHub Actions**.
3. بعد أول push سيظهر الرابط في تبويب Actions.
