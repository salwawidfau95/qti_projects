
# QTI Backend API Project

## Overview
Project ini adalah RESTful API sederhana yang dibuat dengan FastAPI dan PostgreSQL/SQLite, dilengkapi dengan sistem autentikasi JWT, role-based access control (`admin` dan `user`), serta unit test menggunakan `pytest`.

Fitur utama:
- User Register & Login
- CRUD Profile (oleh user sendiri)
- CRUD Content (oleh user untuk kontennya sendiri)
- Role-based access (`admin` bisa kelola semua data, `user` hanya milik sendiri)
- Unit testing dengan pytest

---

## Tech Stack
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic
- JWT (JSON Web Token)
- SQLite (untuk pengujian)
- Pytest

---

## Setup & Running

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Jalankan server
```bash
uvicorn app.main:app --reload
```

---

## Testing

### Jalankan seluruh test
```bash
pytest
```

Test yang disediakan mencakup:
- Register & Login
- Get / Update / Delete Profile
- Create / Read / Update / Delete Content (oleh user)

---

## API Endpoints

### Auth
- `POST /auth/register` → Register user
- `POST /auth/login` → Login dan dapat token

### User
- `GET /users/profile` → Lihat profil sendiri
- `PATCH /users/profile` → Update profil sendiri
- `DELETE /users/profile` → Hapus akun sendiri

### Content
- `POST /content/` → Buat konten baru
- `GET /content/` → Lihat semua konten milik sendiri (user) / semua konten (admin)
- `GET /content/{id}` → Lihat konten detail
- `PUT /content/{id}` → Update konten milik sendiri
- `DELETE /content/{id}` → Hapus konten milik sendiri

---

## Autentikasi
Gunakan header:
```
Authorization: Bearer <your_jwt_token>
```
Token didapat setelah login (`/auth/login`).

---

## Roles
- `admin` → Dapat mengakses & mengelola semua user dan konten
- `user` → Hanya dapat mengakses & mengelola milik sendiri

---

## Catatan
- Semua fitur yang dapat diakses `user` sudah diuji dengan `pytest`
- Tidak ada testing untuk fitur khusus `admin-only`

---

## Author
Salwa Widfa Utami  
Backend Developer Test Submission  
PT Quantus Telematika Indonesia
