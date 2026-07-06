# PRODUCT REQUIREMENTS DOCUMENT (PRD)

## Stratify v1.0 - Machine Learning Analytics Platform

**Version:** 1.0

**Status:** Completed

**Project Duration:** May 2025 – September 2025

**Author:** Tarun Chaudhary

**Project Type:** Machine Learning Analytics Platform

---

# 1. Product Overview

## Product Summary

Stratify is a machine learning-based analytics platform designed to evaluate the esports and creator economy using data-driven metrics. Instead of relying on raw statistics such as prize pools, subscriber counts, or tournament earnings, the platform transforms historical datasets into interpretable scores that help users compare market opportunities, competitive performance, and creator growth.

The first release focuses on building an end-to-end machine learning pipeline that integrates multiple analytical models within a single Streamlit application.

---

# 2. Problem Statement

Current esports analytics rely heavily on isolated metrics such as tournament prize pools, subscriber counts, or total earnings. These metrics provide limited insight into ecosystem health or long-term sustainability.

Key challenges include:

* No unified platform combining tournament, team, and creator analytics.
* Difficulty comparing different esports genres using standardized metrics.
* Limited analytical tools for sponsors, investors, and creators.
* Public datasets remain fragmented across multiple sources.
* Most dashboards present descriptive statistics rather than actionable insights.

---

# 3. Product Vision

Develop an analytics platform that enables stakeholders in the esports ecosystem to evaluate tournaments, teams, genres, and creators through machine learning-driven insights rather than isolated performance metrics.

---

# 4. Objectives

### Primary Objectives

* Build a centralized analytics platform.
* Develop six custom analytics models.
* Integrate machine learning with interactive visualizations.
* Store processed data in PostgreSQL.
* Deliver an interactive Streamlit dashboard.
* Demonstrate end-to-end ML workflow from data preprocessing to prediction.

---

# 5. Stakeholders

| Stakeholder     | Role                                    |
| --------------- | --------------------------------------- |
| Tarun Chaudhary | Product Owner & ML Developer            |
| Academic Mentor | Project Reviewer                        |
| End Users       | Sponsors, Investors, Creators, Analysts |

---

# 6. Target Users

| User                  | Primary Need                                               |
| --------------------- | ---------------------------------------------------------- |
| Sponsors              | Evaluate market opportunities before sponsorship decisions |
| Investors             | Assess long-term tournament stability                      |
| Esports Organizations | Compare team performance                                   |
| Content Creators      | Benchmark growth and engagement                            |
| Data Enthusiasts      | Explore esports analytics                                  |

---

# 7. Scope

## In Scope

* Tournament analytics
* Creator analytics
* Team analytics
* Machine learning models
* PostgreSQL database
* Streamlit dashboard
* Interactive visualizations
* Basic model evaluation

### Out of Scope

* Live API integration
* Real-time predictions
* User authentication
* Cloud deployment
* Mobile application
* Automated retraining
* CI/CD automation
* Docker deployment

---

# 8. Data Sources

| Dataset                    | Purpose              |
| -------------------------- | -------------------- |
| Esports Tournament Dataset | Tournament analytics |
| Esports Team Dataset       | Team performance     |
| YouTube Creator Dataset    | Creator analytics    |
| PostgreSQL Database        | Structured storage   |

### Data Characteristics

* Static datasets
* CSV format
* Manual preprocessing
* Historical records only

---

# 9. System Architecture

```text
CSV Datasets
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Machine Learning Models
      │
      ▼
PostgreSQL Database
      │
      ▼
Streamlit Dashboard
```

---

# 10. Machine Learning Pipeline

| Stage               | Description                          |
| ------------------- | ------------------------------------ |
| Data Collection     | Import CSV datasets                  |
| Data Cleaning       | Remove duplicates and missing values |
| Feature Engineering | Generate analytical features         |
| Model Development   | Train analytical models              |
| Prediction          | Generate scores                      |
| Storage             | Save processed data in PostgreSQL    |
| Visualization       | Display results in Streamlit         |

---

# 11. Machine Learning Models

| Model                      | Objective                               | Technique                  |
| -------------------------- | --------------------------------------- | -------------------------- |
| Genre Saturation Risk      | Estimate competitiveness of game genres | Regression-based scoring   |
| Prize-to-Hype Ratio        | Compare prize pool against popularity   | Custom analytical metric   |
| Tournament Stability Score | Measure tournament ecosystem stability  | Regression model           |
| Team Dominance Index       | Rank team performance                   | Weighted scoring algorithm |
| Growth Efficiency Index    | Measure creator growth efficiency       | Regression model           |
| Engagement Clustering      | Segment creators based on engagement    | K-Means Clustering         |

