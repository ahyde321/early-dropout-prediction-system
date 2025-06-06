# Early Dropout Prediction System (EDPS)

## Project Overview

The Early Dropout Prediction System (EDPS) is a full-stack web application designed to help academic advisors and administrators proactively identify students at risk of dropping out. By combining machine learning models with an intuitive dashboard interface, EDPS provides early insights and allows for timely interventions to improve student retention.

## Features

- Predicts dropout risk using trained ML models (Random Forest, KNN, Logistic Regression)
- Dynamic model routing based on data availability (early/mid/final phase)
- Risk scores visualized with breakdowns and trends
- Feature selection using ANOVA F-test and chi-squared tests
- CSV import of student and grade data
- SHAP explainability for insight into predictions
- Real-time notification system for advisors and admins
- Filter, sort, and search students by name, ID, risk level, or score
- Vue 3 + Tailwind UI with adaptive layout
- Docker-ready deployment

## Installation

### Backend (FastAPI)

1. Clone the repository:
```bash
git clone https://gitlab.eeecs.qub.ac.uk/40328713/early-dropout-prediction-system.git
cd early-dropout-prediction-system
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run the backend server:
```bash
uvicorn main:app --reload
```

### Frontend (Vue 3)

1. Navigate to the frontend directory (e.g. `edps-dashboard`):
```bash
cd edps-dashboard
```

2. Install dependencies:
```bash
npm install
```

3. Run the frontend dev server:
```bash
npm run dev
```

The app should now be accessible at http://localhost:8080/


## Usage

- Login as an admin or advisor
- Upload students or grades via CSV
- Trigger predictions from the dashboard
- View, filter, and sort students by risk level
- Navigate to individual profiles
- Admins receive bulk and summary notifications on key actions (e.g., prediction runs)

## Project Structure

```
.
├── backend
│   ├── api
│   ├── db
│   ├── models
│   └── main.py
├── edps-dashboard
│   ├── components
│   ├── views
│   └── App.vue
├── models
│   ├── utils
│   ├── trained_models
├── data
│   ├── raw
│   └── processed
└── docker-compose.yml
```

## Tech Stack

- Frontend: Vue 3, Tailwind CSS, Pinia, Vue Router
- Backend: FastAPI, SQLAlchemy, Pydantic
- ML: scikit-learn, pandas, numpy, SHAP
- Database: PostgreSQL
- Notifications: Real-time alerts via API
- Auth: JWT-based advisor login
- Deployment: Docker + Docker Compose

## Roadmap

- [x] Add student filtering, sorting, and risk visualizations
- [x] Add SHAP explanations per prediction
- [x] CSV-based bulk student and grade uploads
- [x] Admin-only views for insights and high-risk spikes
- [x] Dynamic model phase selection (early, mid, final)
- [ ] Add model retraining from UI
- [x] Enable secure role-based API endpoints
- [ ] Deploy live on university server or cloud (e.g., AWS, Heroku)

## Author

- Andrew Hyde  
  Computer Science, Queen's University Belfast

## Supervisor

- Dr. Baharak Ahmaderaghi

## Acknowledgments

Thanks to Queen’s University Belfast and the School of Electronics, Electrical Engineering and Computer Science for project support and guidance.
