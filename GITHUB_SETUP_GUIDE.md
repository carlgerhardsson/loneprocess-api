# 🚀 GitHub Setup Guide - Lättaste sättet!

## Två alternativ att välja mellan:

---

## 📦 Alternativ 1: Jag skapar ett zip-arkiv (ENKLAST!)

### Steg 1: Ladda ner allt
Jag packar ihop allt i ett zip-arkiv som du laddar ner.

### Steg 2: Skapa GitHub repo
1. Gå till https://github.com
2. Klicka på **"+"** → **"New repository"**
3. Namnge det: `loneprocess-api`
4. Välj **Public** eller **Private**
5. ✅ Kryssa i **"Add a README file"**
6. Klicka **"Create repository"**

### Steg 3: Ladda upp filerna
1. På din nya repo-sida, klicka **"Add file"** → **"Upload files"**
2. Dra och släpp alla filer från zip-arkivet
3. Skriv commit message: "Initial commit"
4. Klicka **"Commit changes"**

### Steg 4: Klona till VS Code
1. Öppna VS Code
2. Tryck **Ctrl+Shift+P** (Cmd+Shift+P på Mac)
3. Skriv: `Git: Clone`
4. Klistra in din repo URL: `https://github.com/[ditt-username]/loneprocess-api`
5. Välj var du vill spara projektet
6. Klicka **"Open"**

### Steg 5: Installera och kör
I VS Code terminal:
```bash
pip install -r requirements.txt
python standalone_api.py
```

**KLART!** 🎉

---

## 🔄 Alternativ 2: Använd Git från början (för mer kontroll)

### Vad du behöver installerat:
- Git: https://git-scm.com/downloads
- GitHub account: https://github.com

### Steg 1: Ladda ner zip-arkivet
Ladda ner alla filer jag packade.

### Steg 2: Skapa lokalt repo
```bash
# Packa upp zip-arkivet
cd loneprocess-api

# Initiera git
git init

# Lägg till alla filer
git add .

# Första commit
git commit -m "Initial commit: Löneprocess API setup"
```

### Steg 3: Skapa GitHub repo
1. Gå till https://github.com/new
2. Namnge: `loneprocess-api`
3. **KRYSSA INTE** i "Initialize with README" (vi har redan filer)
4. Klicka **"Create repository"**

### Steg 4: Koppla ihop och pusha
GitHub visar dig dessa kommandon - kör dem:
```bash
git remote add origin https://github.com/[ditt-username]/loneprocess-api.git
git branch -M main
git push -u origin main
```

### Steg 5: Öppna i VS Code
```bash
# Om du är i mappen redan:
code .

# Eller öppna via VS Code: File → Open Folder
```

### Steg 6: Installera och kör
```bash
pip install -r requirements.txt
python standalone_api.py
```

---

## 👥 För Frontend-teamet (superviktigt!)

När du lagt upp på GitHub kan frontend-teamet göra såhär:

### 1. Klona repo (supersimpelt!)

```bash
git clone https://github.com/[ditt-username]/loneprocess-api.git
cd loneprocess-api
pip install -r requirements.txt
python standalone_api.py
```

**Eller i VS Code:**
1. Ctrl+Shift+P → `Git: Clone`
2. Klistra in repo URL
3. Öppna terminalen
4. Kör: `pip install -r requirements.txt && python standalone_api.py`

### 2. API är nu tillgängligt på:
```
http://localhost:8000/api/v1
```

### 3. De kan börja utveckla!
All dokumentation finns i:
- Swagger UI: http://localhost:8000/docs
- `docs/FRONTEND_INTEGRATION.md`
- `docs/API_EXAMPLES.md`

---

## 🔄 Uppdatera senare

Om du gör ändringar:

### Du (repo owner):
```bash
# Gör ändringar i koden
git add .
git commit -m "Update: beskrivning av ändring"
git push
```

### Frontend-teamet (få uppdateringar):
```bash
git pull
```

Det är ALLT! Alla får automatiskt samma version! 🎉

---

## 🎯 Min rekommendation för dig:

### **Använd Alternativ 1** om:
- ✅ Du vill ha det enklaste sättet
- ✅ Du är inte van vid Git commandline
- ✅ Du vill komma igång direkt

### **Använd Alternativ 2** om:
- ✅ Du är bekväm med Git
- ✅ Du vill ha full kontroll från början
- ✅ Du planerar göra många updates

---

## 📦 Filer som kommer finnas i repo:

```
loneprocess-api/
├── README.md                      ← Projektbeskrivning
├── standalone_api.py              ← API servern
├── requirements.txt               ← Dependencies
├── .gitignore                     ← Filer att ignorera
├── CONTRIBUTING.md                ← Guide för contributors
├── docs/
│   ├── API_EXAMPLES.md            ← Request/response exempel
│   ├── ERROR_CODES.md             ← Felkoder
│   ├── FRONTEND_INTEGRATION.md    ← Frontend guide
│   └── api_test.html              ← Test sida
└── .github/
    └── workflows/
        └── test.yml               ← Automatiska tester
```

---

## ❓ FAQ

### Q: Behöver jag betala för GitHub?
**A:** Nej! Gratis account räcker. Du kan ha obegränsat med publika repos.

### Q: Vad är skillnaden på public och private repo?
**A:** 
- **Public** - Alla kan se koden (men bara du kan ändra)
- **Private** - Bara du och folk du bjuder in kan se

### Q: Kan flera personer jobba samtidigt?
**A:** Ja! Det är hela poängen med GitHub. Alla klonar, gör ändringar, och pushar.

### Q: Vad händer om vi gör ändringar samtidigt?
**A:** Git hanterar det! Om samma rad ändras får ni "merge conflict" som ni löser tillsammans.

### Q: Måste frontend-teamet kunna Git?
**A:** Nej! De kan använda VS Code's Git-integration (knappar istället för kommandon).

---

## 🎓 Vad du får med GitHub:

✅ **Version control** - Hela historiken sparas
✅ **Backup** - Koden finns i molnet
✅ **Collaboration** - Flera kan jobba samtidigt
✅ **Easy sharing** - En URL och alla kan klona
✅ **Issues** - Rapportera bugs
✅ **Releases** - Tagga versioner
✅ **CI/CD** - Automatiska tester (redan konfigurerat!)

---

## 🚀 Nästa steg för dig:

1. Ladda ner zip-arkivet jag skapar
2. Följ **Alternativ 1** ovan
3. Dela repo-länken med frontend-teamet
4. Alla kan börja jobba!

**Vill du att jag packar ihop allt i ett zip-arkiv nu?** 📦
