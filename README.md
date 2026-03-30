# TrustHut Backend

> Django REST API backend for the TrustHut accessibility reporting platform.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Framework | Django 5.1.5 + Django REST Framework 3.15.2 |
| Auth | Firebase Admin SDK 6.6.0 (token verification) |
| Database | Google Cloud Firestore (NoSQL) |
| Email | Django SMTP (Gmail) |
| Server | Gunicorn 23.0.0 |
| Static Files | WhiteNoise 6.8.2 |
| Deployment | Vercel (serverless) / Render (container) |

---

## Project Structure

```
trusthut_backend/
├── apps/
│   ├── core/              # Firebase singleton, shared middleware, config
│   │   ├── firebase.py    # FirebaseService — init, Firestore client, token verify
│   │   ├── middleware.py  # Firebase auth decorator
│   │   ├── config.py      # Firestore collection names
│   │   └── exceptions.py  # Custom DRF exception handler
│   ├── users/             # User registration, profiles, OTP password reset
│   ├── posts/             # Accessibility report CRUD + search
│   ├── likes/             # Like / unlike posts
│   └── chatbot/           # AI chatbot query endpoint
├── trusthut_backend/
│   ├── settings.py        # Django settings
│   ├── urls.py            # Root URL config
│   └── wsgi.py            # WSGI entry point (Vercel/Gunicorn)
├── vercel.json            # Vercel serverless config
├── render.yaml            # Render blueprint
├── build.sh               # Render build script
└── requirements.txt
```

---

## API Reference

### Authentication
All protected endpoints require `Authorization: Bearer <firebase_id_token>` header.

### Posts
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `GET` | `/api/posts/` | ❌ | List all posts |
| `GET` | `/api/posts/<id>/` | ❌ | Get single post |
| `POST` | `/api/posts/create/` | ✅ | Create new report |
| `PUT` | `/api/posts/update/<id>/` | ✅ | Update post (owner only) |
| `DELETE` | `/api/posts/delete/<id>/` | ✅ | Delete post (owner only) |
| `GET` | `/api/posts/search/?q=` | ❌ | Search posts |
| `GET` | `/api/posts/user/` | ✅ | Get current user's posts |

### Users
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/users/register/` | ✅ | Register user in Firestore |
| `GET` | `/api/users/profile/` | ✅ | Get profile |
| `PUT` | `/api/users/profile/` | ✅ | Update profile |
| `GET` | `/api/users/all/` | ✅ | List all users (admin) |
| `POST` | `/api/users/forgot-password/send-otp/` | ❌ | Send OTP to email |
| `POST` | `/api/users/forgot-password/verify-otp/` | ❌ | Verify OTP + reset password |

### Likes
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/like/` | ✅ | Like a post |
| `POST` | `/api/unlike/` | ✅ | Unlike a post |
| `GET` | `/api/like/check/<postId>/` | ✅ | Check like status |

### Chatbot
| Method | Endpoint | Auth | Description |
|---|---|---|---|
| `POST` | `/api/chatbot/query/` | ❌ | Send query to AI chatbot |

---

## Environment Variables

| Variable | Description |
|---|---|
| `SECRET_KEY` | Django secret key |
| `DEBUG` | `True` for dev, `False` for prod |
| `ALLOWED_HOSTS` | Comma-separated allowed hosts |
| `CORS_ALLOWED_ORIGINS` | Comma-separated CORS origins |
| `FIREBASE_CREDENTIAL_PATH` | Path to `serviceAccountKey.json` (local only) |
| `FIREBASE_CREDENTIALS_BASE64` | Base64-encoded service account JSON (cloud) |
| `GOOGLE_MAPS_KEY` | Google Maps API key |
| `EMAIL_HOST` | SMTP host (e.g. `smtp.gmail.com`) |
| `EMAIL_PORT` | SMTP port (587) |
| `EMAIL_HOST_USER` | Sender Gmail address |
| `EMAIL_HOST_PASSWORD` | Gmail App Password |
| `EMAIL_FROM` | Display name + address |

---

## Local Setup

```bash
# Create & activate virtual environment
python -m venv .venv
.venv\Scripts\activate     # Windows
source .venv/bin/activate  # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env       # fill in your values

# Run development server
python manage.py runserver
```

---

## Deployment

### Vercel
- Push to `main` branch — Vercel auto-deploys via `vercel.json`
- Set all env vars in Vercel dashboard → Project → Settings → Environment Variables
- Use `FIREBASE_CREDENTIALS_BASE64` (base64 of `serviceAccountKey.json`)

### Render
- Uses `render.yaml` blueprint + `build.sh`
- Mount `serviceAccountKey.json` as a Secret File at `/etc/secrets/serviceAccountKey.json`

---

## Firebase Credentials for Cloud Deployment

```powershell
# Generate base64 from local JSON file (Windows)
$bytes = [IO.File]::ReadAllBytes("serviceAccountKey.json")
[Convert]::ToBase64String($bytes) | Set-Content firebase_b64.txt -NoNewline
```
Paste the contents of `firebase_b64.txt` as the `FIREBASE_CREDENTIALS_BASE64` env var.
