# Euroleague Chatbot (ETL + SQL RAG)

This project consists of two main parts:

1. **ETL pipeline** – fetches and prepares EuroLeague basketball data and stores it in a SQLite database  
2. **Chatbot** – a natural language interface that answers questions by generating SQL queries over the database and explaining the results

The chatbot does **not** have access to all data at once.  
Instead, it dynamically generates SQL queries based on the user question, executes them, and then explains the results.

## Database Schema

The SQLite database (`euroleague.db`) contains the following tables:

- **games** – match results and schedules  
- **players** – basic player information  
- **players_average_stats** – season-level average player statistics  
- **players_teams** – mapping between players and teams  
- **teams** – team codes and names  

These tables are connected through foreign keys and are designed to be queried together using SQL JOINs.

## ETL Pipeline

The ETL process is responsible for:
- Fetching EuroLeague data
- Transforming it into a clean, structured format
- Loading it into the SQLite database

### How to Run ETL

1. Navigate to the `etl` folder:
   ```bash
   cd etl
   python main.py
   ```
When prompted, enter the season you want to load data for (e.g. 2024) and the script will populate or update euroleague.db with data for the selected season.

## Chatbot (SQL RAG System)

The chatbot provides a natural language interface for querying the EuroLeague SQLite database.

### Architecture Overview

The chatbot works in **four clearly separated steps**:

1. **Retrieving tables info**
    - Takes the user's natural language question
    - Use vector search to retrieve needed tables

2. **SQL Generation**
   - Takes the user’s natural language question
   - Uses only the database schema and retrieved table descriptions
   - Generates a valid **SQLite SQL query**

3. **Query Execution (Application Layer)**
   - The generated SQL query is executed against `euroleague.db`
   - No LLM has direct access to the database

4. **Answer Generation**
   - Receives the raw SQL query results
   - Produces a clear, human-readable answer

This design ensures:
- full control over database access
- debuggable and explainable behavior
- no hallucinated data

### How to Run the Chatbot

1. Navigate to the `chatbot` folder:
   ```bash
   cd chatbot
   python bot.py
   ```

2. Ask questions in natural language, for example:
    - Which teams played in round 1?
    - What team does a specific player play for?
    - Show average stats for a given player
    - List games where ALBA Berlin was the home team

3. To exit the chatbot, type:
    ```bash
    exit
    ```
    or
    ```bash
    quit
    ```