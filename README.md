# Quality Experiment Survey

A Streamlit-based survey application for quality comparison experiments with video content.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```
 

## Running the Application

```bash
streamlit run quality-experiment.py
```

## Features

- 12 questions with video comparisons
- Left/Right radio button selection for each question
- Progress tracking
- Answer summary sidebar
- Automatic CSV export of responses
- Participant ID tracking

## Output

Survey responses are saved to `survey_responses.csv` with the following columns:
- Participant_ID
- Question
- Choice (Left/Right)
- Timestamp
