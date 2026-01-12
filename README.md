**CMS Backend – Educational Content Manager**

This is a lightweight backend built with Django + Django REST Framework.
It lets editors create programs, terms and lessons, schedule when a lesson should go live,
and automatically makes it visible to students through a public API.

The focus of the project is:
✔ clean structure
✔ auto-publishing
✔ simple, easy-to-use APIs
✔ clear separation between admin users and public learners

-

**🧱 Architecture Overview**

Very simple flow:

```
[Admin User]
   |
   |  creates & schedules content
   v
[Django Admin + REST API] ---> stores in DB
   |
   |  worker checks timestamps
   v
[Auto Publish Worker]
   |
   |  once published
   v
[Public Catalog API] ---> visible to learners
```

Roles:

* **Editors/Admins** → create/update/schedule lessons
* **Worker** → runs every minute and publishes scheduled lessons
* **Learners** → read-only access to published lessons only



**⚙️ Local Setup (Python)**

1️⃣ Clone the repo

```bash
git clone <repo-url>
cd cms-backend
```

2️⃣ Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .\.venv\Scripts\activate
```

3️⃣ Install packages

```bash
pip install -r requirements.txt
```

4️⃣ Create your `.env`

```bash
cp .env.example .env
```

5️⃣ Run migrations

```bash
python manage.py migrate
```

6️⃣ Create a superuser

```bash
python manage.py createsuperuser
```

7️⃣ Start the server

```bash
python manage.py runserver
```

Admin available at:
👉 [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

---

## **📦 Running the Worker**

The worker is what turns scheduled lessons into published lessons.

Manual run (use anytime):

```bash
python manage.py publish_scheduled
```

Loop version (optional during testing):

```bash
while true; do python manage.py publish_scheduled; sleep 60; done
```

---

**🎬 Demo Flow **

1️⃣ Login to **/admin** using your superuser
2️⃣ Create:

* a Program
* a Term inside that Program
* a Lesson inside that Term

3️⃣ Set the Lesson to:

* `status = scheduled`
* pick a future **publish_at** time

4️⃣ Wait until time passes (or run `publish_scheduled`)
5️⃣ Check:

* `/catalog/programs/`
* `/catalog/lessons/`

➡️ Your scheduled lesson will now appear as **published**.



**🗃 Migrations & Seeding**

Run migrations anytime:

```bash
python manage.py makemigrations
python manage.py migrate
```

Optional seed support:

```bash
python manage.py loaddata seed.json
```


**🌍 Public & Admin URLs**

| Feature        | URL                  |
| -------------- | -------------------- |
| Admin Panel    | `/admin/`            |
| Auth Token     | `/api/token/`        |
| Public Catalog | `/catalog/programs/` |
| API Docs       | `/api/docs/`         |


**📝 Tech Used**

* Django
* Django REST Framework
* JWT Authentication
* Simple scheduled worker (no heavy Celery)
* PostgreSQL (prod) / SQLite (dev)



**✔️ Summary**

This backend:

* Lets editors manage learning content
* Allows scheduling lessons for future release
* Automatically publishes lessons on time
* Gives learners a clean read-only API
* Keeps permissions, structure, and workflow simple

