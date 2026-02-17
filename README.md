# 🚀 Projekt TCL - Database & Transaction Management

Ky projekt, i emërtuar **"Projekt TCL"**, është një sistem i integruar i menaxhimit të transaksioneve që përdor **Oracle Database** dhe një ndërfaqe vizuale në **Python**. Sistemi fokusohet në sigurinë e të dhënave, menaxhimin e përdoruesve dhe kontrollin e transaksioneve (TCL).

## 👥 Grupi i Punës
* **Leader:** Deniz Ikili
* **Anëtarët:** Gridi Çupi, Ergi Kelo, Nataniel Bejtja

---

## 🛠️ Kërkesat Paraprake (Prerequisites)
Për të nisur këtë projekt, duhet të keni të instaluar:
1. **Oracle Database XE** (versioni 18c ose 21c).
2. **VS Code** me extension-in "Oracle SQL Developer".
3. **Python 3.10+**.

---

## 🚀 Udhëzuesi i Nisjes (Getting Started)

### 1. Konfigurimi i Database-it
1. Hapni VS Code dhe lidhuni me Oracle si `SYSDBA` (Fjalëkalimi: `123456`).
2. Ekzekutoni skriptin `database_master.sql`. Ky skript:
   - Pastron çdo mbetje të mëparshme (Drop if exists).
   - Krijon tabelat dhe përdoruesit e rinj.
   - Instalon procedurat PL/SQL.

### 2. Konfigurimi i Python
1. Hapni terminalin në folderin e projektit.
2. Instaloni libraritë e nevojshme:
   ```bash```bash
   pip install oracledb streamlit pandas pyplot plotly
   ``````
3.Nisni programin 
   ``````
    python -m streamlit run app.py
   ``````
