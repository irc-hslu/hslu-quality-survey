import streamlit as st
import pandas as pd
import os
from datetime import datetime
import random
import streamlit.components.v1 as components
# Page configuration
st.set_page_config(
    page_title="Subjective quality assessment of Gaussian Splats vs Point Clouds ",
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
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WeAreGoingOnBullrun.mp4",
    "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/WhatCarCanYouGetForAGrand.mp4",
    "https://raw.githubusercontent.com/kitylam9/surveyvideo/main/gsvspcd.mp4"
]
def balancedLatinSquareWithBlocks6(participantId):
	random.seed(datetime.now().timestamp())

	AB_BA_Stimuli = [[r"0AB", r"0BA"],
					 [r"1AB", r"1BA"],
					 [r"2AB", r"2BA"],
					 [r"3AB", r"3BA"],
					 [r"4AB", r"4BA"],
					 [r"5AB", r"5BA"]]

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

def get_video_url(question_num):
    """Get video URL for a specific question (1-indexed)"""
    if 1 <= question_num <= len(videoUrls):
        return videoUrls[question_num - 1]
    return None

def get_video_index_for_question(question_num):
    """Get the video index for a specific question based on the balanced Latin square sequence"""
    if 'video_sequence' not in st.session_state:
        return None
    if 1 <= question_num <= len(st.session_state.video_sequence):
        return st.session_state.video_sequence[question_num - 1]
    return None

def generate_participant_id():
    """Generate a participant ID based on the number of existing survey responses"""
    csv_file = 'survey_responses.csv'
    
    if not os.path.exists(csv_file): 
        return 1
    
    try:
        # Read existing CSV to count unique participants
        existing_df = pd.read_csv(csv_file)
        
        if existing_df.empty or 'Participant_ID' not in existing_df.columns: 
            return 1
        
        # Get unique participant IDs
        next_num = existing_df['Participant_ID'].max() 
        next_num += 1
        return next_num
    except Exception:
        # If there's any error reading the file, start with P001
        return 1

def save_to_csv():
    """Save all answers to CSV file"""
    if not st.session_state.answers:
        return
    
    # Prepare data for CSV
    data = []
    for question_num in range(1, NUM_QUESTIONS + 1):
        answer = st.session_state.answers.get(question_num, "No answer")
        video_index = get_video_index_for_question(question_num)
        data.append({
            'Participant_ID': st.session_state.participant_id or 'Unknown',
            'Question': question_num,
            'Video_Index': video_index if video_index is not None else 'Unknown',
            'Choice': answer,
            'TimeUsed': st.session_state.time_used[question_num]
        })
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Save to CSV (append mode to preserve previous responses)
    csv_file = f'survey_responses_{st.session_state.start_time.strftime("%Y-%m-%d_%H-%M-%S")}.csv'
    df.to_csv(csv_file, index=False)
    concat_csv='survey_responses.csv'
    if os.path.exists(concat_csv):
        existing_df = pd.read_csv(concat_csv)
        df = pd.concat([existing_df, df], ignore_index=True)
    df.to_csv(concat_csv, index=False)
    return csv_file
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
    if os.path.exists(css_file):
        with open(css_file, 'r') as f:
            css = f.read()
            st.markdown(f'<style>{css}</style>', unsafe_allow_html=True)
    else:
        # Fallback inline CSS if file doesn't exist
        st.markdown("""
        <style>
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
        }
        h1 {
            color: #1f77b4;
            text-align: center;
            margin-bottom: 1.5rem;
        }
        </style>
        """, unsafe_allow_html=True)
def setLogoImage():
    st.space("medium")
    col1, col2, col3, col4 = st.columns([1, 1, 1, 1]) 
    with col2:
        st.image("img\\hslulogo.svg", width=300)         
    with col3:
        st.image("img\\Logo_Heat_512x142.jpg", width=250)
def main():
    # Load CSS styles
    load_css()
    
    # Auto-generate participant ID if not set
    st.session_state.participant_id = generate_participant_id()
     
    # Show introduction screen if not started yet
    if st.session_state.current_question == -3: 
        setLogoImage()
        st.title("Subjective quality assessment of Gaussian Splats vs Point Clouds")
        st.markdown("""  
 <div style="margin: 4em; text-align: justify; font-size: 1.2rem;"> 
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
            if st.button("Start Survey", type="primary", use_container_width=True):
                # Generate video sequence using balanced Latin square
                participant_id_num = int(st.session_state.participant_id) 
                array_indices = list(range(len(videoUrls)))
                st.session_state.video_sequence = balanced_latin_square(array_indices, participant_id_num)
                st.session_state.current_question = -2 
                st.rerun()
        return
    if st.session_state.current_question == -2:
        setLogoImage()
        st.title("Start of training")
        st.markdown("""  <div style="margin: 4em; text-align: center; font-size: 1.2rem;"> 
                   Now the training starts. You will see a video showing two side-by-side 3D reconstructions, click on the best reconstruction video. 
                   <br> When you click on the video, the next stimulus is shown. <br>
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
        surveyVideo(videoUrls[11]) 
        return
    if st.session_state.current_question == -4:
        setLogoImage()
        st.title("Training completed")
        st.markdown(""" 
                   <div style="margin: 4em; text-align: center; font-size: 1.2rem;"> The training is finished. Now, the experiment starts.
                   </div></br>""", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            if st.button("Next", type="primary", use_container_width=True):
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
        csv_file = save_to_csv()
        st.success(f"Survey completed! Thank you for contributing this research project.")
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
