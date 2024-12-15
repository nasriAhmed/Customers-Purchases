# Customer and Purchase Data Processor

## Description
Python app using Flask to process customer and purchase data from CSV files, format it to JSON, and send it to an external REST API. Includes a CLI for automation.

## Project Structure
```
/python_app/
    ├── app/
    │   ├── __init__.py        # Initialisation de l'application Flask
    │   ├── routes.py          # Routes API
    │   ├── utils/
    │   │   ├── __init__.py    # Initialisation du package utils
    │   │   ├── logger.py      # Configuration des logs
    │   │   ├── csv_parser.py  # Lecture et traitement des fichiers CSV
    │   │   ├── json_formatter.py  # Formatage des données pour l'API
    │   │   ├── api_client.py  # Envoi des données à l'API
    ├── run.py                 # Point d'entrée de l'application Flask
    ├── cli.py                 # Interface CLI
    ├── requirements.txt       # Dépendances Python
    ├── static/
    │   ├── customers.csv      # Exemple de fichier clients
    │   ├── purchases.csv      # Exemple de fichier achats
    └── logs/
        └── (Fichiers de logs générés automatiquement)
```

## Features
- **CSV Processing**: Parses `customers.csv` and `purchases.csv`, formats data for the API.
- **Flask API**: Endpoints to process and send data.
- **CLI**: Automates CSV processing and data sending.
- **Logging**: Generates unique log files for each execution.

## Installation
### Prerequisites
- Python 3.9
- Pip

### Steps
1. Clone the repo:
    ```bash
    git clone <REPO_URL>
    cd python_app
    ```
2. (Optional) Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage
1. **Start Flask App**:
    ```bash
    python run.py
    ```
2. **Use CLI**:
    ```bash
    python cli.py --customers-file static/customers.csv --purchases-file static/purchases.csv --api-url https://myhostname.com/v1/customers
    ```

## Testing
1. Use Postman or curl to test the API.
2. Ensure `customers.csv` and `purchases.csv` are correctly formatted.
3. Validate data sending with a tool like httpbin.org:
    ```bash
    python cli.py --customers-file static/customers.csv --purchases-file static/purchases.csv --api-url https://httpbin.org/put
    ```

**Author**: Ahmed Nasri
