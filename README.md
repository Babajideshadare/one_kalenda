# One Kalenda 🗓️

One Kalenda is a work-in-progress **habit and calendar tracker** built with **Django**.

The goal: give you a clean calendar interface to track daily habits, mark them as completed, and write notes for each day – then see simple reports over time.

This project is being developed **step-by-step**, with an emphasis on learning and clarity:
- Small, focused tasks
- Clear “checkers” for each step
- UI/UX first, then back-end logic

---

## 🚧 Project Status

**Status:** Early development (pre-MVP)

Currently implemented:

- Django project and `habits` app
- Global layout:
  - Left **sidebar** with navigation:
    - CALENDAR VIEW
    - REPORT
    - CUSTOMIZE ICONS
    - DAILY NOTES ENTRY
  - Top **nav bar** with:
    - Collapsible sidebar toggle (X / ☰)
    - “CREATE CALENDAR ENTRY +” button
    - Notification icon, SETTINGS, PROFILE
  - Main **content area** with an initial empty state:
    - “ADD CALENDAR ENTRY” + `+` button
- Collapsible sidebar:
  - Expanded: full sidebar visible, icon shows **X**
  - Collapsed: sidebar fully hidden, icon shows **☰**
  - Smooth animation
- Color palette matches the UI design:
  - Nav bar: `#43318C`
  - Sidebar: `#262628`
  - Active item highlight (Calendar View): `rgba(67, 49, 140, 0.2)`
  - Sidebar divider: `#555555`
  - Text: white on nav/sidebar, black in content

Not yet implemented (planned):

- User registration / login / logout
- Habit management (create/rename/delete habits)
- Calendar view per habit (month view with completed/notes indicators)
- Daily notes & completed status storage
- Reports (e.g. last 30 days summary)
- Customize icons / habit colors

---

## 🧠 Concept

### Core idea

For each **habit** and each **date**, One Kalenda will allow you to:

- Mark the habit as **completed** (yes/no)
- Add **multiple text notes** (e.g. “Slept at 11pm, woke at 6am”)

You will then be able to:

- See these on a **calendar** for each habit
- Use a **Daily Notes** view to edit one day at a time
- See **reports** over the last X days

### UI/UX structure

The app layout is built around three main regions:

- **Sidebar** (left, dark):
  - LOGO
  - CALENDAR VIEW
  - REPORT
  - CUSTOMIZE ICONS
  - DAILY NOTES ENTRY

- **Top nav bar** (purple):
  - X / ☰ toggle button to hide/show sidebar
  - “CREATE CALENDAR ENTRY +”
  - Notification icon
  - SETTINGS, PROFILE (placeholders for now)

- **Content area** (white):
  - Currently shows an empty state:
    - `ADD CALENDAR ENTRY`
    - `+` button below
  - Will later show:
    - Calendar view, notes panel, and reports

---

## 🛠 Tech Stack

- **Backend:** Django (4.2+ up to <7, currently using 5.x on servers)
- **Frontend:** Django templates + CSS + a tiny bit of JavaScript
- **Database:** SQLite (development)
- **Deployment:** PythonAnywhere (for now; via GitHub + `git pull`)

---

## 📁 Project Structure

From the project root:

