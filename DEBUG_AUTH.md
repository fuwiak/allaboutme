# 🔍 Debug Auth Issue

## Problem: Token nie jest wysyłany do backend

## Szybki Test:

### 1. W przeglądarce otwórz Console (F12):

```javascript
// Sprawdź czy token istnieje
localStorage.getItem('auth_token')

// Powinno pokazać długi string jak:
// "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."

// Jeśli null:
// 1. Logout
// 2. Login ponownie
// 3. Sprawdź ponownie
```

### 2. Test request ręcznie:

```javascript
// W Console:
const token = localStorage.getItem('auth_token');

fetch('/api/settings/', {
  headers: {
    'Authorization': `Bearer ${token}`
  }
}).then(r => r.json()).then(console.log)

// Powinno zwrócić settings
// Jeśli 401 - token wygasł, zaloguj się ponownie
```

---

## 🔧 Najprostsze Rozwiązanie:

### Wyczyść localStorage i zaloguj się od nowa:

1. **W Console (F12)**:
```javascript
localStorage.clear()
location.reload()
```

2. **Login**: `admin` / `admin123`

3. **Test ponownie**

---

## ✅ Backend działa?

Sprawdź:
```bash
curl http://localhost:8000/health
```

Jeśli nie odpowiada - backend crashnął. Restart:

```bash
# Terminal 2
cd /Users/user/allaboutme/backend
source .venv/bin/activate
export DATABASE_URL="postgresql://postgres:postgres@localhost:5433/allaboutme"
export REDIS_URL="redis://localhost:6379/0"
export STORAGE_PATH="/tmp/allaboutme"
export JWT_SECRET_KEY="dev-secret"
uvicorn app.main:app --reload --port 8000
```

---

**Najpierw sprawdź czy backend działa, potem clear localStorage i re-login!**

