# 🧪 Quick Test - Auth Issues

## Problem: 403 Forbidden

Możliwe przyczyny:
1. Token wygasł
2. Token nie jest wysyłany
3. Backend wymaga re-login

## ✅ Szybkie Rozwiązanie:

### 1. Logout i Login Ponownie

W aplikacji:
1. Click **"Logout"** (w nawigacji)
2. Login ponownie: `admin` / `admin123`
3. Spróbuj ponownie edit/delete script

### 2. Sprawdź Token w Console

W przeglądarce:
1. Press **F12** (DevTools)
2. Console → wpisz:
```javascript
localStorage.getItem('auth_token')
```
3. Powinieneś zobaczyć długi string (JWT token)
4. Jeśli `null` → **zaloguj się ponownie**

### 3. Test API Bezpośrednio

```bash
# Get new token
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Copy token from response
TOKEN="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsImV4cCI6MTc2MDk5NDgyN30.jurg-5qAkL3-BXrYd8ISRaPIXlnOJQIYZbpaezf8QGw"

# Test update script
curl -X PUT http://localhost:8000/api/scripts/6 \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"script":"test"}'
```

---

## 🔧 Co Naprawiłem w api.ts:

1. ✅ Token reload z localStorage przy każdym request
2. ✅ Auto-logout na 401/403
3. ✅ Handle 204 No Content responses
4. ✅ Better error messages

---

## ✅ Po Frontend Reload:

1. **Logout** z aplikacji
2. **Login** ponownie: `admin` / `admin123`
3. Nowy fresh token
4. Wszystko powinno działać!

---

**Try now: Logout → Login → Edit script → Should work!** ✅

