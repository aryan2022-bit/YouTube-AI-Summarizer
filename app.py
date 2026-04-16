import os
import langcodes
import google.generativeai as genai
import streamlit as st
from dotenv import load_dotenv
from youtube_transcript_api import YouTubeTranscriptApi
from warnings import filterwarnings



def streamlit_config():

    # page configuration
    st.set_page_config(page_title='YouTube')

    # page header transparent color and Removes top padding 
    page_background_color = """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@600;700;800&family=DM+Sans:wght@400;500;600&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    [data-testid="stHeader"] {
        background: rgba(0,0,0,0);
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 950px;
    }

    /* ── Sidebar ── */
    [data-testid="stSidebar"] {
        background: #181820;
        border-right: 1px solid #262635;
    }

    [data-testid="stSidebar"] * {
        color: #e0e0ec !important;
    }

    /* Sidebar section label */
    .sidebar-section-label {
        font-size: 13px;
        font-weight: 700;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        color: #808098 !important;
        margin-bottom: 10px;
        margin-top: 12px;
        padding-left: 2px;
    }

    /* Sidebar inputs & selectboxes */
    [data-testid="stSidebar"] input {
        background-color: #232330 !important;
        border: 1px solid #36364a !important;
        border-radius: 12px !important;
        color: #ffffff !important;
        padding: 5px !important; 
        transition: border 0.3s ease, box-shadow 0.3s ease;
        font-size: 14.5px !important; 
    }

    [data-testid="stSidebar"] input:focus {
        border-color: #ff5555 !important;
        box-shadow: 0 0 0 3px rgba(255, 85, 85, 0.15) !important;
        background-color: #282836 !important;
    }

    /* Fix the SelectBox inside Sidebar */
    [data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #232330 !important;
        border: 1px solid #36364a !important;
        border-radius: 12px !important;
        color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] div[data-baseweb="select"]:hover > div {
        border-color: #ff5555 !important;
    }

    /* Summarize button */
    [data-testid="stSidebar"] .stButton > button {
        background: linear-gradient(135deg, #ff4040 0%, #e01818 100%) !important;
        color: #ffffff !important;
        font-family: 'DM Sans', sans-serif !important;
        font-weight: 700 !important;
        font-size: 15px !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 18px 0 !important;
        letter-spacing: 0.3px !important;
        box-shadow: 0 6px 20px rgba(220, 30, 30, 0.3) !important;
        transition: transform 0.15s ease, box-shadow 0.15s ease !important;
        margin-top: 5px;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 25px rgba(220, 30, 30, 0.4) !important;
    }

    [data-testid="stSidebar"] .stButton > button:active {
        transform: translateY(0) !important;
        box-shadow: 0 2px 10px rgba(220, 30, 30, 0.25) !important;
    }

    /* Sidebar tip box */
    .sidebar-tip {
        background: linear-gradient(135deg, #1e1e28, #1c1c24);
        border: 1px solid #2c2c3e;
        border-radius: 12px;
        padding: 18px 20px;
        margin-top: 24px;
        font-size: 13.5px;
        color: #9595a8 !important;
        line-height: 1.6;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }

    .sidebar-tip strong {
        color: #ff5555 !important;
        font-weight: 700;
        display: block;
        margin-bottom: 6px;
        font-size: 14.5px;
    }

    /* ── Main area ── */
    .stApp {
        background: #0f0f14;
    }

    /* ── Hero title area ── */
    .hero-wrap {
        text-align: center;
        padding: 10px 0 24px 0;
    }

    .hero-title {
        font-family: 'Syne', sans-serif;
        font-size: 3rem;
        font-weight: 800;
        color: #f0f0fa;
        margin-bottom: 12px;
        letter-spacing: -1px;
        line-height: 1.15;
    }

    .hero-title span { color: #ff4444; }

    .hero-sub {
        color: #8c8c9e;
        font-size: 16px;
        margin-top: 0;
        margin-bottom: 22px;
    }

    /* Feature badges */
    .badge-row {
        display: flex;
        justify-content: center;
        gap: 12px;
        flex-wrap: wrap;
        margin-top: 16px;
    }

    .badge {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 100px;
        padding: 6px 16px;
        font-size: 13px;
        font-weight: 600;
        color: #a0a0b2;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    /* Thin divider */
    .section-divider {
        border: none;
        border-top: 1px solid #20202b;
        margin: 32px 0;
    }

    /* ── How it Works ── */
    .hiw-label {
        text-align: center;
        margin-bottom: 24px;
    }

    .hiw-label-top {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        color: #ff5555;
        margin-bottom: 8px;
    }

    .hiw-label-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.6rem;
        font-weight: 700;
        color: #e4e4f0;
    }

    .hiw-grid {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 18px;
        margin-bottom: 10px;
    }

    .hiw-card {
        background: #16161d;
        border: 1px solid #242432;
        border-radius: 16px;
        padding: 26px 20px;
        text-align: center;
        transition: border-color 0.25s, transform 0.2s, box-shadow 0.25s;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
    }

    .hiw-card:hover {
        border-color: rgba(255,68,68,0.4);
        transform: translateY(-4px);
        box-shadow: 0 12px 25px rgba(0,0,0,0.3);
    }

    .hiw-icon { font-size: 32px; margin-bottom: 12px; display: block; }

    .hiw-step {
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        color: #ff5555;
        margin-bottom: 6px;
    }

    .hiw-title {
        font-family: 'Syne', sans-serif;
        font-size: 16px;
        font-weight: 700;
        color: #e4e4f0;
        margin-bottom: 6px;
    }

    .hiw-desc {
        font-size: 13px;
        color: #8c8c9e;
        line-height: 1.6;
    }

    /* ── Thumbnail ── */
    [data-testid="stImage"] img {
        border-radius: 18px !important;
        box-shadow: 0 15px 35px rgba(0,0,0,0.5), 0 0 0 1px rgba(255,255,255,0.03) !important;
    }

    /* ── Summary ── */
    .summary-header {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 6px;
    }

    .summary-title {
        font-family: 'Syne', sans-serif;
        font-size: 1.4rem;
        font-weight: 700;
        color: #f0f0fa;
    }

    .summary-badge {
        background: rgba(255,68,68,0.15);
        border: 1px solid rgba(255,68,68,0.3);
        border-radius: 100px;
        padding: 4px 14px;
        font-size: 12px;
        font-weight: 600;
        color: #ff6666;
        letter-spacing: 0.2px;
    }

    .summary-divider {
        border: none;
        border-top: 1px solid #242432;
        margin: 14px 0 20px 0;
    }

    .summary-card {
        background: #16161d;
        border: 1px solid #242432;
        border-radius: 20px;
        padding: 35px 40px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.2);
        color: #c4c4d4;
        line-height: 1.9;
        font-size: 16px;
    }

    .summary-card h1, .summary-card h2, .summary-card h3 {
        font-family: 'Syne', sans-serif !important;
        color: #ff5555 !important;
        margin-top: 22px;
        margin-bottom: 12px;
    }

    .summary-card strong { color: #f0f0fa; }
    .summary-card ul, .summary-card ol { padding-left: 24px; margin-bottom: 16px;}
    .summary-card li { margin-bottom: 6px; }

    /* Spinner */
    [data-testid="stSpinner"] p {
        color: #a0a0b2 !important;
        font-size: 15px !important;
        font-weight: 500;
    }

    /* Toast */
    [data-testid="stToast"] {
        background: #1e1e28 !important;
        border-left: 4px solid #ff5555 !important;
        border-radius: 10px !important;
        font-size: 14px !important;
        box-shadow: 0 4px 15px rgba(0,0,0,0.3) !important;
        color: #f0f0fa !important;
    }

    /* Scrollbar */
    ::-webkit-scrollbar { width: 6px; }
    ::-webkit-scrollbar-track { background: #0f0f14; }
    ::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 10px; }
    ::-webkit-scrollbar-thumb:hover { background: rgba(255,255,255,0.25); }

    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)

    # Hero: title + subtitle + feature badges
    st.markdown("""
        <div class='hero-wrap'>
            <h1 class='hero-title'>📺 YouTube <span>AI</span> Summarizer</h1>
            <p class='hero-sub'>Transform any YouTube video into a clean, concise summary in seconds</p>
            <div class='badge-row'>
                <span class='badge'>⚡ Gemini AI</span>
                <span class='badge'>📋 Detailed summaries</span>
                <span class='badge'>🎯 Key point extraction</span>
            </div>
        </div>
    """, unsafe_allow_html=True)



def extract_languages(video_id):
    try:
        # Fetch the List of Available Transcripts for Given Video
        ytt_api = YouTubeTranscriptApi()
        transcript_list = ytt_api.list(video_id)

        # Extract the Language Codes from List ---> ['en','ta']
        available_transcripts = [i.language_code for i in transcript_list]

        # Convert Language_codes to Human-Readable Language_names ---> 'en' into 'English'
        language_list = list({langcodes.Language.get(i).display_name() for i in available_transcripts})

        # Create a Dictionary Mapping Language_names to Language_codes
        language_dict = {langcodes.Language.get(i).display_name():i for i in available_transcripts}

        return language_list, language_dict
    except Exception as e:
        return None, str(e)



def extract_transcript(video_id, language):
    
    try:
        # Request Transcript for YouTube Video using API
        ytt_api = YouTubeTranscriptApi()
        transcript_content = ytt_api.fetch(video_id=video_id, languages=[language])
    
        # Extract Transcript Content from JSON Response and Join to Single Response
        transcript = ' '.join([i.text for i in transcript_content.snippets])

        return transcript
    
    
    except Exception as e:
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.write("")
        st.markdown(f'<h5 style="text-position:center;color:orange;">{e}</h5>', unsafe_allow_html=True)



def generate_summary(transcript_text):

    try:
        # Configures the genai Library
        genai.configure(api_key=os.environ['GOOGLE_API_KEY'])

        # Initializes a Gemini Generative Model
        model = genai.GenerativeModel(model_name = 'gemini-2.5-flash-lite')  

        # Define a Prompt for AI Model
        prompt = """You are a YouTube video summarizer. You will be taking the transcript text and summarizing the entire video, 
                    providing the important points as proper sub-headings in a concise manner (detailed summary). 
                    Please provide the summary of the text given here: """
        
        response = model.generate_content(prompt + transcript_text)

        return response.text

    except Exception as e:
        error_message = str(e)
        if "429" in error_message or "Quota exceeded" in error_message:
            st.toast("⚠️ API Rate Limit Exceeded", icon="🔴")
            return "### 🔴 Whoops! Rate Limit Hit\nYou have exceeded the free tier quota for the Google Gemini API (Too many requests in a short time). \n\n**Please wait about 1 minute and try again!**"
        
        # Fallback for other errors
        for _ in range(3):
            st.write("")
        st.markdown(f'<h5 style="text-align:center; color:orange;">{error_message}</h5>', unsafe_allow_html=True)
        return None


 
def main():

    # Filter the Warnings
    filterwarnings(action='ignore')

    # Load the Environment Variables
    load_dotenv()

    # Streamlit Configuration Setup
    streamlit_config()

    # Initialize the Button Variable
    button = False

    with st.sidebar:

        image_url = 'https://raw.githubusercontent.com/aryan2022-bit/YouTube-AI-Summarizer/main/image/youtube_banner.JPG'
        st.image(image_url, width='stretch')
        st.write("")

        # Sidebar section label
        st.markdown("<div class='sidebar-section-label'>🔗 Video Input</div>", unsafe_allow_html=True)

        # Get YouTube Video Link From User 
        video_link = st.text_input(label='Enter YouTube Video Link')

        if video_link:
            # Extract the Video ID From URL
            if 'v=' in video_link:
                video_id = video_link.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in video_link:
                video_id = video_link.split('youtu.be/')[1].split('?')[0]
            else:
                video_id = video_link

            # Extract Language from Video_ID
            languages_info = extract_languages(video_id)
            
            if languages_info[0] is None:
                st.error("Failed to retrieve transcripts. This video might be age-restricted, disabled, or YouTube is blocking requests. Please try a different video link.")
                st.stop()
            else:
                language_list, language_dict = languages_info

                # Sidebar section label
                st.markdown("<div class='sidebar-section-label'>🌐 Language</div>", unsafe_allow_html=True)
            
                # User Select the Transcript Language
                language_input = st.selectbox(label='Select Transcript Language', 
                                            options=language_list)
                
                # Get Language_code from Dict
                language = language_dict[language_input]

                # Click Submit Button
                st.write("")
                button = st.button(label='✨ Summarize Video', type='primary', use_container_width=True)

        # Tip box — always visible in sidebar
        st.markdown("""
            <div class='sidebar-tip'>
                <strong>💡 Tips for best results</strong>
                Works great with lectures, podcasts, news & tutorials. Videos with auto-generated captions are also supported.
            </div>
        """, unsafe_allow_html=True)
        

    # User Enter the Video Link and Click Submit Button
    if button and video_link:
        
        # Clean center layout for thumbnail
        st.write("")
        col1, col2, col3 = st.columns([0.5, 4, 0.5])

        # Display the Video Thumbnail nicely framed
        with col2:
            st.image(image=f'http://img.youtube.com/vi/{video_id}/0.jpg', 
                     use_container_width=True)
        
        st.write("")
        st.write("")

        # Extract Transcript from YouTube Video
        with st.spinner(text='⏳ Extracting Transcript from YouTube...'):
            transcript_text = extract_transcript(video_id, language)

        if transcript_text:
            # Generating Summary using Gemini AI
            with st.spinner(text='🧠 Generating AI Summary...'):
                summary = generate_summary(transcript_text)

            # Display the Summary beautifully
            if summary:
                st.write("")
                st.toast("Summary generation complete!", icon="✅")

                # Summary header with badge
                st.markdown("""
                    <div class='summary-header'>
                        <span class='summary-title'>📝 Video Summary</span>
                        <span class='summary-badge'>AI Generated</span>
                    </div>
                    <hr class='summary-divider'>
                """, unsafe_allow_html=True)

                # Summary card
                st.markdown(f"<div class='summary-card'>{summary}</div>", unsafe_allow_html=True)

    else:
        # ── Empty state: How it works + stats ──
        st.markdown("<hr class='section-divider'>", unsafe_allow_html=True)

        st.markdown("""
            <div class='hiw-label'>
                <div class='hiw-label-top'>Get Started</div>
                <div class='hiw-label-title'>How it works</div>
            </div>

            <div class='hiw-grid'>
                <div class='hiw-card'>
                    <span class='hiw-icon'>🔗</span>
                    <div class='hiw-step'>Step 01</div>
                    <div class='hiw-title'>Paste a Link</div>
                    <div class='hiw-desc'>Copy any YouTube URL and paste it into the sidebar input field</div>
                </div>
                <div class='hiw-card'>
                    <span class='hiw-icon'>🌐</span>
                    <div class='hiw-step'>Step 02</div>
                    <div class='hiw-title'>Pick a Language</div>
                    <div class='hiw-desc'>Choose your preferred transcript language from available options</div>
                </div>
                <div class='hiw-card'>
                    <span class='hiw-icon'>✨</span>
                    <div class='hiw-step'>Step 03</div>
                    <div class='hiw-title'>Get the Summary</div>
                    <div class='hiw-desc'>Gemini AI reads the transcript and delivers a structured summary</div>
                </div>
            </div>

            <hr class='section-divider'>
        """, unsafe_allow_html=True)
        


if __name__ == '__main__':
    
    try:
        main()

    except Exception as e:
        for _ in range(5):
            st.write("")
        st.markdown(f'<h5 style="text-position:center;color:orange;">{e}</h5>', unsafe_allow_html=True)