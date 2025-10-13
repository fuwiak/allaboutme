# 🔍 Debug Steps - Check Console

## Frontend ma teraz debug logging!

---

## 🎯 Co Zrobić:

### 1. Otwórz Console (F12)

### 2. Wyczyść localStorage:
```javascript
localStorage.clear()
location.reload()
```

### 3. Login ponownie:
- Username: `admin`
- Password: `admin123`

### 4. Sprawdź Console - zobaczysz:
```
[API] POST /api/auth/login { hasToken: false, tokenPrefix: 'none' }
Login successful, token: eyJhbGciOiJIUzI1NiI...
Token saved in localStorage: YES
```

### 5. Kliknij Settings - zobaczysz:
```
Token found, loading settings...
[API] GET /api/settings/ { hasToken: true, tokenPrefix: 'eyJhbGci...' }
[API] Authorization header added
```

---

## ✅ Jeśli Widzisz:

### DOBRZE ✅:
```
[API] Authorization header added
```
→ Token jest wysyłany, backend powinien zaakceptować

### ŹLE ❌:
```
[API] No token available!
```
→ Token nie jest w localStorage - zaloguj się ponownie

---

## 🎉 Po Clear + Login:

**Wszystko powinno działać:**
- ✅ Settings load
- ✅ Edit scripts
- ✅ Delete scripts  
- ✅ Generate videos
- ✅ Upload backgrounds

---

**Wykonaj: localStorage.clear() → reload → login → sprawdź Console!**

W Console zobaczysz dokładnie co się dzieje z tokenem.

