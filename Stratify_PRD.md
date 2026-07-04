# Stratify — Product Requirements Document
### Esports & Creator Economy Analytics Project
Author: Tarun Chaudhary

---

# Part 1: Version 1.0 (as built)

## Title
Stratify — Esports and Creator Economy Analytics Tool

## Problem Statement
People who follow esports and the creator economy — sponsors, small investors, creators themselves — usually judge things using surface numbers: subscriber count, prize pool size, view counts. These numbers don't tell you if a genre is oversaturated, if a tournament scene is stable, or if a creator's growth is actually healthy or just a temporary spike. Stratify tries to turn raw earnings and engagement data into a few simple scores that say something more useful than the raw numbers alone.

## Background
This started as a personal/college project to practice working with real-world-style data across three areas — esports tournaments, esports teams, and YouTube creators — and to build a few original metrics instead of just using standard dashboards. It's not a funded product, there's no company behind it, and it hasn't been shown to real sponsors or investors — it's a learning project meant to demonstrate data analysis, Python, and basic ML skills.

## Goals
- Build 6 different scores/metrics across the three data areas (tournaments, teams, creators).
- Show all of them in one simple app (built with Streamlit) so they can be explored interactively.
- Make sure the whole thing — from raw data to trained model to output — can be run again from scratch.

## Success Metrics
Right now, "success" for v1.0 basically means: all six models run without crashing, and the app lets you switch between them. That's it — there's no defined accuracy target or real-world validation, because this hasn't been tested against actual outcomes. Worth saying honestly: for a project that claims to help with "risk" decisions, not having any actual measure of whether the risk score is correct is a real gap, not a small detail.

## Target Users
- Sponsors deciding whether to back a game genre
- Investors deciding whether a tournament scene is stable long-term
- Creators wanting to see how they compare to others
- Team organizers wanting to show competitive standing

## User Personas
Three rough personas were sketched out (a sponsorship manager, an angel investor, a growing YouTuber) to help think through what each type of user might want. To be clear — these are made up for the purpose of thinking through the project, not based on interviews or actual users. That's normal for a college project, but it shouldn't be presented as "user research" if asked, since none was actually done.

## User Stories
- As a sponsor, I want to check a genre's saturation score so I can skip genres that look risky.
- As an investor, I want to see a tournament's stability score so I can judge if it's worth backing.
- As a creator, I want to know which engagement group I fall into so I can compare myself to others.
- As a team, I want to see my dominance score so I can show it to potential sponsors.

## Scope
- Genre Saturation Risk score
- Prize-to-Hype Ratio score
- Team Dominance Index
- Growth Efficiency Index
- Engagement Clustering (grouping creators by engagement level)
- Tournament Stability Score
- One Streamlit app to view all six

## Out of Scope
- Live data collection (scraping in real time) — data used here is static CSV files, not a live feed
- A proper API
- Automated testing or CI/CD
- Hosting it anywhere other than a local computer
- Any login/user accounts
- Proper handling of passwords/credentials (this was skipped in v1.0, which is a real problem — explained below)

## Functional Requirements
- Each of the six models should take in the relevant dataset and output its score.
- The Streamlit app should let a user pick which model they want to see and get a result.

## Non-Functional Requirements
Not really defined for v1.0 — there was no target for speed, reliability, or security when this was built. That's a gap, because it's exactly why the password ended up hardcoded in the code (see below) — nobody had written down "don't do that" as a requirement before building it.

## Assumptions
- Past earnings/engagement data is a decent stand-in for future risk/performance — this was assumed, not tested.
- The three datasets are roughly comparable in terms of when/how they were collected — also assumed, not confirmed, since there's no documentation of where each dataset actually came from or when it was pulled.

## Dependencies
- A local PostgreSQL database
- Python libraries: pandas, scikit-learn, psycopg2, streamlit
- CSV files that were manually put together, not pulled live from any API despite an API key being referenced in the setup files

## Constraints
- The team-level dataset only has 47 rows. That's just not enough data to build a real model on — this is a data problem, not something more coding can fix.
- This is a one-person project, so anything that sounds like a "pipeline" should really be understood as "some scripts one student wrote and ran manually."

## Wireframes / Mockups
None were made — the interface is just a simple sidebar in Streamlit with six options. No design was planned out beforehand, it was built directly as code.

## Timeline (what actually happened)
Data was collected and cleaned → six models were built one by one → they were wired into a single Streamlit app → some test files and a CI/CD file were drafted, but never actually finished or made to work.

## Open Questions
- Is 47 rows all the team data that's realistically available, or is more out there?
- Where exactly did each dataset come from, and when? This isn't written down anywhere.
- Was the testing/CI/CD setup something in-progress that got abandoned, or something that was never really started properly?

---

# Part 2: Version 2.0 (planned update — May 2026)

## Title
Stratify v2.0 — Fixing the Core Problems and Making It Actually Runnable Anywhere

## Problem Statement
Version 1.0 works, but only on one laptop, with a password sitting in plain text in the code, and with at least one model that doesn't actually do what it claims to do. Before adding anything new, version 2.0 is about fixing what's already broken: the security mistake, the fake test setup, and the circular model logic — then making the whole thing easy to run on any machine using Docker.

## Background
This update exists specifically because of the problems listed in Version 1.0 above. It's not adding new features — it's making the existing six claims actually true, and making the project something that could be shown to someone technical without them immediately spotting a security mistake or a broken test suite.

