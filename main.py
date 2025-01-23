import streamlit as st
import os
import base64

def get_base64_video(video_path):
    """Get base64 encoded video"""
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode()

def get_app_link(app_name):
    """
    Dynamically generate links based on deployment environment
    """
    deployment_links = {
        "IF": {
            "local": "http://localhost:8501",
            "production": "https://bioinformatics-if-prediction.streamlit.app/"
        },
        "Args": {
            "local": "http://localhost:8502",
            "production": "https://bioinformatics-args-prediction.streamlit.app/"
        },
        "PPIN": {
            "local": "http://localhost:8503",
            "production": "https://bioinformatics-ppin-prediction.streamlit.app/"
        },
        "Similarity": {
            "local": "http://localhost:8504",
            "production": "https://bioinformatics-similarity-prediction.streamlit.app/"
        }
    }
    
    # Determine environment with explicit fallback
    env = os.environ.get('STREAMLIT_ENV', 'local')
    
    # Add explicit error handling
    try:
        link = deployment_links.get(app_name, {}).get(env, None)
        if not link:
            st.error(f"No link found for {app_name} in {env} environment")
            return "#"
        return link
    except Exception as e:
        st.error(f"Error getting link for {app_name}: {str(e)}")
        return "#"

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
    
    .main .block-container {
        padding-top: 0rem;
        padding-bottom: 0rem;
    }
    
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
            body {{
                margin: 0;
                overflow-x: hidden;
            }}
            
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
                transform: translate(-50%, -50%) scale(1.00);
                min-width: 100%;
                min-height: 100%;
                width: auto;
                height: auto;
                object-fit: cover;
            }}
            
            .stApp {{
                background: none;
            }}
            
            .card {{
                background-color: rgba(226, 247, 250, 0.9);
                border-radius: 20px;
                padding: 1.5rem;
                margin: 3rem;
                text-align: center;
                box-shadow: 0 4px 6px rgba(0, 0, 2, 0.1);
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
            
            .main-title {{
                color: white;
                text-align: center;
                padding: 2rem;
                text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.5);
                margin-top: 0;
            }}
            
            .card h3 {{
                margin-bottom: 1rem;
                color: #1f1f1f;
            }}
            
            .card p {{
                color: #666;
                font-size: 0.9rem;
            }}
            
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
            <a href="{link}" style="text-decoration: none; color: inherit;">
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
        
        # Define cards with dynamically generated links
        cards = [
            {
                "title": "(IF)",
                "description": "🧬 Imprinting Factor (IF) Prediction",
                "link": get_app_link("IF"),
                "icon": "🔬"
            },
            {
                "title": "Args",
                "description": "ARG Classifier & Mobility Analyzer",
                "link": get_app_link("Args"),
                "icon": "🧪"
            },
            {
                "title": "PPIN",
                "description": "Configure your preferences",
                "link": get_app_link("PPIN"),
                "icon": "🌐"
            },
            {
                "title": "Similarity",
                "description": "Explore Similarity Metrics",
                "link": get_app_link("Similarity"),
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