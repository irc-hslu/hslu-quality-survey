import streamlit as st
import pandas as pd
from datetime import datetime
import random
import streamlit.components.v1 as components
import gspread
from google.oauth2.service_account import Credentials

# Google Sheets configuration
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_google_sheet():
    """Connect to Google Sheets using service account credentials from Streamlit secrets"""
    try:
        # Get credentials from Streamlit secrets
        credentials = Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
        client = gspread.authorize(credentials)
        
        # Open the spreadsheet by name or URL
        # You can change this to your spreadsheet name
        spreadsheet = client.open(st.secrets["spreadsheet_name"])
        return spreadsheet
    except Exception as e:
        st.error(f"Failed to connect to Google Sheets: {e}")
        return None

# NOTE: To bypass ngrok's browser warning, users need to:
# 1. Use a browser extension to add "ngrok-skip-browser-warning: true" header
# 2. Or use ngrok's paid plan with custom domain
# 3. Or instruct users to click through the warning page once
# Page configuration
st.set_page_config(
    page_title="Subjective Quality Assessment of Gaussian Splats vs Point Clouds ",
    page_icon="🎬",
    layout="wide"
)

# Initialize session state
if 'current_question' not in st.session_state:
    st.session_state.current_question = -3  # -1 means intro screen
if 'answers' not in st.session_state:
    st.session_state.answers = {} 
if 'participant_id' not in st.session_state:
    st.session_state.participant_id = None
if 'survey_completed' not in st.session_state:
    st.session_state.survey_completed = False 
if 'video_sequence' not in st.session_state:
    st.session_state.video_sequence = []
if 'time_used' not in st.session_state:
    st.session_state.time_used = {}
if 'start_time' not in st.session_state:
    st.session_state.start_time = datetime.now()
# Number of questions
NUM_QUESTIONS = 12

# Video URLs for each question
videoUrls = [
#    "videos/den_1_perf_2_GS_PCD.mp4",
#    "videos/den_1_perf_2_PCD_GS.mp4",
#    "videos/nathalie_1_perf_3_GS_PCD.mp4",
#    "videos/nathalie_1_perf_3_PCD_GS.mp4",
#    "videos/philipp_1_perf_5_GS_PCD.mp4",
#    "videos/philipp_1_perf_5_PCD_GS.mp4",
#    "videos/philipp_1_perf_6_GS_PCD.mp4",
#    "videos/philipp_1_perf_6_PCD_GS.mp4",
#    "videos/simone_2_perf_3_GS_PCD.mp4",
#    "videos/simone_2_perf_3_PCD_GS.mp4",
#    "videos/thanos_2_perf_2_GS_PCD.mp4",
#    "videos/thanos_2_perf_2_PCD_GS.mp4",
#    "videos/training.mp4"
    "https://drive.switch.ch/index.php/s/BK5i2WWlAyqgN6e/download",
    "https://drive.switch.ch/index.php/s/Em5LKTNyd1Q7Noh/download",
    "https://drive.switch.ch/index.php/s/2aLNTwCSA7hxJoF/download",
    "https://drive.switch.ch/index.php/s/8fKxU3YXct9eTbk/download",
    "https://drive.switch.ch/index.php/s/mo1sZyDaZX5Oc5m/download",
    "https://drive.switch.ch/index.php/s/Kahcf6TMK12q10q/download",
    "https://drive.switch.ch/index.php/s/3Eep8QOUbxoCb9Y/download",
    "https://drive.switch.ch/index.php/s/GeiuNSQpKv7rGkP/download",
    "https://drive.switch.ch/index.php/s/H6ERCoS2hRrUCNp/download",
    "https://drive.switch.ch/index.php/s/LLusIqa1DCeDwYb/download",
    "https://drive.switch.ch/index.php/s/Iay1Wi9JfEEJkhy/download",
    "https://drive.switch.ch/index.php/s/5ucLQ9NtwLJAQMX/download",
    "https://drive.switch.ch/index.php/s/2Y52cs2O057wkVu/download"
]
def balancedLatinSquareWithBlocks6(participantId):
	random.seed(datetime.now().timestamp())

	#AB_BA_Stimuli = [[r"0AB", r"0BA"],
	#				 [r"1AB", r"1BA"],
	#				 [r"2AB", r"2BA"],
	#				 [r"3AB", r"3BA"],
	#				 [r"4AB", r"4BA"],
	#				 [r"5AB", r"5BA"]]
	AB_BA_Stimuli = [[0, 1],
					 [2, 3],
					 [4, 5],
					 [6, 7],
					 [8, 9],
					 [10, 11]]

	Random_AB_BA_Stimuli = [random.sample(row, k=len(row)) for row in AB_BA_Stimuli]

	# debug
	# print("Random_AB_BA_Stimuli")
	# print(Random_AB_BA_Stimuli)

	# Balanced Latin Square from https://hci-studies.org/balanced-latin-square/
	BLS_6 = [	[0,	1,	2,	3,	4,	5],
				[1,	3,	0,	5,	2,	4],
				[3,	5,	1,	4,	0,	2],
				[5,	4,	3,	2,	1,	0],
				[4,	2,	5,	0,	3,	1],
				[2,	0,	4,	1,	5,	3]]

	first_row = participantId % 6
	second_row = (participantId+1) % 6

	stimuli = []

	for i in range(6):
		stimulus_i = BLS_6[first_row][i]
		stimulus = Random_AB_BA_Stimuli[stimulus_i][0]
		stimuli.append(stimulus)

	for i in range(6):
		stimulus_i = BLS_6[second_row][i]
		stimulus = Random_AB_BA_Stimuli[stimulus_i][1]
		stimuli.append(stimulus)

	return stimuli

