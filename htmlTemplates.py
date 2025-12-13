# htmlTemplates.py

css = """
<style>
/* Import Google Fonts */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Poppins:wght@400;500;600;700&display=swap');

/* Global Styles */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

/* Force Streamlit sidebar to show properly */
[data-testid="stSidebar"] {
    visibility: visible !important;
    display: block !important;
    transform: translateX(0) !important;
}

/* Full screen black gradient sidebar - FIXED LEFT POSITION */
[data-testid="stSidebar"] {
    background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%) !important;
    min-width: 320px !important;
    width: 320px !important;
}

/* Hide Streamlit Elements */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Main container adjustments - content goes beside sidebar */
.main .block-container {
    padding-left: 340px !important;
    padding-right: 2rem !important;
    padding-top: 0 !important;
    padding-bottom: 100px !important; /* SPACE FOR FIXED INPUT */
    max-width: 100% !important;
    margin-left: 0 !important;
}

@media (max-width: 768px) {
    .main .block-container {
        padding-left: 2rem !important;
    }
}

/* FIXED INPUT CONTAINER - STAYS AT BOTTOM */
.fixed-input-wrapper {
    position: fixed !important;
    bottom: 0 !important;
    left: 340px !important;
    right: 0 !important;
    background: white !important;
    z-index: 9999 !important;
    padding: 15px 30px !important;
    border-top: 1px solid #e5e7eb !important;
    box-shadow: 0 -4px 20px rgba(0, 0, 0, 0.1) !important;
    width: calc(100% - 340px) !important;
}

/* Ensure Streamlit doesn't interfere */
[data-testid="stAppViewContainer"] {
    overflow: visible !important;
}

/* Sidebar custom styling */
.sidebar-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 30px;
    # padding: 20px 0;
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-logo {
    width: 50px;
    height: 50px;
    filter: brightness(0) invert(1);
}

.sidebar-title {
    font-family: 'Poppins', sans-serif;
    font-size: 28px;
    font-weight: 700;
    color: white;
    margin: 0;
    letter-spacing: 0.5px;
}

/* Tips Container in sidebar */
.tips-container {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    padding: 25px;
    border-radius: 16px;
    color: white;
    margin: 20px 0;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.tips-container h3 {
    font-family: 'Poppins', sans-serif;
    font-size: 20px;
    font-weight: 600;
    margin-top: 0;
    margin-bottom: 15px;
    color: white;
}

.tips-container ul {
    margin: 10px 0;
    padding-left: 20px;
}

.tips-container li {
    margin: 10px 0;
    font-size: 14px;
    line-height: 1.6;
    opacity: 0.9;
}

/* Sidebar text color */
[data-testid="stSidebar"] p, 
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h4, 
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stMarkdown {
    color: white !important;
}

/* Sidebar uploader */
[data-testid="stSidebar"] .uploadedFile {
    border: 2px dashed rgba(255, 255, 255, 0.3) !important;
    background: rgba(255, 255, 255, 0.05) !important;
    color: white !important;
}

[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stTextInput textarea {
    background: rgba(255, 255, 255, 0.1) !important;
    border: 1px solid rgba(255, 255, 255, 0.2) !important;
    color: white !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    height: 48px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    transition: all 0.3s ease !important;
    margin: 5px 0 !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
}

/* Chat container */
.chat-container {
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
}

/* Messages container - SCROLLABLE */
.messages-container {
    max-height: calc(100vh - 250px) !important; /* Reduced for fixed input */
    overflow-y: auto !important;
    overflow-x: hidden !important;
    padding: 20px;
    scroll-behavior: smooth;
}

/* Scroll wrapper for messages */
.messages-scroll-wrapper {
    height: calc(100vh - 250px);
    overflow-y: auto;
    padding: 20px;
}

/* Message styling */
.message-wrapper {
    margin-bottom: 25px;
    animation: fadeInUp 0.4s ease-out;
}

@keyframes fadeInUp {
    from {
        opacity: 0;
        transform: translateY(20px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* User message on LEFT */
.user-message {
    display: flex;
    justify-content: flex-start;
}

.user-message .message-bubble {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border-radius: 20px 20px 20px 5px;
    padding: 16px 22px;
    max-width: 75%;
    margin-left: 15px;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.2);
    font-size: 15px;
    line-height: 1.6;
}

.user-message .avatar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
    box-shadow: 0 4px 10px rgba(102, 126, 234, 0.3);
}

/* AI message on RIGHT */
.ai-message {
    display: flex;
    justify-content: flex-end;
}

.ai-message .message-bubble {
    background: white;
    color: #1f2937;
    border-radius: 20px 20px 5px 20px;
    padding: 16px 22px;
    max-width: 75%;
    margin-right: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
    border: 1px solid #f0f0f0;
    font-size: 15px;
    line-height: 1.6;
}

.ai-message .avatar {
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    color: white;
    width: 45px;
    height: 45px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    flex-shrink: 0;
    box-shadow: 0 4px 10px rgba(16, 185, 129, 0.3);
}

/* Message content layout */
.message-content {
    display: flex;
    align-items: flex-start;
    gap: 30px;
}

.ai-message .message-content {
    flex-direction: row-reverse;
}

/* Welcome message */
.welcome-container {
    text-align: center;
    padding: 20px 20px;
    color: #4b5563;
}

.welcome-title {
    font-family: 'Poppins', sans-serif;
    font-size: 42px;
    font-weight: 700;
    margin-bottom: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* Input styling */
.stTextInput>div>div>input {
    border-radius: 12px;
    border: 2px solid #e5e7eb;
    padding: 14px 20px;
    font-size: 16px;
    transition: all 0.3s ease;
    font-family: 'Inter', sans-serif;
}

.stTextInput>div>div>input:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.15);
    outline: none;
}

/* Send button in fixed container */
.fixed-input-wrapper .stButton>button {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    height: 52px !important;
    width: 52px !important;
    font-size: 20px !important;
    transition: all 0.3s ease !important;
    margin: 0 !important;
}

.fixed-input-wrapper .stButton>button:hover {
    transform: scale(1.05) !important;
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4) !important;
}

/* File processed list */
.file-list {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 15px;
    margin-top: 15px;
}

.file-item {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 8px 12px;
    margin: 5px 0;
    background: rgba(255, 255, 255, 0.08);
    border-radius: 8px;
    color: white;
    font-size: 14px;
}

/* Scrollbar styling */
::-webkit-scrollbar {
    width: 8px;
}

::-webkit-scrollbar-track {
    background: #f1f1f1;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: linear-gradient(135deg, #5a6fd8 0%, #693d9e 100%);
}

/* Metrics styling */
.metric-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 15px;
    margin: 10px 0;
    text-align: center;
    border: 1px solid rgba(255, 255, 255, 0.1);
}

.metric-value {
    font-size: 24px;
    font-weight: 700;
    color: white;
    margin: 5px 0;
}

.metric-label {
    font-size: 12px;
    color: rgba(255, 255, 255, 0.7);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}


</style>
"""