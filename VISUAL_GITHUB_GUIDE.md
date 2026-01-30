# 📸 Visuell Guide - GitHub + VS Code Setup

## 🎯 Målet
Efter denna guide har du:
- ✅ Projektet på GitHub
- ✅ Projektet i VS Code
- ✅ Servern igång
- ✅ Frontend-teamet kan klona och köra

---

## 📦 STEG 1: Förberedelser

### Vad du behöver:
- [ ] GitHub account (gratis på https://github.com/signup)
- [ ] VS Code installerat (https://code.visualstudio.com)
- [ ] Python installerat (https://python.org)
- [ ] Git installerat (https://git-scm.com) - *eller använd GitHub Desktop*

---

## 🌟 ENKLASTE VÄGEN (Rekommenderad!)

### A) Skapa GitHub Repo (via webben)

**1. Gå till GitHub:**
```
https://github.com/new
```

**2. Fyll i:**
```
Repository name: loneprocess-api
Description: REST API för löneprocessaktiviteter
✅ Public (eller Private om du vill)
✅ Add a README file
```

**3. Klicka "Create repository"**

---

### B) Ladda upp filer

**1. På din nya repo-sida:**
```
Klicka: "Add file" → "Upload files"
```

**2. Dra och släpp dessa filer:**
```
✅ standalone_api.py
✅ requirements.txt
✅ README.md
✅ .gitignore
✅ CONTRIBUTING.md
✅ docs/ (hela mappen)
✅ .github/ (hela mappen)
```

**3. Längst ner:**
```
Commit message: "Initial commit - API setup"
Klicka: "Commit changes"
```

**KLART!** Din kod är nu på GitHub! 🎉

---

### C) Klona till VS Code

**1. Kopiera din repo URL:**
```
På GitHub-sidan, klicka på grön "Code" knapp
Kopiera URL: https://github.com/[ditt-username]/loneprocess-api.git
```

**2. Öppna VS Code:**
```
Tryck: Ctrl+Shift+P (Cmd+Shift+P på Mac)
Skriv: git clone
Välj: "Git: Clone"
Klistra in URL
Välj var du vill spara projektet (t.ex. Desktop eller Documents)
```

**3. När kloningen är klar:**
```
VS Code frågar: "Would you like to open the cloned repository?"
Klicka: "Open"
```

**PERFEKT!** Nu har du projektet i VS Code! 💻

---

### D) Installera och starta

**1. Öppna Terminal i VS Code:**
```
Terminal → New Terminal
(eller tryck Ctrl+`)
```

**2. Installera dependencies:**
```bash
pip install -r requirements.txt
```

Du ser massa text - det är okej! Vänta tills det är klart.

**3. Starta servern:**
```bash
python standalone_api.py
```

Du ser:
```
🚀 Löneprocess Digital Checklista API
✓ Database initialized successfully
📚 Swagger UI: http://localhost:8000/docs
```

**4. Öppna Swagger UI:**
```
Ctrl+Click (Cmd+Click på Mac) på länken
ELLER öppna i browser: http://localhost:8000/docs
```

**🎊 SUCCÉ! API:et körs!**

---

## 👥 DELA MED FRONTEND-TEAMET

### Skicka dem detta:

**Repo URL:**
```
https://github.com/[ditt-username]/loneprocess-api
```

**Instruktioner till dem:**
```
1. Öppna VS Code
2. Ctrl+Shift+P → "Git: Clone"
3. Klistra in: https://github.com/[ditt-username]/loneprocess-api
4. Öppna terminal i VS Code
5. Kör: pip install -r requirements.txt
6. Kör: python standalone_api.py
7. API körs nu på: http://localhost:8000
```

De kan också läsa: `docs/FRONTEND_INTEGRATION.md`

---

## 🔄 UPPDATERA SENARE

### När du gör ändringar i koden:

**I VS Code:**

**1. Se ändringar:**
```
Klicka på Source Control ikonen (grenen till vänster)
Du ser alla ändrade filer
```

**2. Commit ändringarna:**
```
Skriv ett meddelande i rutan, t.ex: "Fix: buggfix i activities endpoint"
Klicka på checkmark (✓) ikonen
```

**3. Push till GitHub:**
```
Klicka på "..." (tre prickar)
Välj "Push"
```

**KLART!** Dina ändringar är på GitHub!

---

### Frontend-teamet hämtar uppdateringar:

**I deras VS Code:**
```
Klicka på "..." i Source Control
Välj "Pull"
```

Alla får samma version automatiskt! 🔄

---

## 🎨 ALTERNATIV: GitHub Desktop (ännu enklare!)

Om du inte gillar kommandoraden:

**1. Ladda ner GitHub Desktop:**
```
https://desktop.github.com
```

**2. Efter installation:**
```
File → Clone Repository
Välj din repo från listan
Välj var den ska sparas
Klicka Clone
```

**3. Öppna i VS Code:**
```
Repository → Open in Visual Studio Code
```

**4. Commit och Push:**
```
Skriv commit message i GitHub Desktop
Klicka "Commit to main"
Klicka "Push origin"
```

Supersimpelt! 🎯

---

## 📊 Vad som händer nu:

```
DU                          GITHUB                      FRONTEND-TEAMET
│                              │                              │
├─ Skapar kod                  │                              │
├─ git add .                   │                              │
├─ git commit                  │                              │
├─ git push ──────────────────>│                              │
│                              ├─ Sparar kod                  │
│                              ├─ Kör tester (CI/CD)          │
│                              │<──────────────── git clone ──┤
│                              │                              ├─ Hämtar kod
│                              │                              ├─ pip install
│                              │                              ├─ python app
│                              │                              └─ Utvecklar!
│                              │                              │
├─ Gör ändringar               │                              │
├─ git push ──────────────────>│                              │
│                              │<──────────────── git pull ───┤
│                              │                              ├─ Får uppdatering
│                              │                              └─ Fortsätter jobba!
```

---

## ✅ Checklist innan du börjar:

### Förberedelser:
- [ ] GitHub account skapat
- [ ] VS Code installerat
- [ ] Python installerat
- [ ] Alla projektfiler nedladdade

### Setup:
- [ ] GitHub repo skapat
- [ ] Filer uppladdade till GitHub
- [ ] Repo klonat till VS Code
- [ ] Dependencies installerade
- [ ] Servern startar utan fel

### Test:
- [ ] http://localhost:8000/docs fungerar
- [ ] Kan testa endpoints i Swagger UI
- [ ] Database skapas automatiskt

### Dela:
- [ ] Frontend-teamet har repo URL
- [ ] De har instruktioner
- [ ] De kan klona och köra

---

## 🆘 Felsökning

### "git: command not found"
**Lösning:** Installera Git från https://git-scm.com

### "Permission denied" när du klonar
**Lösning:** Använd HTTPS URL istället för SSH, eller sätt upp SSH keys

### "pip: command not found"
**Lösning:** 
```bash
python -m pip install -r requirements.txt
# eller
python3 -m pip install -r requirements.txt
```

### "Port 8000 already in use"
**Lösning:** Någon annan process använder port 8000
```bash
# På Mac/Linux
lsof -ti:8000 | xargs kill

# På Windows
netstat -ano | findstr :8000
# Hitta PID och avsluta i Task Manager
```

### VS Code hittar inte Python
**Lösning:**
```
Ctrl+Shift+P → "Python: Select Interpreter"
Välj din Python installation
```

---

## 🎓 Sammanfattning

**Med GitHub:**
- ✅ All kod på ett ställe
- ✅ Version control (hela historiken)
- ✅ Enkelt att dela med teamet
- ✅ Automatiska backups
- ✅ Kan jobba från olika datorer

**Med VS Code:**
- ✅ Enkel Git-integration
- ✅ Inbyggd terminal
- ✅ Syntax highlighting
- ✅ Debugging tools

**Tillsammans = Perfekt utvecklingsmiljö!** 🚀

---

**Behöver du hjälp?** 
Läs mer i:
- `README.md` - Projektöversikt
- `CONTRIBUTING.md` - Utvecklingsguide
- `docs/` - All dokumentation
