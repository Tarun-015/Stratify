"""
setup_stratify.py

Run this once to create the entire Stratify project structure.
Usage: python setup_stratify.py
"""

from pathlib import Path

# ── Folders to create ─────────────────────────────────────────────────────────

FOLDERS = [
    "stratify/data",
    "stratify/models/engagement_clustering",
    "stratify/models/genre_saturation",
    "stratify/models/prize_hype_ratio",
    "stratify/models/team_dominance",
    "stratify/models/growth_efficiency",
    "stratify/models/tournament_stability",
    "stratify/dashboard/pages",
    "stratify/utils",
    "data/raw",
    "data/processed",
    "saved_models",
    "notebooks",
    "scripts",
    "tests",
    ".github/workflows",
]

# ── Empty files to create ─────────────────────────────────────────────────────

FILES = [
    # Package init files
    "stratify/__init__.py",
    "stratify/data/__init__.py",
    "stratify/models/__init__.py",
    "stratify/models/engagement_clustering/__init__.py",
    "stratify/models/genre_saturation/__init__.py",
    "stratify/models/prize_hype_ratio/__init__.py",
    "stratify/models/team_dominance/__init__.py",
    "stratify/models/growth_efficiency/__init__.py",
    "stratify/models/tournament_stability/__init__.py",
    "stratify/dashboard/__init__.py",
    "stratify/utils/__init__.py",
    "tests/__init__.py",

    # Model files — one set per model
    "stratify/models/engagement_clustering/train.py",
    "stratify/models/engagement_clustering/predict.py",
    "stratify/models/engagement_clustering/evaluate.py",

    "stratify/models/genre_saturation/train.py",
    "stratify/models/genre_saturation/predict.py",
    "stratify/models/genre_saturation/evaluate.py",

    "stratify/models/prize_hype_ratio/train.py",
    "stratify/models/prize_hype_ratio/predict.py",
    "stratify/models/prize_hype_ratio/evaluate.py",

    "stratify/models/team_dominance/train.py",
    "stratify/models/team_dominance/predict.py",
    "stratify/models/team_dominance/evaluate.py",

    "stratify/models/growth_efficiency/train.py",
    "stratify/models/growth_efficiency/predict.py",
    "stratify/models/growth_efficiency/evaluate.py",

    "stratify/models/tournament_stability/train.py",
    "stratify/models/tournament_stability/predict.py",
    "stratify/models/tournament_stability/evaluate.py",

    # Data layer
    "stratify/data/db.py",
    "stratify/data/loader.py",
    "stratify/data/validator.py",

    # Dashboard
    "stratify/dashboard/app.py",
    "stratify/dashboard/components.py",
    "stratify/dashboard/pages/1_engagement.py",
    "stratify/dashboard/pages/2_genre_risk.py",
    "stratify/dashboard/pages/3_prize_hype.py",
    "stratify/dashboard/pages/4_team_dominance.py",
    "stratify/dashboard/pages/5_growth_efficiency.py",
    "stratify/dashboard/pages/6_tournament_stability.py",

    # Utils
    "stratify/utils/logger.py",
    "stratify/utils/helpers.py",

    # Scripts
    "scripts/train_all.py",
    "scripts/seed_db.py",

    # Tests
    "tests/conftest.py",
    "tests/test_engagement.py",
    "tests/test_genre.py",
    "tests/test_prize_hype.py",
    "tests/test_team_dominance.py",
    "tests/test_growth_efficiency.py",
    "tests/test_tournament_stability.py",

    # Config files
    ".env.example",
    ".gitignore",
    "pyproject.toml",
    "README.md",
    ".github/workflows/ci.yml",
]

# ── Script ────────────────────────────────────────────────────────────────────

def create_structure():
    base = Path.cwd()
    print(f"\nCreating Stratify structure in: {base}\n")

    # Create folders
    for folder in FOLDERS:
        path = base / folder
        path.mkdir(parents=True, exist_ok=True)
        print(f"  [folder] {folder}")

    print()

    # Create files
    for file in FILES:
        path = base / file
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.touch()
            print(f"  [file]   {file}")
        else:
            print(f"  [skip]   {file} already exists")

    print("\n✓ Done. Your Stratify project structure is ready.")
    print("\nNext steps:")
    print("  1. Copy .env.example to .env and fill in your credentials")
    print("  2. Run: pip install -e .[dev]")
    print("  3. Run: python scripts/seed_db.py")
    print("  4. Run: python scripts/train_all.py")
    print("  5. Run: streamlit run stratify/dashboard/app.py")

if __name__ == "__main__":
    create_structure()
