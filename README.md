# CLOUD-BASED-AI-POWERED-EXPENSE-TRACKER
**Project Overview**
The Cloud-Based AI Expense Tracker is a web application designed to help users manage and analyze their personal finances easily. It allows users to record income and expenses, automatically categorize transactions using AI, and view insights through interactive charts.

**Features & Modules**
The system consists of five fully integrated modules:  
-User Management: Secure registration, login, and profile management.  
-Expense Entry: Allows users to add, view, edit, and delete expense entries with ML-based category prediction.  
-Income Management: Facilitates the recording and tracking of user income.  
-Analytics: Provides interactive charts (pie, bar, line) using Chart.js to visualize spending patterns, category-wise breakdowns, savings rate calculations, and AI-driven financial insights. 
Data Backup & Export: Enables a one-click download of structured financial reports in .xlsx format using openpyxl and automates JSON backups to Google Drive via the official Google Drive API.  

**Tech Stack**
Frontend: HTML, CSS (Tailwind CSS), and JavaScript (located in the aianfrontend/ folder).  
Backend: Python Flask providing RESTful API endpoints (located in the aianbackend/ folder).  
Database: Supabase (PostgreSQL-based cloud database) configured with Row Level Security (RLS) for real-time, multi-user access.  
Libraries & APIs: Chart.js for visualization, openpyxl for Excel export, and Google Drive API (v3) for cloud backups. 

**Architecture**
The project follows a clean, modular, full-stack cloud-based architecture. The frontend provides a responsive dashboard with live data binding, which communicates securely via HTTP requests to the Flask backend. The backend handles logic, AI analytics, and database interactions with Supabase.

**Team Information**
-Aanya Godiyal: Expense Entry Module (with ML category prediction, CRUD, Flask backend integration), and Integration of all modules (Expense + Income + Dashboard). -Aanya Punj: Analytics Module (use of AI) and Data Backup and Export.  
-Aditya Negi: Database (Supabase) Setup and User Management Module.  
-Apurwa Jain: Income Module. 
