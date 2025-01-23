import streamlit as st
import base64

def get_base64_video(video_path):
    """Get base64 encoded video."""
    try:
        with open(video_path, "rb") as video_file:
            return base64.b64encode(video_file.read()).decode()
    except FileNotFoundError:
        st.error(f"Video file {video_path} not found")
        return ""

def get_app_link(app_name):
    """Dynamically generate links for different apps."""
    deployment_links = {
        "IF": "https://bioinformatics-if-prediction.streamlit.app",
        "Args": "https://bioinformatics-arg.streamlit.app", 
        "PPIN": "https://bioinformatics-ppin.streamlit.app",
        "Similarity": "https://bioinformatics-similarity.streamlit.app"
    }
    return deployment_links.get(app_name, "#")

st.set_page_config(
    layout="wide",
    page_title="Interactive Dashboard",
    page_icon="🎥",
    initial_sidebar_state="collapsed"
)

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
        </style>
    """

def main():
    # Hide default Streamlit elements
    st.markdown("""
        <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
        </style>
    """, unsafe_allow_html=True)

    # Video background
    video_path = "background.mp4"
    try:
        video_base64 = get_base64_video(video_path)
        st.markdown(load_css(video_base64), unsafe_allow_html=True)
    except Exception as e:
        st.warning(f"Background video loading error: {e}")

    # Define apps with details
    apps = [
        {
            "name": "(IF)",
            "description": "🧬 Imprinting Factor (IF) Prediction",
            "link": get_app_link("IF"),
            "icon": "🔬"
        },
        {
            "name": "Args",
            "description": "ARG Classifier & Mobility Analyzer", 
            "link": get_app_link("Args"),
            "icon": "🧪"
        },
        {
            "name": "PPIN",
            "description": "Protein-Protein Interaction Network Analysis",
            "link": get_app_link("PPIN"),
            "icon": "🌐"
        },
        {
            "name": "Similarity",
            "description": "Explore Similarity Metrics",
            "link": get_app_link("Similarity"),
            "icon": "🔗"
        }
    ]

    # Create columns
    col1, col2 = st.columns(2)

    # Render apps in columns
    with col1:
        for app in apps[:2]:
            if st.button(f"{app['icon']} {app['name']}", key=app['name'], use_container_width=True):
                st.markdown(f'<meta http-equiv="refresh" content="0;url={app["link"]}">', unsafe_allow_html=True)

    with col2:
        for app in apps[2:]:
            if st.button(f"{app['icon']} {app['name']}", key=app['name'], use_container_width=True):
                st.markdown(f'<meta http-equiv="refresh" content="0;url={app["link"]}">', unsafe_allow_html=True)

    # Add custom JavaScript for additional link handling
    st.components.v1.html("""
        <script>
        document.addEventListener('DOMContentLoaded', (event) => {
            var buttons = document.querySelectorAll('button');
            buttons.forEach(function(button) {
                button.addEventListener('click', function() {
                    var link = this.getAttribute('data-link');
                    if (link) {
                        window.location.href = link;
                    }
                });
            });
        });
        </script>
    """, height=0)

if __name__ == "__main__":
    main()
