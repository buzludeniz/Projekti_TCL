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
1. Hapni VS Code dhe lidhuni me Oracle si `SYSDBA` (me fjalëkalimin që keni caktuar gjatë instalimit të Oracle; mos e shkruani në repo).
2. Ekzekutoni skriptin `query1.sql`. Ky skript:
   - Pastron çdo mbetje të mëparshme (Drop if exists).
   - Krijon tabelat dhe përdoruesit e rinj.
   - Instalon procedurat PL/SQL.

### 2. Konfigurimi i Python
1. Hapni terminalin në folderin e projektit.
2. Instaloni libraritë e nevojshme:
   ``````
   pip install -r requirements.txt
   ``````
3. Vendosni kredencialet e database-it në variabla mjedisi. Kopjoni skedarin shembull dhe plotësoni vlerat tuaja (skedari `.env` nuk ngarkohet në git):
   ``````
   cp .env.example .env
   ``````
   Variablat: `DB_USER`, `DB_PASSWORD`, `DB_DSN` (default `localhost:1521/XEPDB1`) dhe `DB_SYSDBA=true` nëse lidheni si `SYSDBA`. Mund t'i vendosni edhe direkt në terminal, p.sh. `export DB_PASSWORD=...` (Linux/macOS) ose `$env:DB_PASSWORD="..."` (PowerShell).
4. Nisni programin
   ``````
    python -m streamlit run app.py
   ``````

---

## English summary

Projekt TCL is a university group project (team lead: Deniz Ikili) on
transaction control in Oracle Database, with a Streamlit front end for a small
sales-management system.

**Database (`query1.sql`)**
- Tables `Shitjet` (sales) and `Audit_Log`.
- Three database users with different privileges: an admin with full DML on
  sales, a developer, and a read-only analyst.
- PL/SQL procedure `shto_transaksion_shitje` inserts a sale and logs it. It
  rejects non-positive amounts (logging the blocked attempt) and rolls back on
  any error.
- PL/SQL procedure `fshi_transaksion_shitje` deletes a sale by id after checking
  it exists, logs the result, and rolls back on failure.

**App (`app.py`)**
- Streamlit UI with three tabs: data management (add or delete a sale through
  the stored procedures, latest records), charts (sales by product, share by
  user, sales over time with Plotly), and project info.
- Connects with `python-oracledb`.

**Run it**
1. Install Oracle Database XE (18c or 21c) and run `query1.sql` as `SYSDBA`.
2. `pip install -r requirements.txt`
3. `cp .env.example .env` and fill in `DB_USER`, `DB_PASSWORD` (and `DB_SYSDBA=true` if connecting as SYSDBA); the app reads them from the environment.
4. `python -m streamlit run app.py`
