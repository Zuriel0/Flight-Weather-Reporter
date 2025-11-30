# Flight Weather Reporter

This project is a Python-based tool that generates a comprehensive report correlating flight tickets with current weather conditions at both origin and destination airports. It is designed to efficiently process large datasets by leveraging asynchronous programming and caching mechanisms.

## 🚀 Features

- **Data Loading**: Parses flight ticket and airport data from CSV datasets.
- **Weather Integration**: Fetches real-time weather data (temperature and description) for airports using their geolocation (latitude/longitude).
- **High Performance**:
  - **Asynchronous Processing**: Uses `asyncio` and `aiohttp` for concurrent API requests.
  - **Concurrency Control**: Limits the number of simultaneous requests to avoid hitting API rate limits.
  - **Caching**: Implements a disk-based cache to prevent redundant API calls for the same airport on the same day.
- **Reporting**: Generates a CSV report combining flight details with weather metrics.

## 🛠️ Prerequisites

- Python 3.8+
- A valid API key for [WeatherAPI](https://www.weatherapi.com/) (or the configured weather provider).

## 📦 Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository-url>
    cd ECOM
    ```

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    # Windows
    venv\Scripts\activate
    # macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies**:
    *(Note: Ensure you have `aiohttp` and `pydantic-settings` installed. If a `requirements.txt` is present, use that.)*
    ```bash
    pip install aiohttp pydantic-settings
    ```

## ⚙️ Configuration

The application uses environment variables for configuration. Create a `.env` file in the root directory or set them in your environment:

```env
WEATHER_API_KEY=your_api_key_here
DATASET_PATH=path/to/your/dataset.csv
OUTPUT_PATH=output_report.csv
CONCURRENCY_LIMIT=10
CACHE_PATH=.cache
```

## 🏃 Usage

Run the main application script:

```bash
python src/main.py
```

The script will:
1.  Load the dataset specified in `DATASET_PATH`.
2.  Identify unique airports.
3.  Fetch weather data for each airport (using cache if available).
4.  Generate a report at `OUTPUT_PATH`.

## 📂 Project Structure

```
ECOM/
├── src/
│   ├── data/              # Data storage (if applicable)
│   ├── utils/             # Utility modules (e.g., caching)
│   ├── config.py          # Configuration management
│   ├── data_loader.py     # CSV data loading logic
│   ├── main.py            # Entry point of the application
│   ├── models.py          # Data models (Ticket, Airport, Weather)
│   ├── report.py          # Report generation logic
│   ├── weather_client.py  # API client for weather service
│   └── weather_service.py # Business logic for weather fetching & caching
├── tests/                 # Test suite
└── README.md              # Project documentation
```

## 📝 Input Data Format

The input CSV should contain at least the following columns (based on `data_loader.py`):
- `origin`, `destination`, `airline`, `flight_num`
- `origin_iata_code`, `origin_name`, `origin_latitude`, `origin_longitude`
- `destination_iata_code`, `destination_name`, `destination_latitude`, `destination_longitude`