def balanced_latin_square(array, participant_id):
    """
    Generate a balanced Latin square sequence for video randomization.
    Args:
        array: List of indices (0 to n-1)
        participant_id: Participant ID as integer
    
    Returns:
        List of indices in balanced Latin square order
    """
    result = []
    j = 0
    h = 0 
    for i in range(len(array)):
        val = 0
        if i < 2 or i % 2 != 0:
            val = j
            j += 1
        else:
            val = len(array) - h - 1
            h += 1
        
        idx = (val + participant_id) % len(array)
        result.append(array[idx])
    
    if len(array) % 2 != 0 and participant_id % 2 != 0:
        result = result[::-1]  # Reverse the list 
    return result

#def get_video_url(question_num):
#    """Get video URL for a specific question (1-indexed)"""
#    if 1 <= question_num <= len(videoUrls):
#        return videoUrls[question_num - 1]
#    return None

def get_video_index_for_question(question_num):
    """Get the video index for a specific question based on the balanced Latin square sequence"""
    if 'video_sequence' not in st.session_state:
        return None
    if 1 <= question_num <= len(st.session_state.video_sequence):
        return st.session_state.video_sequence[question_num - 1]
    return None

def generate_participant_id():
    """Generate a participant ID based on the number stored in Google Sheets"""
    try:
        spreadsheet = get_google_sheet()
        if spreadsheet is None:
            # Fallback to random ID if Google Sheets connection fails
            return random.randint(1, 1000000)
        
        # Try to get or create 'ParticipantID' worksheet
        try:
            worksheet = spreadsheet.worksheet('ParticipantID')
        except gspread.WorksheetNotFound:
            # Create the worksheet if it doesn't exist
            worksheet = spreadsheet.add_worksheet(title='ParticipantID', rows=10, cols=1)
            worksheet.update_cell(1, 1, '0')
        
        # Get current ID and increment
        current_value = worksheet.cell(1, 1).value
        if current_value is None or current_value == '':
            last_num = 0
        else:
            try:
                last_num = int(current_value)
            except ValueError:
                last_num = 0
        
        new_id = last_num + 1
        worksheet.update_cell(1, 1, str(new_id))
        return new_id
        
    except Exception as e:
        st.warning(f"Could not generate participant ID from Google Sheets: {e}")
        # Fallback to random ID
        return random.randint(1, 1000000)

