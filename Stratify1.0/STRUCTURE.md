# Stratify — new folder structure

## How to migrate

Run these commands in your repo root to create the new structure:

```bash
mkdir -p src/stratify/models
mkdir -p src/stratify/data
mkdir -p src/stratify/api
mkdir -p src/stratify/utils
mkdir -p tests
mkdir -p notebooks
mkdir -p data/raw
mkdir -p data/processed
mkdir -p saved_models
mkdir -p .github/workflows
touch src/__init__.py
touch src/stratify/__init__.py
touch src/stratify/models/__init__.py
touch src/stratify/data/__init__.py
touch src/stratify/api/__init__.py
touch src/stratify/utils/__init__.py
touch tests/__init__.py
```

Then move your existing files:
```bash
# Move ML model scripts
mv ML_models/*.py src/stratify/models/

# Move data files
mv Data-collection/  data/raw/
mv Final-data/       data/processed/

# Move notebooks if any
mv *.ipynb notebooks/  2>/dev/null || true
```

## Final structure

```
Stratify/
│
├── src/
│   └── stratify/
│       ├── __init__.py
│       ├── models/
│       │   ├── __init__.py
│       │   ├── genre_risk.py          ← Genre Saturation Risk model
│       │   ├── team_dominance.py      ← Team Dominance Index model
│       │   ├── growth_efficiency.py   ← Growth Efficiency Index model
│       │   ├── tournament_stability.py← Tournament Stability Score model
│       │   ├── engagement_clusters.py ← Engagement Clustering model
│       │   └── prize_hype_ratio.py    ← Prize-to-Hype Ratio model
│       │
│       ├── data/
│       │   ├── __init__.py
│       │   ├── loader.py              ← load CSVs from data/processed/
│       │   └── validator.py           ← schema validation helpers
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   └── main.py                ← FastAPI app (Phase 3)
│       │
│       └── utils/
│           ├── __init__.py
│           └── helpers.py             ← shared utility functions
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                    ← shared pytest fixtures
│   ├── test_data_loader.py            ← data schema & loading tests
│   ├── test_genre_risk.py
│   ├── test_team_dominance.py
│   ├── test_growth_efficiency.py
│   ├── test_tournament_stability.py
│   ├── test_engagement_clusters.py
│   └── test_prize_hype_ratio.py
│
├── data/
│   ├── raw/                           ← original collected data (gitignored)
│   └── processed/                     ← cleaned final datasets
│       ├── tournaments.csv
│       ├── teams.csv
│       ├── games.csv
│       └── youtube_creators.csv
│
├── saved_models/                      ← serialized .pkl files (gitignored)
│
├── notebooks/                         ← EDA and exploration notebooks
│
├── .github/
│   └── workflows/
│       └── ci.yml                     ← GitHub Actions CI pipeline
│
├── .env                               ← LOCAL ONLY — never commit
├── .env.example                       ← template — safe to commit
├── .gitignore
├── requirements.txt
├── requirements-dev.txt               ← test/dev dependencies
├── README.md
└── LICENSE
```
