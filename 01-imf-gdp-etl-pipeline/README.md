# 🌍 IMF Global GDP ETL Pipeline

An automated **Extract, Transform, Load (ETL)** pipeline built in Python to collect nominal GDP rankings published by the International Monetary Fund (IMF), standardize currency units, and persist the processed data into both **CSV** and **SQLite** formats for downstream querying.

## 📌 Business Scenario

An international organization evaluating global expansion opportunities requires a repeatable, automated script to track countries ranked by their nominal GDP (in billions of USD). Because the IMF updates these figures biannually, this pipeline is designed to extract, transform, and store updated records on demand, log each execution stage, and query economies exceeding **$100 billion USD**.

---

## ⚙️ Pipeline Architecture & Functions

The script `etl_project_gdp.py` is structured into modular functions covering the full ETL lifecycle:

1. **`extract(url, table_attribs)`**: Scrapes the target web page using `requests` and `BeautifulSoup` to parse the IMF nominal GDP table into a raw `pandas` DataFrame.
2. **`transform(df)`**: Cleans currency strings, converts values from millions to **billions of USD** rounded to 2 decimal places using `numpy`, and standardizes column schemas.
3. **`load_to_csv(df, csv_path)`**: Exports the transformed dataset to `Countries_by_GDP.csv`.
4. **`load_to_db(df, sql_connection, table_name)`**: Persists the records into the `Countries_by_GDP` table inside `World_Economies.db` (`SQLite`).
5. **`run_query(query_statement, sql_connection)`**: Executes SQL validation queries against the database (filtering economies where `GDP_USD_billion > 100`) and outputs results to the console.
6. **`log_progress(message)`**: Appends timestamped audit entries to `etl_project_log.txt` throughout execution.

---

## 🛠️ Tech Stack

* **Language:** Python
* **Data Processing:** `pandas`, `numpy`
* **Web Scraping:** `requests`, `beautifulsoup4`
* **Database & Logging:** `sqlite3`, `datetime`
