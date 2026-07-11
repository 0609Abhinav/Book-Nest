<h1 align="center">📚 BookNest — Your Book Exchange Hub</h1>

<p align="center">
  <strong>India's community platform for pre-owned book exchange</strong><br/>
  Connecting students and readers across the country with affordable, quality books.
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8%2B-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/Django-3.2-092E20?logo=django&logoColor=white" alt="Django" />
  <img src="https://img.shields.io/badge/Bootstrap-5.x-7952B3?logo=bootstrap&logoColor=white" alt="Bootstrap" />
  <img src="https://img.shields.io/badge/SQLite-3-003B57?logo=sqlite&logoColor=white" alt="SQLite" />
  <img src="https://img.shields.io/badge/License-MIT-green" alt="License" />
</p>

---

## 🌟 About

**BookNest** is a full-stack Django web application that allows students and readers to **discover, share, and download** pre-owned books. Whether you're looking for UP Board textbooks, CBSE study material, novels, or technical books — BookNest brings them all under one roof.

Built with ❤️ by **Abhinav Tripathi**.

---

## ✨ Features

| Feature                | Description                                                       |
| ---------------------- | ----------------------------------------------------------------- |
| 📖 **Browse Books**    | Explore books by category (UP Board, CBSE, ICSE, Novels, etc.)    |
| 🔍 **Search**          | Search books by title across the entire catalog                   |
| ➕ **Add Books**        | Registered users can list books with cover image & PDF upload     |
| 📥 **Download**        | Download book PDFs directly from the listing                      |
| 👤 **User Auth**       | Sign up, sign in, and manage your profile                         |
| 📂 **My Books**        | View and manage all books you've uploaded                         |
| 🗑️ **Delete Books**   | Remove your own listings anytime                                  |
| 🏙️ **City Filter**    | Browse books available in your city                               |
| 🔥 **New Releases**    | Highlighted section for recently added books                      |
| 📱 **Responsive UI**   | Fully responsive design that works on desktop, tablet, and mobile |
| 💬 **WhatsApp Chat**   | Floating WhatsApp button for instant contact                      |
| 📧 **Contact Form**    | Built-in contact form for inquiries                               |

---

## 🛠️ Tech Stack

- **Backend:** Python 3.8+, Django 3.2
- **Frontend:** HTML5, CSS3 (custom design system), Bootstrap 5, Font Awesome
- **Database:** SQLite3 (development)
- **Icons:** Custom inline SVG icons per category
- **Deployment:** Ready for any WSGI server (Gunicorn, uWSGI)

---

## 📂 Project Structure

```
BookNest/
├── books/                      # Django project root
│   ├── books/                  # Project configuration
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # Root URL configuration
│   │   ├── wsgi.py             # WSGI entry point
│   │   └── asgi.py             # ASGI entry point
│   ├── senior/                 # Main application
│   │   ├── models.py           # Database models (reg, category, addbooks, etc.)
│   │   ├── views.py            # View functions
│   │   ├── urls.py             # App URL patterns
│   │   ├── admin.py            # Admin configuration
│   │   └── migrations/         # Database migrations
│   ├── templates/              # HTML templates
│   │   ├── base.html           # Base layout (header, navbar, footer)
│   │   └── senior/             # App-specific templates
│   │       ├── index.html      # Home page
│   │       ├── latestbooks.html# Browse/filter books
│   │       ├── addbooks.html   # Add book form
│   │       ├── myprofile.html  # User's uploaded books
│   │       ├── signup.html     # Registration page
│   │       ├── signin.html     # Login page
│   │       ├── contactus.html  # Contact form
│   │       └── aboutus.html    # About page
│   ├── static/                 # Static assets
│   │   ├── css/                # Stylesheets
│   │   │   ├── global.css      # Custom design system
│   │   │   └── bootstrap.css   # Bootstrap framework
│   │   ├── js/                 # JavaScript files
│   │   ├── fonts/              # Custom fonts
│   │   └── images/             # Static images
│   ├── manage.py               # Django management script
│   └── db.sqlite3              # SQLite database (dev only)
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8+** installed on your system
- **pip** (Python package installer)
- **Git** (optional, for cloning)

### 1. Clone the Repository

```bash
git clone https://github.com/0609Abhinav/Book-Nest-.git
cd Book-Nest-
```

### 2. Create a Virtual Environment (Recommended)

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install django Pillow
```

### 4. Run Database Migrations

```bash
cd books
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin Access)

```bash
python manage.py createsuperuser
```

### 6. Start the Development Server

```bash
python manage.py runserver
```

Open your browser and visit: **http://127.0.0.1:8000/senior/home**

---

## 📋 Database Models

| Model       | Purpose                                      |
| ----------- | -------------------------------------------- |
| `reg`       | User registration (name, email, mobile, etc) |
| `login`     | Login credentials                            |
| `contact`   | Contact form submissions                     |
| `category`  | Book categories (UP Board, CBSE, etc.)       |
| `new`       | New/featured book releases                   |
| `city`      | City listings for location-based search      |
| `addbooks`  | User-uploaded books with details & files     |

---

## 🛣️ URL Routes

| URL                         | View        | Description              |
| --------------------------- | ----------- | ------------------------ |
| `/senior/home`              | `home`      | Home page                |
| `/senior/latestbooks/`      | `latest`    | Browse all/filtered books|
| `/senior/latestbooks/?id=X` | `latest`    | Filter by category       |
| `/senior/addbooks/`         | `addbuk`    | Add a new book           |
| `/senior/myprofile/`        | `profile`   | View your uploaded books |
| `/senior/signup/`           | `signu`     | User registration        |
| `/senior/signin/`           | `sign`      | User login               |
| `/senior/logout/`           | `logout`    | User logout              |
| `/senior/contactus/`        | `contactus` | Contact form             |
| `/senior/aboutus`           | `about`     | About page               |
| `/senior/delete/<id>/`      | `deletebook`| Delete a book            |

---

## 📸 Screenshots

### Home Page
The home page features a hero carousel, stats strip, category cards with custom SVG icons, new releases, city-based search, and a CTA banner.

### Browse Books
A grid layout of book cards with cover images, author info, pricing, and download buttons. Includes a category sidebar for filtering.

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/your-feature`
3. **Commit** your changes: `git commit -m "Add your feature"`
4. **Push** to the branch: `git push origin feature/your-feature`
5. **Open** a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 📞 Contact

- **Developer:** Abhinav Tripathi
- **YouTube:** [POLY UPDATE](https://youtube.com/c/POLYUPDATE)
- **Instagram:** [@_abhinavtripathi](https://www.instagram.com/_abhinavtripathi/)
- **Facebook:** [Abhinav Tripathi](https://www.facebook.com/profile.php?id=100014486285262)

---

<p align="center">
  Made with ❤️ in India &nbsp;|&nbsp; © 2024 BookNest
</p>
