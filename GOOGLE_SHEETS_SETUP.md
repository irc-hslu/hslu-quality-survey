# Streamlit Secrets Configuration for Google Sheets Integration

This file documents the secrets you need to configure in Streamlit Cloud for Google Sheets integration.

## Setup Steps

### 1. Create a Google Cloud Project and Service Account

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the **Google Sheets API** and **Google Drive API**
4. Go to **IAM & Admin** > **Service Accounts**
5. Click **Create Service Account**
6. Give it a name (e.g., "streamlit-sheets-writer")
7. Click **Create and Continue**
8. Skip the optional steps and click **Done**
9. Click on the service account you just created
10. Go to the **Keys** tab
11. Click **Add Key** > **Create new key**
12. Choose **JSON** and click **Create**
13. Save the downloaded JSON file securely

### 2. Create a Google Sheet

1. Go to [Google Sheets](https://sheets.google.com/)
2. Create a new spreadsheet
3. Give it a name (e.g., "HSLU Quality Survey Responses")
4. **Important:** Share the spreadsheet with the service account email (found in the JSON file as `client_email`), giving it **Editor** access

### 3. Configure Streamlit Cloud Secrets

In your Streamlit Cloud app settings, go to **Secrets** and add the following TOML configuration:

```toml
spreadsheet_name = "HSLU Quality Survey Responses"

[gcp_service_account]
type = "service_account"
project_id = "your-project-id"
private_key_id = "your-private-key-id"
private_key = "-----BEGIN PRIVATE KEY-----\nYOUR_PRIVATE_KEY_HERE\n-----END PRIVATE KEY-----\n"
client_email = "your-service-account@your-project.iam.gserviceaccount.com"
client_id = "your-client-id"
auth_uri = "https://accounts.google.com/o/oauth2/auth"
token_uri = "https://oauth2.googleapis.com/token"
auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
client_x509_cert_url = "https://www.googleapis.com/robot/v1/metadata/x509/your-service-account%40your-project.iam.gserviceaccount.com"
```

**Note:** Copy the values from the JSON file you downloaded in step 1.

### 4. Local Development (Optional)

For local testing, create a `.streamlit/secrets.toml` file in your project root with the same content as above.

**Important:** Add `.streamlit/secrets.toml` to your `.gitignore` to avoid committing sensitive credentials!

## Data Structure

The app will create two worksheets in your Google Sheet:

1. **ParticipantID**: Stores the current participant ID counter
2. **Responses**: Stores all survey responses with columns:
   - Timestamp
   - Participant_ID
   - Question
   - Video_Index
   - Choice
   - TimeUsed
   - Session_Start
