# Flight Price Prediction Web App

This project is a Django-based web application that uses machine learning to analyze flight data, predict ticket prices, and provide real-time flight booking insights.

The application allows users to search for flights using origin and destination airports along with a desired departure date. Live flight data is retrieved through SerpAPI and processed using a trained machine learning pipeline to generate price predictions.

Search results are organized based on ticket price and include both live and historical analytics such as average, minimum, and maximum route prices to support more informed booking decisions.

## 🧰 Tech Stack
| Category | Technologies |
|---|---|
| Backend | Python, Django, SQLite |
| Machine Learning & Data Processing | scikit-learn, Pandas, Random Forest Regressor, joblib, .pkl model serialization |
| APIs | SerpAPI, Amadeus API, REST APIs |
| Frontend | HTML, Tailwind CSS, JavaScript |
| Development Tools | Git, GitHub |