def save_to_google_sheets():
    """Save all answers to Google Sheets"""
    if not st.session_state.answers:
        return False
    
    try:
        spreadsheet = get_google_sheet()
        if spreadsheet is None:
            return False
        
        # Try to get or create 'Responses' worksheet
        try:
            worksheet = spreadsheet.worksheet('Responses')
        except gspread.WorksheetNotFound:
            # Create the worksheet with headers
            worksheet = spreadsheet.add_worksheet(title='Responses', rows=1000, cols=7)
            worksheet.update('A1:G1', [['Timestamp', 'Participant_ID', 'Question', 'Video_Index', 'Choice', 'TimeUsed', 'Session_Start']])
        
        # Prepare data for Google Sheets
        rows_to_add = []
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        session_start = st.session_state.start_time.strftime("%Y-%m-%d %H:%M:%S")
        
        for question_num in range(1, NUM_QUESTIONS + 1):
            answer = st.session_state.answers.get(question_num, "No answer")
            video_index = get_video_index_for_question(question_num)
            rows_to_add.append([
                timestamp,
                st.session_state.participant_id or 'Unknown',
                question_num,
                video_index if video_index is not None else 'Unknown',
                answer,
                st.session_state.time_used.get(question_num, 0),
                session_start
            ])
        
        # Append all rows at once
        worksheet.append_rows(rows_to_add, value_input_option='USER_ENTERED')
        return True
        
    except Exception as e:
        st.error(f"Failed to save to Google Sheets: {e}")
        return False
def surveyVideo(video_url):
    video_html = f"""
    <video autoplay loop muted playsinline src="{video_url}" > 
    </video>
    """
    st.markdown(  video_html , unsafe_allow_html=True)
    return 
def load_css():
    """Load and inject CSS styles"""
    css_file = 'style.css'
    try:
        with open(css_file, 'r') as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        # Fallback inline CSS if file doesn't exist
        st.warning("Fallback inline CSS if file doesn't exist")
def setLogoImage():
    st.space("medium")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1]) 
    with col2:
        st.image("img/hslulogo.svg", width=300)         
    with col3:
        st.image("img/Logo_Heat_512x142.jpg", width=250)
