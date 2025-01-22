import streamlit as st
import os
import base64

def get_base64_video(video_path):
    """Get base64 encoded video"""
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode()

# Set the page configuration
st.set_page_config(
    layout="wide",
    page_title="Interactive Dashboard",
    page_icon="🎥",
    initial_sidebar_state="collapsed"
)

# Hide Streamlit's default menu and footer
hide_streamlit_style = """
<style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display: none;}
    [data-testid="stToolbar"] {visibility: hidden !important;}
    [data-testid="stDecoration"] {visibility: hidden !important;}
    [data-testid="stStatusWidget"] {visibility: hidden !important;}
    
    /* Remove padding and gap at the top */
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    
    /* Remove padding from container */
    .stApp > header + div > div {
        padding-top: 0rem;
    }
</style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

def load_css(video_base64):
    """Generate CSS for styling the application."""
    return f"""
        <style>
            /* Reset default margins and handle overflow */
            body {{
                margin: 0;
                overflow-x: hidden;
            }}
            
            /* Video background styling */
            .video-container {{
                position: fixed;
                right: 0;
                bottom: 0;
                min-width: 100%;
                min-height: 100%;
                width: 100%;
                height: 100%;
                z-index: -1;
                overflow: hidden;
                background: rgba(0, 0, 0, 0.3);
            }}

            #background-video {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) scale(1.00);  /* Reduced zoom scale */
                min-width: 100%;
                min-height: 100%;
                width: auto;
                height: auto;
                object-fit: cover;  /* Ensures video covers container without stretching */
            }}
            
            /* Main content container */
            .stApp {{
                background: none;
            }}
            
            /* Card styling */
            .card {{
                background-color: rgba(226, 247, 250, 0.9);
                border-radius: 20px;
                padding: 1.5rem;
                margin: 3rem;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 1, 2, 0.1);
                width: 500px;
                height: 200px;
                transition: transform 0.3s ease, box-shadow 0.3s ease;
                cursor: pointer;
                display: flex;
                flex-direction: column;
                justify-content: center;
            }}
            
            .card:hover {{
                transform: translateY(-5px);
                box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
            }}
            
            /* Title styling */
            .main-title {{
                color: white;
                text-align: center;
                padding: 2rem;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
                margin-top: 0;
            }}
            
            /* Card title styling */
            .card h3 {{
                margin-bottom: 1rem;
                color: #1f1f1f;
            }}
            
            /* Card description styling */
            .card p {{
                color: #666;
                font-size: 0.9rem;
            }}
            
            /* Add responsive design */
            @media (max-width: 768px) {{
                .card {{
                    width: 100%;
                    margin: 1rem 0;
                }}
            }}
        </style>
        <div class="video-container">
            <video id="background-video" autoplay loop muted playsinline>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
            </video>
        </div>
    """


def create_card(title: str, description: str, link: str, icon: str = None) -> str:
    icon_html = f"<div style='font-size: 2rem; margin-bottom: 1rem;'>{icon}</div>" if icon else ""
    return f"""
        <div class="card">
            <a href="{link}" target="_self" style="text-decoration: none; color: inherit;">
                {icon_html}
                <h3>{title}</h3>
                <p>{description}</p>
            </a>
        </div>
    """




def main():
    # Get the video path
    video_path = "static/background.mp4"
    
    try:
        # Convert video to base64
        video_base64 = get_base64_video(video_path)
        
        # Inject CSS and video background
        st.markdown(load_css(video_base64), unsafe_allow_html=True)
        
        # Create columns for cards
        col1, col2 = st.columns(2)
        
        # Define cards with icons and descriptions
        cards = [
            {
                "title": "(IF)",
                "description": " 🧬Imprinting Factor (IF) Prediction",
                "link": "https://bioinformatics-if-prediction.streamlit.app/",
                "icon": "🔬"
            },
            {
                "title": "Args",
                "description": "ARG Classifier & Mobility Analyzer",
                "link": "https://example.com/reports",
                "icon": "🧪"
            },
            {
                "title": "PPIN",
                "description": "Configure your preferences",
                "link": "https://example.com/settings",
                "icon": "🌐"
            },
            {
                "title": "similarity",
                "description": "Get support and documentation",
                "link": "https://example.com/help",
                "icon": "🔗"
            }
        ]
        
        # Add cards to columns
        with col1:
            st.markdown(create_card(**cards[0]), unsafe_allow_html=True)
            st.markdown(create_card(**cards[1]), unsafe_allow_html=True)
        
        with col2:
            st.markdown(create_card(**cards[2]), unsafe_allow_html=True)
            st.markdown(create_card(**cards[3]), unsafe_allow_html=True)
            
    except FileNotFoundError:
        st.error("Video file not found. Please ensure the video file exists in the static folder.")
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()