## Goals
- Remove the hardcoded password and change the actual database password (since it's already been exposed on GitHub, just deleting it from the code isn't enough).
- Fix the Genre Saturation Risk model so the label isn't calculated from the same data used to predict it.
- Actually check what the right number of clusters is for the engagement grouping, instead of just assuming 3.
- Fix the CI/CD file so it points to the real folders, and rewrite the tests so they test the real code, not a placeholder.
- Package the project properly and add Docker, so it can run on any computer with one command instead of needing a specific local setup.
- Clean up the duplicate folders.
- Show, next to each score in the app, how much data it was trained on and some basic validation info — so it's clear which scores are reliable and which (like the 17-row team models) are not.

## Success Metrics
- No password anywhere in the code or in the project's git history (the old one gets changed, not just removed going forward).
- The CI/CD pipeline actually runs successfully on a fresh copy of the project.
- The tests genuinely check the real model code and reach reasonable coverage.
- The whole app can be started with one Docker command on a computer that's never seen this project before.
- Someone reviewing the Genre Saturation Risk code can confirm the label and the input data don't overlap anymore.

## Target Users
Same as v1.0. This update doesn't change who the tool is for — it just makes the tool trustworthy and portable. One more "user" worth naming honestly: anyone (a professor, recruiter, or interviewer) who opens the GitHub repo and checks it in five minutes. Right now, that's arguably the person this project actually needs to satisfy.

## User Personas
Same three personas as before — not changing them, since this update is about the backend, not the users.

## User Stories
- As someone reviewing this project, I want to run it with one command, so I don't need to manually set up a database.
- As a security-conscious reviewer, I want to check there's no password in the code, so I can trust the project was built properly.
- As whoever runs the tests, I want them to actually test the real model files, so a passing result means something.
- As a user of the Genre Saturation Risk score, I want it to be based on something other than the same numbers I can already see, so it's actually telling me something new.

## Scope
- Fixing the password/security issue
- Fixing the Genre Saturation Risk label logic
- Properly checking the number of clusters for engagement grouping
- Fixing and rewriting CI/CD and tests
- Adding Docker so the project runs anywhere
- Cleaning up duplicate folders
- Adding basic data/validation info to the app's display

## Out of Scope
- New models or new data sources
- Real-time data collection (still using static files for now — building a live scraper is a bigger, separate project on its own)
- User accounts or logins
- Actually fixing the 17-row team data problem — this update will just clearly label those two models as unreliable, not solve the underlying lack of data

## Functional Requirements
- Move the database password and any other secret values out of the code and into an environment file that isn't uploaded to GitHub.
- Change the label calculation for Genre Saturation Risk so it doesn't reuse the same input columns.
- Run a proper check (like a silhouette score) to decide the right number of clusters, instead of hardcoding 3.
- Fix the CI/CD file to point to the actual project folders.
- Rewrite the test files to import and test the real model code.
- Add a setup file so the project can be installed properly instead of relying on running it from a specific folder.
- Add Docker files so the whole app (plus database) can start with one command.
- Combine the duplicate folders into one clean version each.
- Add a small info panel in the app showing how much data each model was trained on and a basic validation number, and clearly flag the two models trained on very little data as unreliable.

## Non-Functional Requirements
- No secrets should ever be stored directly in the code going forward.
- The project should be able to run the same way on any computer, not just the one it was built on.
- Anyone cloning the project should be able to get it working without needing to ask the author for help.

## Assumptions
- It's worth fixing and keeping all six models, rather than just dropping the two that are trained on almost no data. This is actually worth questioning rather than assuming — see the open question below.
- One Docker setup with a database container is enough; there's no need for a proper cloud-hosted database at this stage.

## Dependencies
- The label fix and clustering fix need to happen before the tests are rewritten, otherwise the tests will just lock in the same mistakes.
- The CI/CD and testing fixes need to happen before adding Docker — there's no point packaging code that hasn't been checked yet.
- The password fix can happen independently, first, before anything else.

## Constraints
- This is still a one-person project, so everything needs to be done one step at a time, not all at once.

## User Flow
1. Someone downloads the project and runs one Docker command.
2. The app and database start up automatically using settings from an environment file, not hardcoded values.
3. The Streamlit app opens with the six models, each now showing basic info about how much data it's based on.
4. If someone picks the team-based models, a warning shows up saying the data behind it is very limited.
5. When new code is pushed to GitHub, the CI/CD pipeline runs the real tests automatically and fails if something's broken or if a password is accidentally added back in.

## Wireframes / Mockups
Still none — the changes are small additions to the existing app layout (an info panel and a warning message), not a full redesign.

## Acceptance Criteria
- Searching the code and git history for "password" turns up nothing, and the actual database password has been changed.
- The CI/CD pipeline runs successfully from a fresh copy of the project with no manual steps.
- The test coverage report is based on the real model code, not the placeholder files.
- Someone with no prior context can get the app running with Docker in under 10 minutes.
- A code review confirms the Genre Saturation Risk label doesn't share the same data as its inputs anymore.

## Edge Cases
- What happens when a genre has only one game in it? The current genre score just becomes the same as the raw earnings number, so it isn't really saying anything new — this still needs a proper fix, not just relabeling.
- A brand-new creator with almost no data yet — the clustering will still put them somewhere, even though there isn't enough information to place them meaningfully.

## Risks
- Even after changing the password, the old one is still visible in the project's past history on GitHub if the repo is public, so it should be treated as already compromised.
- Fixing the label logic will likely change the output of the Genre Saturation Risk model compared to before — that's expected, but it's worth being upfront about that change if anyone compares old and new results.
- Adding a "limited data" warning to the two weak models doesn't actually fix them — it just tells people they're weak. It shouldn't be mistaken for a real solution.

## Milestones / Timeline
1. Remove and rotate the password
2. Fix the Genre Saturation Risk label and the clustering logic
3. Fix CI/CD and rewrite the tests
4. Add packaging and Docker
5. Clean up duplicate folders
6. Add the data/validation info panel to the app