def main():
    # Load CSS styles
    load_css()
    # Show introduction screen if not started yet
    if st.session_state.current_question == -3:  
        setLogoImage()
        st.title("Subjective Quality Assessment of Gaussian Splats vs Point Clouds")
        st.markdown("""  
 <div style="margin: 4em; text-align: center; font-size: 1.2rem;"> 
Thank you for participating in this study. The goal is to evaluate and compare the visual quality of two different 3D representations: Gaussian splats and point clouds.
<br>
In this study, you will watch videos showing two 3D reconstructions of people, each created using one of the two representations. After viewing each pair, please choose the reconstruction with the better visual quality.
<br>
Before starting the actual experiment, you will complete a short training phase to become familiar with the task.
<br>
Your feedback is valuable and will help us better understand how these 3D representations perform from a human visual perception perspective. All responses will be treated confidentially and used solely for research purposes.
<br> 
Thank you for your time and contribution. </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next", type="primary", use_container_width=True):
                #st.session_state.participant_id = generate_participant_id()
                # Generate video sequence using balanced Latin square 
                #array_indices = list(range(len(videoUrls)))
                #st.session_state.video_sequence = balanced_latin_square(array_indices, participant_id_num)
                #st.session_state.video_sequence = balancedLatinSquareWithBlocks6(st.session_state.participant_id)
                st.session_state.current_question = -2 
                st.rerun()
        return
    if st.session_state.current_question == -2:
        setLogoImage()
        st.title("Start of Training")
        st.markdown("""  <div style="margin: 4em; text-align: center; font-size: 1.2rem;"> 
                   Now the training begins. You will see a video with two side-by-side 3D reconstructions. Your task is to click on the reconstruction with best visual quality. Each video is 10 seconds long and will loop continuously. Please maximize the window to better inspect the videos. 
                   <br> When you click on the reconstruction,the training finishes. In the actual experiment, a click submits your choice and advances to the next video. <br>
                   </div>""", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next", type="primary", use_container_width=True):
                st.session_state.current_question = -1
                st.rerun()
        return
    if st.session_state.current_question == -1:  
        #right_choice = st.radio("Training - Video with best quality:", ["Left", "Right"],key=f"qTRAINING_right", horizontal=True,index=None)
        #if right_choice == "Left" or right_choice == "Right": 
        col1, col2= st.columns([1, 1], gap=None)
        with col1:
            if st.button(" ", key="trainLeft", type="secondary",use_container_width = True ):   
                st.session_state.current_question = -4
                st.rerun()
        with col2:
            if st.button(" ", key="trainRight", type="secondary", use_container_width = True ):
                st.session_state.current_question = -4
                st.rerun()
        surveyVideo(videoUrls[12]) 
        return
    if st.session_state.current_question == -4:
        setLogoImage()
        st.title("Training Completed")
        st.markdown(""" 
                   <div style="margin: 4em; text-align: center; font-size: 1.2rem;"> The training is complete. You can now begin the experiment.
                   </div></br>""", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next", type="primary", use_container_width=True):
                st.session_state.participant_id = generate_participant_id() 
                st.session_state.video_sequence = balancedLatinSquareWithBlocks6(st.session_state.participant_id)
                st.session_state.start_time = datetime.now()
                st.session_state.current_question = 0
                st.rerun()
        return
    # Current question number (1-indexed)
    question_num = st.session_state.current_question + 1 
      
    current_answer = st.session_state.answers.get(question_num)
    choice_index = 0 if current_answer == "Left" else (1 if current_answer == "Right" else None)
        # Check if survey is completed
    if st.session_state.get('survey_completed', False):
        setLogoImage()
        if save_to_google_sheets():
            st.success("Survey completed! Thank you for taking part and contributing to this research study.")
        else:
            st.warning("Survey completed! However, there was an issue saving responses. Please contact the administrator.")
        st.balloons()
        return
    else:
        right_choice=None
        col1, col2= st.columns([1, 1], gap=None)
        with col1:
            if st.button(" ", key="trainLeft", type="secondary",use_container_width = True ):   
                right_choice="Left"
        with col2:
            if st.button(" ", key="trainRight", type="secondary", use_container_width = True ):
                right_choice="Right"
        # Radio button for right (centered, horizontal inline)
        #right_choice = st.radio(  f"Question {question_num} - Video with best quality:", ["Left", "Right"], key=f"q{question_num}_right", horizontal=True, index=choice_index)
        # Get video index from balanced Latin square sequence
        video_index = get_video_index_for_question(question_num)
        
        # Display single video for the question
        if video_index is not None and 0 <= video_index < len(videoUrls):
            video_url = videoUrls[video_index]
            surveyVideo(video_url)
        else:
            st.warning(f"No video URL found for question {question_num}")
        # Update answer if right radio changed and auto-advance
        if right_choice != current_answer:
            st.session_state.answers[question_num] = right_choice
            elapsed = datetime.now() - st.session_state.start_time
            # Store time used as seconds (float) instead of full timedelta (e.g. "0 days 00:00:05")
            st.session_state.time_used[question_num] = elapsed.total_seconds()
            # Auto-advance to next question or submit if last question
            if question_num < NUM_QUESTIONS:
                st.session_state.current_question += 1
                st.session_state.start_time = datetime.now()
                st.rerun()
            else:
                # Last question - auto-submit
                if len(st.session_state.answers) == NUM_QUESTIONS:
                    st.session_state.survey_completed = True
                    st.rerun() 
    
if __name__ == "__main__":
    main()