\`\`\`text
one_kalenda/
├─ manage.py
├─ one_kalenda/
│  ├─ __init__.py
│  ├─ settings.py
│  ├─ urls.py
│  ├─ asgi.py
│  └─ wsgi.py
├─ habits/
│  ├─ __init__.py
│  ├─ admin.py
│  ├─ apps.py
│  ├─ migrations/
│  ├─ models.py
│  ├─ tests.py
│  ├─ views.py
│  └─ urls.py
├─ templates/
│  ├─ base.html
│  └─ habits/
│     └─ home.html
├─ static/
│  ├─ css/
│  │  └─ styles.css
│  └─ js/
│     └─ sidebar.js
├─ requirements.txt
└─ README.md
\`\`\`

Key files:

- \`one_kalenda/settings.py\` – Django configuration (templates, static, allowed hosts)
- \`one_kalenda/urls.py\` – routes root URL to \`habits.urls\`
- \`habits/views.py\` – currently only \`home\` view
- \`templates/base.html\` – global layout (sidebar + topbar + \`{% block content %}\`)
- \`templates/habits/home.html\` – initial homepage content inside the layout
- \`static/css/styles.css\` – layout and design system
- \`static/js/sidebar.js\` – sidebar collapse/expand logic

---

## 🚀 Getting Started (Local Development)

### 1. Clone the repo

\`\`\`bash
git clone https://github.com/<YOUR_USERNAME>/one_kalenda.git
cd one_kalenda
\`\`\`

### 2. Create and activate a virtualenv

On Windows (PowerShell):

\`\`\`bash
python -m venv venv
venv\Scripts\activate
\`\`\`

On macOS / Linux:

\`\`\`bash
python3 -m venv venv
source venv/bin/activate
\`\`\`

### 3. Install dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

\`requirements.txt\` currently includes:

\`\`\`text
Django>=4.2,<7
djangorestframework>=3.15,<4
\`\`\`

(DRF is installed but not used yet.)

### 4. Apply migrations

\`\`\`bash
python manage.py migrate
\`\`\`

### 5. Run the development server

\`\`\`bash
python manage.py runserver
\`\`\`

Visit:

- \`http://127.0.0.1:8000/\`

You should see:

- Sidebar with CALENDAR VIEW, REPORT, CUSTOMIZE ICONS, DAILY NOTES ENTRY
- Purple top bar with X / ☰, CREATE CALENDAR ENTRY +, bell, SETTINGS, PROFILE
- Centered “ADD CALENDAR ENTRY” with a + button
- Clicking X/☰ hides/shows the sidebar with a smooth animation

---

## 🌐 Deployment (PythonAnywhere Outline)

One Kalenda has been deployed to PythonAnywhere using this flow:

1. **On PythonAnywhere**
   - Start a Bash console:
     \`\`\`bash
     cd ~
     git clone https://github.com/<YOUR_USERNAME>/one_kalenda.git
     cd one_kalenda
     python3.10 -m venv venv      # or python3.11
     source venv/bin/activate
     pip install -r requirements.txt
     python manage.py migrate
     \`\`\`

2. **Create a web app** (Manual configuration, choose same Python version as venv)

3. **Web app config**
   - Source code: \`/home/<USERNAME>/one_kalenda\`
   - Virtualenv: \`/home/<USERNAME>/one_kalenda/venv\`
   - Static files:
     - URL: \`/static/\`
     - Directory: \`/home/<USERNAME>/one_kalenda/static\`

4. **WSGI file** (\`/var/www/<USERNAME>_pythonanywhere_com_wsgi.py\`):

   \`\`\`python
   import os
   import sys

   project_path = os.path.expanduser('~/one_kalenda')
   if project_path not in sys.path:
       sys.path.append(project_path)

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'one_kalenda.settings')

   from django.core.wsgi import get_wsgi_application
   application = get_wsgi_application()
   \`\`\`

5. **Reload** the web app.

Future updates:

- Locally: \`git add\` → \`git commit\` → \`git push\`
- On PythonAnywhere: \`cd ~/one_kalenda && source venv/bin/activate && git pull\` → Web tab → **Reload**

---

## 📌 Development Style: Steps & Checkers

This project is built in **small steps**, each with:

- A set of **tasks** (e.g. “create view”, “add URL”, “update template”)
- A set of **checkers** (e.g. “URL loads without error”, “element visible in browser”)

Example (already completed):

- **Step:** Implement collapsible sidebar
- **Checkers:**
  - Sidebar visible with nav items and LOGO in expanded state
  - Clicking X → sidebar hides completely; icon switches to ☰
  - Clicking ☰ → sidebar returns; icon switches to X
  - No JS errors in browser console

If you contribute, try to keep this style:

- Describe changes in small steps
- Specify how to verify them

---

## 🧩 Roadmap

Planned next steps:

1. **User Authentication**
   - Register
   - Login / Logout
   - Protect main pages (\`login_required\`)

2. **Habits**
   - \`Habit\` model (user, name, created_at)
   - CRUD: create, rename, delete habits
   - Habit selection UI (tabs / dropdown / sidebar list)

3. **Daily Notes & Entries**
   - \`HabitEntry\` model for (habit, date, completed)
   - \`HabitNote\` model for text notes linked to an entry
   - “Daily Notes Entry” screen:
     - Date selector
     - Completed toggle
     - Notes list + “Add note” form

4. **Calendar View**
   - Month view per habit with navigation
   - Visual indicators for:
     - Completed days
     - Days with notes
   - Click day → show details (completed + notes)

5. **Reports**
   - Simple summary: last 30 days
   - Per-habit completion counts & recent notes

6. **Customize Icons / Themes**
   - Let users assign icons/colors to habits
   - Store these in the database and reflect in UI

---

## 🤝 Contributing

Right now this is a learning and personal project, but contributions/feedback are welcome.

Guidelines:

- Keep changes small and focused.
- Follow Django best practices (views, templates, models).
- Respect the **step + checkers** pattern whenever possible.
- Add or update documentation / comments if behavior changes.

---

## 🙏 Credits

- **Design:** Home layout and visual direction by the project owner’s girlfriend (UI/UX designer).
- **Development:** Django + templates + CSS/JS by the project owner, with AI assistance.

---

## 📄 License

License: **TBD**