---

# 12. Functional Requirements

| ID    | Requirement                             | Priority |
| ----- | --------------------------------------- | -------- |
| FR-01 | Import datasets into PostgreSQL         | High     |
| FR-02 | Clean and preprocess datasets           | High     |
| FR-03 | Generate analytical features            | High     |
| FR-04 | Train six ML models                     | High     |
| FR-05 | Display predictions in Streamlit        | High     |
| FR-06 | Allow model selection through dashboard | Medium   |
| FR-07 | Store processed outputs                 | Medium   |
| FR-08 | Visualize analytics using charts        | High     |

---

# 13. Non-Functional Requirements

| ID     | Requirement                                 |
| ------ | ------------------------------------------- |
| NFR-01 | Dashboard response time under 5 seconds     |
| NFR-02 | Local execution without internet dependency |
| NFR-03 | Reproducible ML pipeline                    |
| NFR-04 | Compatible with PostgreSQL                  |
| NFR-05 | Modular Python codebase                     |

---

# 14. Technology Stack

| Layer                | Technology   |
| -------------------- | ------------ |
| Programming Language | Python       |
| Database             | PostgreSQL   |
| Dashboard            | Streamlit    |
| Data Processing      | Pandas       |
| Machine Learning     | Scikit-learn |
| Visualization        | Matplotlib   |
| Database Connector   | psycopg2     |
| Version Control      | Git & GitHub |

---

# 15. Success Metrics

| Metric                     | Target                 |
| -------------------------- | ---------------------- |
| ML Models Developed        | 6                      |
| Dashboard Modules          | 1 Integrated Dashboard |
| Database Integration       | Completed              |
| Interactive Visualizations | Available              |
| End-to-End Pipeline        | Functional             |
| Model Outputs Generated    | Successful             |

---

# 16. Engineering Limitations

| Area            | Limitation                                 |
| --------------- | ------------------------------------------ |
| Data Collection | Static CSV datasets                        |
| Database        | Local PostgreSQL only                      |
| Security        | Hardcoded database credentials             |
| Deployment      | Local execution only                       |
| Validation      | Limited model evaluation                   |
| Testing         | Minimal automated testing                  |
| CI/CD           | Not implemented                            |
| Docker          | Not available                              |
| Team Dataset    | Limited sample size (47 records)           |
| Explainability  | No feature importance or confidence scores |

---

# 17. Project Timeline

| Month              | Phase                   | Activities                                                                        | Deliverables                        |
| ------------------ | ----------------------- | --------------------------------------------------------------------------------- | ----------------------------------- |
| **May 2025**       | Requirement Analysis    | Problem definition, literature review, dataset identification, metric ideation    | Project proposal, dataset shortlist |
| **June 2025**      | Data Preparation        | Dataset collection, cleaning, preprocessing, PostgreSQL setup                     | Clean datasets, database schema     |
| **July 2025**      | Model Development       | Feature engineering, implementation of six analytical models, initial evaluation  | Functional ML models                |
| **August 2025**    | Dashboard Development   | Streamlit dashboard integration, database connectivity, visualization development | Interactive analytics dashboard     |
| **September 2025** | Testing & Documentation | Functional testing, debugging, documentation, GitHub repository preparation       | Final project release (v1.0)        |

---

# 18. Acceptance Criteria

The project is considered complete when:

* Six analytical models are implemented.
* All datasets are successfully processed.
* PostgreSQL stores processed data correctly.
* Dashboard displays outputs from all models.
* End-to-end workflow executes without errors.
* Source code is documented and available through GitHub.

---

# 19. Future Roadmap (Towards Version 2.0)

The first version establishes the core analytics platform. The next release will focus on transforming the project into a production-ready machine learning system by addressing the engineering and data limitations identified in Version 1. Planned improvements include:

* Expanding datasets from multiple sources to improve model reliability.
* Building an automated ETL pipeline for data ingestion and validation.
* Improving feature engineering and model validation techniques.
* Introducing model explainability and confidence metrics.
* Replacing hardcoded credentials with secure environment variables.
* Containerizing the application using Docker for reproducible deployment.
* Implementing automated testing and CI/CD pipelines.
* Enhancing the dashboard with advanced filtering, model insights, and performance metrics.
