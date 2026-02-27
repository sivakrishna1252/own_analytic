# Analyatics - Professional Analytics SaaS 📊🛡️

**Analyatics** is a powerful, self-hosted, multi-tenant analytics platform designed for modern web applications. It provides real-time visitor insights, session intelligence, and geographic data with a sleek, executive-level dashboard.

---

## 🚀 Key Features

### 1. **Universal Tracking Engine**
*   **Plug-and-Play Integration**: A lightweight, vanilla JavaScript tracker (`tracker.js`) that works on any platform (HTML, React, Next.js, Vue).
*   **SPA Support**: Automatically detects URL changes in Single Page Applications without page reloads.
*   **Session Management**: Intelligent session tracking that handles heartbeats (20s intervals) and reliable session-end signals using `navigator.sendBeacon`.

### 2. **Executive Intelligence Dashboard**
*   **Vibrant Glassmorphism UI**: A high-end, dark-mode dashboard with modern typography and visual hierarchy.
*   **Real-time Visitor Feed**: Expandable cards showing deep technical details (IP, Location, Browser, OS, Device, and full Navigation Path).
*   **Geographic Insights**: Interactive donut charts and breakdown lists of visitor distribution by country.
*   **Performance Metrics**: Track Total Visitors, Page Hits, Average Duration, and Top Performance Pages with intensity bars.

### 3. **Deep Data Tracking**
*   **Geo-Location**: Precise country detection using GeoIP2.
*   **Environment Detection**: Automatic parsing of User-Agents to identify Browser, OS, and Device types (Mobile/Desktop/Tablet).
*   **Engagement Scores**: Calculation of total sessions, unique pages visited, and precise time spent per page/session.

### 4. **Security & Reliability**
*   **Bot Shield**: Built-in detection to filter out and block abnormal bot traffic.
*   **Beacon API**: Ensures data is saved even when users close the tab or browser.
*   **API Security**: Multi-tenant architecture with unique Site IDs and API Keys for every registered website.

---

## 🛠️ Technology Stack

*   **Backend**: Python / Django / Django REST Framework
*   **Database**: PostgreSQL (via `psycopg2-binary`)
*   **Frontend**: Vanilla HTML5 / CSS3 / JavaScript (ES6+)
*   **Charts**: Chart.js
*   **Geo-Detection**: GeoIP2
*   **Icons**: Lucide-inspired SVG System

---

## 📦 Installation & Setup

1.  **Clone the Repository**:
    ```bash
    git clone [your-repo-link]
    cd Analyatics
    ```

2.  **Install Dependencies**:
    ```bash
    pip install django djangorestframework psycopg2-binary geoip2 django-cors-headers user-agents pyyaml
    ```

3.  **Database Migration**:
    ```bash
    python manage.py migrate
    ```

4.  **Run the Server**:
    ```bash
    python manage.py runserver
    ```

---

## 🔗 How to Integrate

1.  **Register Your Website**: Go to `/api/sites/create/` (or the UI page) to generate your **Site ID** and **API Key**.
2.  **Paste the Script**: Add the following code before the closing `</head>` tag of your website:
    ```html
    <script async 
        src="http://YOUR-DOMAIN.com/tracker.js" 
        data-api-key="YOUR_API_KEY" 
        data-site-id="YOUR_SITE_ID">
    </script>
    ```
3.  **Visualize**: Open the Dashboard at `/dashboard/`, paste your **Site ID**, and watch the live data flow in!

---

## 📁 Project Structure

*   `analytic_core/`: The heart of the system (Models, Logic, Reports).
    *   `reports/`: Logic for aggregating data into dashboard metrics.
    *   `services/`: Intelligent engines (Bot detection, GeoIP, Session logic).
*   `static/`: Contains the production-ready `tracker.js`.
*   `templates/`: The professional HTML dashboards and integration UI.
*   `main_analytic/`: Primary Django configuration.

---

## 🛡️ License
Designed and Developed with ❤️ for High-Performance Analytics.
