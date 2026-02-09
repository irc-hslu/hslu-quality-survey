# Quality Experiment Survey

A Streamlit-based survey application for quality comparison experiments with video content.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure Google Sheets (for Streamlit Cloud deployment):
   - See [GOOGLE_SHEETS_SETUP.md](GOOGLE_SHEETS_SETUP.md) for detailed instructions

## Running the Application

### Local Development
```bash
streamlit run quality-experiment.py
```

### Streamlit Cloud
Deploy via GitHub and configure secrets in the Streamlit Cloud dashboard.

## Features

- 12 questions with video comparisons
- Left/Right button selection for each question
- Balanced Latin square design for counterbalanced video presentation
- Progress tracking
- **Google Sheets integration** for cloud-based response storage
- Participant ID tracking

## Output

Survey responses are saved to Google Sheets with the following columns:
- Timestamp
- Participant_ID
- Question
- Video_Index
- Choice (Left/Right)
- TimeUsed
- Session_Start
