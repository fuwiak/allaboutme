# 🚀 PROSTY START - Skopiuj i Wklej

## Masz 3 terminale otwarte. Uruchom to:

### Terminal 1: Backend (zatrzymaj stary, uruchom nowy)

```bash
# Ctrl+C (zatrzymaj stary backend)

# Potem:
cd /Users/user/allaboutme/backend
./run_backend.sh
```

### Terminal 2: Celery

```bash
cd /Users/user/allaboutme/backend
./run_celery.sh
```

### Terminal 3: Frontend (już działa, zostaw)

```bash
# Zostaw jak jest - już działa
```

---

## ✅ Potem:

1. http://localhost:5173
2. Login: `admin` / `admin123`
3. Dashboard → Generate Scripts
4. DZIAŁA! ✅

---

## 🔧 Dlaczego to nie działało:

❌ **Źle**: `uvicorn app.main:app --reload --port 8000`
- Brak DATABASE_URL
- Brak STORAGE_PATH
- Używa .venv z głównego katalogu zamiast backend/.venv

✅ **Dobrze**: `./run_backend.sh`
- Ustawia wszystkie zmienne
- Używa właściwego .venv
- Uruchamia z właściwego katalogu

---

## 📋 Wszystkie Komendy (Kopiuj i Wklej):

```bash
# Terminal 1: Backend
cd /Users/user/allaboutme/backend
./run_backend.sh

# Terminal 2: Celery  
cd /Users/user/allaboutme/backend
./run_celery.sh

# Terminal 3: Frontend (already running)
# Leave it as is
```

Done! 🎉

