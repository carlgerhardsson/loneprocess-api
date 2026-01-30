# Contributing Guide

## Kom igång med utveckling

### 1. Fork och klona

```bash
# Fork repository på GitHub först, sedan:
git clone https://github.com/[ditt-username]/loneprocess-api.git
cd loneprocess-api
```

### 2. Sätt upp utvecklingsmiljö

```bash
# Skapa virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Installera dependencies
pip install -r requirements.txt
```

### 3. Kör servern

```bash
python standalone_api.py
```

### 4. Testa dina ändringar

```bash
# Öppna Swagger UI
open http://localhost:8000/docs

# Eller kör test HTML
open docs/api_test.html
```

## Branches

- `main` - Production-klar kod
- `develop` - Development branch
- `feature/*` - Nya features
- `bugfix/*` - Buggfixar

## Pull Requests

1. Skapa en branch: `git checkout -b feature/min-feature`
2. Gör dina ändringar
3. Commita: `git commit -m "Add: beskrivning av ändring"`
4. Pusha: `git push origin feature/min-feature`
5. Skapa Pull Request på GitHub

## Commit Messages

Använd följande format:

- `Add: ` för nya features
- `Fix: ` för buggfixar
- `Update: ` för uppdateringar
- `Docs: ` för dokumentation
- `Refactor: ` för refactoring

Exempel:
```
Add: endpoint för att ta bort löneperiod
Fix: validering av datum i loneperiods
Update: förbättrad error handling
Docs: uppdaterad API_EXAMPLES.md
```

## Kodstandard

- Följ PEP 8 för Python kod
- Använd type hints där möjligt
- Dokumentera alla endpoints med Pydantic examples
- Håll funktioner små och fokuserade

## Frågor?

Kontakta backend-teamet på support@loneprocess.se
