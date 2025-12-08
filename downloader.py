import streamlit as st
from yt_dlp import YoutubeDL
import os
import time
from datetime import datetime
import subprocess

st.set_page_config(page_title="VidGrabX - Video Downloader", page_icon="🎯", layout="wide")

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;900&display=swap');
    * { font-family: 'Poppins', sans-serif; }
    .stApp { background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%); color: #ffffff; }
    .block-container { padding-top: 1.5rem !important; padding-bottom: 2rem !important; max-width: 1400px; }
    @media (max-width: 768px) { 
        .logo-text { font-size: 2.2em !important; letter-spacing: 1px !important; } 
        .logo-icon { font-size: 1.8em !important; } 
        .logo-container { padding: 20px 30px !important; }
        .tagline { font-size: 0.85em !important; padding: 0 15px !important; margin-top: 10px !important; } 
        .downloader-card { padding: 20px 12px !important; margin: 15px 5px !important; } 
        .guide-section { padding: 25px 15px !important; margin: 25px 5px !important; } 
        .section-title { font-size: 1.5em !important; margin-bottom: 20px !important; } 
        .platform-tags { margin: 20px 0 !important; }
        .platform-tag { font-size: 0.75em !important; padding: 6px 12px !important; margin: 4px !important; display: inline-block !important; } 
        .stButton>button, .stDownloadButton>button { font-size: 0.95em !important; padding: 12px 16px !important; } 
        .feature-grid { grid-template-columns: 1fr !important; gap: 15px !important; } 
        .feature-card { padding: 25px 20px !important; }
        .stTabs [data-baseweb="tab-list"] { gap: 5px !important; flex-wrap: wrap !important; }
        .stTabs [data-baseweb="tab"] { font-size: 0.8em !important; padding: 10px 12px !important; margin: 3px !important; flex: 1 1 auto !important; min-width: fit-content !important; white-space: nowrap !important; }
        .video-title { font-size: 1em !important; }
        .video-info { font-size: 0.85em !important; }
        .guide-title { font-size: 1.8em !important; }
        .logo-section { padding: 25px 15px 20px !important; }
        .stTextInput input, .stTextArea textarea { font-size: 0.95em !important; padding: 14px !important; }
        .stSelectbox { font-size: 0.9em !important; }
        .feature-icon { font-size: 2.5em !important; }
        .feature-title { font-size: 1.1em !important; }
        .feature-desc { font-size: 0.9em !important; }
    }
    @media (max-width: 480px) {
        .logo-text { font-size: 1.8em !important; }
        .logo-icon { font-size: 1.5em !important; }
        .logo-container { padding: 15px 25px !important; }
        .tagline { font-size: 0.75em !important; line-height: 1.4 !important; }
        .section-title { font-size: 1.3em !important; }
        .platform-tag { font-size: 0.7em !important; padding: 5px 10px !important; margin: 3px !important; }
        .downloader-card { padding: 15px 10px !important; }
        .stTabs [data-baseweb="tab"] { font-size: 0.75em !important; padding: 8px 10px !important; }
        .stButton>button, .stDownloadButton>button { font-size: 0.9em !important; padding: 10px 14px !important; }
        .guide-title { font-size: 1.5em !important; }
        .feature-icon { font-size: 2em !important; }
    }
    @media (min-width: 1400px) {
        .block-container { max-width: 1600px !important; }
    }
    @media (min-width: 1800px) {
        .block-container { max-width: 1800px !important; }
        .feature-grid { grid-template-columns: repeat(3, 1fr) !important; }
    }
    .logo-section { text-align: center; padding: 40px 20px 30px; animation: fadeInDown 0.8s ease-out; }
    @keyframes fadeInDown { from { opacity: 0; transform: translateY(-30px); } to { opacity: 1; transform: translateY(0); } }
    .logo-container { display: inline-block; background: rgba(255,255,255,0.15); padding: 25px 50px; border-radius: 30px; backdrop-filter: blur(20px); box-shadow: 0 20px 60px rgba(0,0,0,0.3); border: 3px solid rgba(255,255,255,0.3); }
    .logo-text { font-size: 4em; font-weight: 900; background: linear-gradient(45deg, #ffffff, #ffd700, #ffffff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 2px 2px 8px rgba(0,0,0,0.3); letter-spacing: 2px; }
    .logo-icon { font-size: 3em; animation: pulse 2s infinite; filter: drop-shadow(0 0 10px rgba(255,255,255,0.5)); }
    @keyframes pulse { 0%, 100% { transform: scale(1); } 50% { transform: scale(1.15); } }
    .tagline { font-size: 1.3em; margin-top: 15px; font-weight: 600; color: #ffffff; text-shadow: 2px 2px 6px rgba(0,0,0,0.3); }
    .downloader-card { background: rgba(255, 255, 255, 0.98); padding: 50px; border-radius: 30px; box-shadow: 0 30px 80px rgba(0,0,0,0.3); margin: 30px auto 50px; border: 2px solid rgba(255,255,255,0.5); animation: fadeInUp 0.8s ease-out; }
    @keyframes fadeInUp { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
    .section-title { text-align: center; background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.3em; font-weight: 900; margin-bottom: 30px; }
    .stTextInput input, .stTextArea textarea { border-radius: 15px !important; border: 3px solid #e0e0e0 !important; padding: 18px !important; background: white !important; color: #2c3e50 !important; font-size: 1.1em !important; font-weight: 500 !important; transition: all 0.3s ease !important; box-shadow: 0 4px 15px rgba(0,0,0,0.08) !important; }
    .stTextInput input:focus, .stTextArea textarea:focus { border-color: #667eea !important; box-shadow: 0 0 0 5px rgba(102, 126, 234, 0.2) !important; transform: translateY(-2px); }
    .stButton>button { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important; color: white !important; border: none !important; border-radius: 15px !important; padding: 18px 36px !important; font-weight: 800 !important; font-size: 1.15em !important; transition: all 0.3s ease !important; box-shadow: 0 10px 30px rgba(102, 126, 234, 0.5) !important; text-transform: uppercase !important; letter-spacing: 1.5px !important; width: 100% !important; }
    .stButton>button:hover { transform: translateY(-4px) !important; box-shadow: 0 15px 45px rgba(102, 126, 234, 0.6) !important; }
    .stDownloadButton>button { background: linear-gradient(135deg, #28a745 0%, #20c997 100%) !important; color: white !important; border: none !important; border-radius: 15px !important; padding: 22px 40px !important; font-weight: 900 !important; font-size: 1.25em !important; box-shadow: 0 12px 35px rgba(40, 167, 69, 0.6) !important; animation: pulse-download 2s infinite !important; text-transform: uppercase !important; letter-spacing: 2px !important; }
    @keyframes pulse-download { 0%, 100% { transform: scale(1); box-shadow: 0 12px 35px rgba(40, 167, 69, 0.6); } 50% { transform: scale(1.05); box-shadow: 0 15px 45px rgba(40, 167, 69, 0.8); } }
    .stDownloadButton>button:hover { background: linear-gradient(135deg, #20c997 0%, #28a745 100%) !important; transform: translateY(-5px) scale(1.05) !important; box-shadow: 0 20px 50px rgba(40, 167, 69, 0.9) !important; }
    .stSelectbox label { color: #2c3e50 !important; font-weight: 700 !important; font-size: 1.05em !important; }
    .stSuccess { background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important; border-left: 6px solid #28a745 !important; border-radius: 12px !important; color: #155724 !important; font-weight: 600 !important; }
    .stError { background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%) !important; border-left: 6px solid #dc3545 !important; border-radius: 12px !important; color: #721c24 !important; font-weight: 600 !important; }
    .stInfo { background: linear-gradient(135deg, #d1ecf1 0%, #bee5eb 100%) !important; border-left: 6px solid #17a2b8 !important; border-radius: 12px !important; color: #0c5460 !important; font-weight: 600 !important; }
    .stWarning { background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%) !important; border-left: 6px solid #ffc107 !important; border-radius: 12px !important; color: #856404 !important; font-weight: 600 !important; }
    .video-title { color: #2c3e50; font-size: 1.2em; font-weight: 700; margin: 10px 0 5px 0; }
    .video-info { color: #6c757d; font-size: 0.95em; font-weight: 500; }
    .loading-container { text-align: center; padding: 30px; background: linear-gradient(135deg, #f8f9fa, #e9ecef); border-radius: 20px; margin: 20px 0; }
    .spinner { border: 5px solid #f3f3f3; border-top: 5px solid #667eea; border-radius: 50%; width: 60px; height: 60px; animation: spin 1s linear infinite; margin: 0 auto 15px auto; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
    .platform-tags { text-align: center; margin: 30px 0; display: flex; flex-wrap: wrap; justify-content: center; align-items: center; padding: 0 10px; }
    .platform-tag { display: inline-block; background: linear-gradient(135deg, #667eea, #764ba2); color: white; padding: 12px 28px; border-radius: 30px; margin: 8px; font-weight: 700; font-size: 1em; box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4); transition: all 0.3s ease; white-space: nowrap; }
    .platform-tag:hover { transform: scale(1.05); box-shadow: 0 8px 30px rgba(102, 126, 234, 0.5); }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; background: transparent; justify-content: center; flex-wrap: wrap; }
    .stTabs [data-baseweb="tab"] { background: rgba(255,255,255,0.8); border-radius: 15px; padding: 15px 30px; font-weight: 700; color: #2c3e50; font-size: 1.05em; transition: all 0.3s ease; border: 2px solid transparent; white-space: nowrap; }
    .stTabs [data-baseweb="tab"]:hover { background: rgba(255,255,255,0.95); transform: translateY(-2px); }
    .stTabs [data-baseweb="tab"][aria-selected="true"] { background: linear-gradient(135deg, #667eea, #764ba2); color: white; border-color: rgba(255,255,255,0.4); box-shadow: 0 6px 25px rgba(102, 126, 234, 0.5); }
    .guide-section { background: rgba(255, 255, 255, 0.97); padding: 50px 40px; border-radius: 30px; margin: 40px auto; box-shadow: 0 25px 70px rgba(0,0,0,0.25); border: 2px solid rgba(255,255,255,0.5); }
    .guide-title { background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2.5em; font-weight: 900; text-align: center; margin-bottom: 40px; }
    .tip-box { background: linear-gradient(135deg, #e7f3ff, #f0e7ff); padding: 25px; border-radius: 15px; margin: 20px 0; border-left: 6px solid #667eea; box-shadow: 0 5px 20px rgba(0,0,0,0.1); color: #2c3e50; font-weight: 500; line-height: 1.8; }
    .tip-box strong { color: #667eea; font-size: 1.15em; }
    .tip-box code { background: rgba(102, 126, 234, 0.1); padding: 4px 8px; border-radius: 5px; color: #764ba2; font-weight: 600; }
    .feature-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 25px; margin: 35px 0; }
    .feature-card { background: linear-gradient(135deg, #ffffff 0%, #f8f9fa 100%); padding: 35px; border-radius: 25px; text-align: center; box-shadow: 0 12px 35px rgba(0,0,0,0.1); transition: all 0.4s ease; border: 3px solid rgba(102, 126, 234, 0.1); }
    .feature-card:hover { transform: translateY(-15px); box-shadow: 0 25px 60px rgba(102, 126, 234, 0.3); border-color: rgba(102, 126, 234, 0.3); }
    .feature-icon { font-size: 3.5em; margin-bottom: 15px; }
    .feature-title { font-weight: 800; color: #2c3e50; margin-bottom: 10px; font-size: 1.3em; }
    .feature-desc { color: #6c757d; font-size: 1em; font-weight: 500; }
    .stProgress > div > div { background: linear-gradient(135deg, #667eea, #764ba2); border-radius: 10px; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

# Initialize session state
if 'video_info' not in st.session_state:
    st.session_state.video_info = None
if 'last_checked_url' not in st.session_state:
    st.session_state.last_checked_url = None
if 'download_history' not in st.session_state:
    st.session_state.download_history = []
if 'batch_videos_info' not in st.session_state:
    st.session_state.batch_videos_info = []

def check_ffmpeg():
    try:
        subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True, timeout=5)
        return True
    except:
        return False

def get_video_info(url):
    ydl_opts = {
        'quiet': True,
        'skip_download': True,
        'no_warnings': True,
        'socket_timeout': 30
    }
    try:
        with YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(url, download=False)
    except:
        return None

def format_duration(seconds):
    if seconds:
        h = seconds // 3600
        m = (seconds % 3600) // 60
        s = seconds % 60
        if h > 0:
            return f"{int(h):02d}:{int(m):02d}:{int(s):02d}"
        else:
            return f"{int(m):02d}:{int(s):02d}"
    return "N/A"

def add_to_history(title, url, format_type):
    title_short = title[:80] + "..." if len(title) > 80 else title
    st.session_state.download_history.insert(0, {
        'title': title_short,
        'url': url,
        'format': format_type,
        'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    })
    if len(st.session_state.download_history) > 15:
        st.session_state.download_history = st.session_state.download_history[:15]

def get_ydl_opts(quality="best", is_audio=False):
    opts = {
        'outtmpl': os.path.join(os.getcwd(), DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'noplaylist': True,
        'socket_timeout': 60,
        'retries': 5
    }
    if is_audio:
        opts['format'] = 'bestaudio'
        if check_ffmpeg():
            opts['postprocessors'] = [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192'
            }]
    else:
        opts['format'] = quality
    return opts

# Header
st.markdown("<div class='logo-section'><div class='logo-container'><span class='logo-icon'>🎯</span><div class='logo-text'>VidGrabX</div></div><div class='tagline'>⚡ Lightning-Fast Downloads • 1000+ Platforms • 100% Free</div></div>", unsafe_allow_html=True)

# FFmpeg check
if check_ffmpeg():
    st.success("✅ **FFmpeg Active** - All features enabled! 🎉")
else:
    st.warning("⚠️ **FFmpeg Missing** - Install for MP3 conversion. Videos still work!")

# Platform tags
st.markdown("<div class='platform-tags'><span class='platform-tag'>📺 YouTube</span><span class='platform-tag'>💥 Facebook</span><span class='platform-tag'>📷 Instagram</span><span class='platform-tag'>🎵 TikTok</span><span class='platform-tag'>🦅 X/Twitter</span><span class='platform-tag'>🎬 Vimeo</span><span class='platform-tag'>🌐 +1000</span></div>", unsafe_allow_html=True)

# Main downloader card
st.markdown("<div class='downloader-card'>", unsafe_allow_html=True)
tab1, tab2, tab3 = st.tabs(["🎥 Single Video", "📋 Batch Download", "🎵 Audio Extractor"])

with tab1:
    st.markdown("<h2 class='section-title'>⚡ Quick Download</h2>", unsafe_allow_html=True)
    video_url = st.text_input("Video URL", placeholder="Paste your video URL here...", key="video_url_single", label_visibility="collapsed")
    
    col_btn1, col_btn2 = st.columns([2, 1])
    with col_btn1:
        if st.button("🔍 ANALYZE VIDEO", key="analyze_single", use_container_width=True):
            if video_url:
                loading = st.empty()
                loading.markdown("<div class='loading-container'><div class='spinner'></div><div style='color: #2c3e50; font-weight: 700; font-size: 1.2em;'>🔍 Analyzing video...</div></div>", unsafe_allow_html=True)
                info = get_video_info(video_url)
                loading.empty()
                
                if info:
                    st.session_state.video_info = info
                    st.session_state.last_checked_url = video_url
                    st.success("✅ Video detected successfully!")
                else:
                    st.error("❌ Failed. Try: pip install --upgrade yt-dlp")
            else:
                st.warning("⚠️ Please paste a URL first!")
    
    if st.session_state.video_info and st.session_state.last_checked_url == video_url:
        info = st.session_state.video_info
        title = info.get('title', 'Unknown')
        thumb = info.get('thumbnail')
        
        st.markdown("<hr style='border: 2px solid #e0e0e0; margin: 30px 0;'>", unsafe_allow_html=True)
        
        if thumb:
            col_img, col_det = st.columns([1, 2])
            with col_img:
                st.image(thumb, use_container_width=True)
            with col_det:
                st.markdown(f"<div class='video-title'>🎬 {title}</div>", unsafe_allow_html=True)
                st.markdown(f"<div class='video-info'>⏱️ {format_duration(info.get('duration', 0))} | 👤 {info.get('uploader', 'Unknown')}</div>", unsafe_allow_html=True)
                if info.get('view_count'):
                    st.markdown(f"<div class='video-info'>👁️ Views: {info.get('view_count'):,}</div>", unsafe_allow_html=True)
        
        st.markdown("<hr style='border: 2px solid #e0e0e0; margin: 30px 0;'>", unsafe_allow_html=True)
        
        col_f, col_q = st.columns(2)
        with col_f:
            dl_type = st.selectbox("📦 Format", ["Video", "Audio (MP3)"], key="single_fmt")
        with col_q:
            if dl_type == "Video":
                quality = st.selectbox("🎯 Quality", ["best", "best[height<=1080]", "best[height<=720]", "best[height<=480]"], key="single_qual")
            else:
                quality = "bestaudio"
        
        st.markdown("<br>", unsafe_allow_html=True)
        col_d1, col_d2, col_d3 = st.columns([1, 2, 1])
        with col_d2:
            if st.button("🚀 DOWNLOAD NOW", key="download_single", use_container_width=True):
                opts = get_ydl_opts(quality, dl_type == "Audio (MP3)")
                with st.status("⬇️ Downloading...", expanded=True) as status:
                    try:
                        status.write("📡 Connecting...")
                        with YoutubeDL(opts) as ydl:
                            status.write("⬇️ Downloading...")
                            result = ydl.extract_info(video_url, download=True)
                            if dl_type == "Audio (MP3)" and check_ffmpeg():
                                filename = ydl.prepare_filename(result).rsplit('.', 1)[0] + '.mp3'
                            else:
                                filename = ydl.prepare_filename(result)
                        
                        status.update(label="✅ Complete!", state="complete")
                        st.success(f"🎉 Downloaded: **{title}**")
                        add_to_history(title, video_url, dl_type)
                        st.markdown("<br>", unsafe_allow_html=True)
                        
                        if os.path.exists(filename):
                            with open(filename, 'rb') as f:
                                file_data = f.read()
                            st.download_button(
                                label="💾 CLICK HERE TO DOWNLOAD FILE",
                                data=file_data,
                                file_name=os.path.basename(filename),
                                mime="application/octet-stream",
                                use_container_width=True,
                                key="dl_btn_" + str(time.time())
                            )
                            st.success("👆 **Click the green button to save!**")
                            st.info(f"📂 File: **{os.path.basename(filename)}**")
                    except Exception as e:
                        status.update(label="❌ Failed", state="error")
                        st.error(f"**Error:** {str(e)[:150]}")

with tab2:
    st.markdown("<h2 class='section-title'>📋 Batch Download</h2>", unsafe_allow_html=True)
    st.info("💡 Paste multiple URLs (one per line)")
    batch_urls = st.text_area("Video URLs", placeholder="https://youtube.com/...\nhttps://tiktok.com/...", height=150, key="batch_urls", label_visibility="collapsed")
    
    col_b1, col_b2 = st.columns(2)
    with col_b1:
        batch_fmt = st.selectbox("Format", ["Video", "Audio (MP3)"], key="batch_fmt")
    with col_b2:
        skip_err = st.checkbox("⭐ Skip Failed", value=True, key="skip_err")
    
    if st.button("🔍 ANALYZE ALL", key="analyze_batch", use_container_width=True):
        if batch_urls:
            urls = [u.strip() for u in batch_urls.split('\n') if u.strip()]
            if urls:
                st.info(f"📊 Analyzing {len(urls)} videos...")
                st.session_state.batch_videos_info = []
                prog = st.progress(0)
                cont = st.container()
                
                for idx, url in enumerate(urls):
                    prog.progress(idx / len(urls), text=f"Analyzing {idx+1}/{len(urls)}")
                    with cont:
                        load = st.empty()
                        load.markdown(f"<div style='background: #f8f9fa; padding: 15px; border-radius: 10px; margin: 10px 0;'><strong style='color: #2c3e50;'>🔍 {idx+1}/{len(urls)}...</strong><br><small style='color: #6c757d;'>{url[:70]}...</small></div>", unsafe_allow_html=True)
                        info = get_video_info(url)
                        load.empty()
                    
                    if info:
                        st.session_state.batch_videos_info.append({
                            'url': url,
                            'title': info.get('title', 'Unknown'),
                            'thumbnail': info.get('thumbnail'),
                            'duration': info.get('duration', 0),
                            'uploader': info.get('uploader', 'Unknown')
                        })
                        c1, c2 = st.columns([1, 3])
                        if info.get('thumbnail'):
                            c1.image(info.get('thumbnail'), use_container_width=True)
                        c2.markdown(f"<div class='video-title'>✅ {info.get('title', 'Unknown')[:60]}</div>", unsafe_allow_html=True)
                        c2.markdown(f"<div class='video-info'>⏱️ {format_duration(info.get('duration', 0))} | 👤 {info.get('uploader', 'Unknown')}</div>", unsafe_allow_html=True)
                    else:
                        st.warning(f"⚠️ Failed: {url[:60]}...")
                    
                    prog.progress((idx + 1) / len(urls))
                
                st.success(f"✅ Analyzed {len(st.session_state.batch_videos_info)} videos!")
    
    if st.session_state.batch_videos_info:
        st.markdown("<hr style='border: 2px solid #e0e0e0; margin: 30px 0;'>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='color: #2c3e50; text-align: center;'>📊 Ready: {len(st.session_state.batch_videos_info)} videos</h3>", unsafe_allow_html=True)
        
        if st.button("🚀 DOWNLOAD ALL", key="download_batch", use_container_width=True):
            opts = get_ydl_opts("best", batch_fmt == "Audio (MP3)")
            prog = st.progress(0)
            cont = st.container()
            success = 0
            failed = 0
            
            for idx, vid in enumerate(st.session_state.batch_videos_info):
                prog.progress(idx / len(st.session_state.batch_videos_info), text=f"Downloading {idx+1}/{len(st.session_state.batch_videos_info)}")
                with cont:
                    st.write(f"**[{idx+1}/{len(st.session_state.batch_videos_info)}]** {vid['title'][:50]}...")
                try:
                    with YoutubeDL(opts) as ydl:
                        ydl.download([vid['url']])
                    success += 1
                    st.success(f"✅ {vid['title'][:50]}")
                    add_to_history(vid['title'], vid['url'], batch_fmt)
                except Exception as e:
                    failed += 1
                    st.warning("⚠️ Failed")
                    if not skip_err:
                        break
                
                prog.progress((idx + 1) / len(st.session_state.batch_videos_info))
            
            st.markdown("<hr>", unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            c1.metric("✅ Success", success)
            c2.metric("❌ Failed", failed)
            c3.metric("📊 Total", len(st.session_state.batch_videos_info))
            st.success(f"🎉 Saved to: {DOWNLOAD_DIR}/")
            st.info("💡 Files are on server. Use Single Video tab for direct downloads.")
            st.session_state.batch_videos_info = []

with tab3:
    st.markdown("<h2 class='section-title'>🎵 Audio Extractor</h2>", unsafe_allow_html=True)
    st.info("💡 Extract audio from videos!")
    src = st.radio("Source", ["🌐 From URL", "📁 Upload File"], key="audio_src", horizontal=True)
    audio_url = None
    uploaded = None
    
    if src == "🌐 From URL":
        audio_url = st.text_input("Video URL", placeholder="Paste URL...", key="audio_url", label_visibility="collapsed")
    else:
        uploaded = st.file_uploader("Upload Video", type=['mp4', 'avi', 'mov', 'mkv', 'flv', 'wmv', 'webm'], key="audio_upload")
        if uploaded:
            st.success(f"✅ **{uploaded.name}** ({uploaded.size / 1024 / 1024:.2f} MB)")
    
    c1, c2 = st.columns(2)
    with c1:
        fmt = st.selectbox("Format", ["MP3", "M4A", "WAV"], key="audio_format")
    with c2:
        qual = st.selectbox("Quality", ["Best (320kbps)", "High (256kbps)", "Medium (192kbps)"], key="audio_quality")
    
    st.markdown("<br>", unsafe_allow_html=True)
    disabled = (src == "🌐 From URL" and not audio_url) or (src == "📁 Upload File" and not uploaded)
    
    if st.button("🎵 EXTRACT AUDIO", key="extract_audio", use_container_width=True, disabled=disabled):
        if src == "🌐 From URL" and audio_url:
            with st.status("🎵 Extracting...", expanded=True) as status:
                try:
                    quality = '320' if 'Best' in qual else ('256' if 'High' in qual else '192')
                    opts = {
                        'format': 'bestaudio',
                        'outtmpl': os.path.join(os.getcwd(), DOWNLOAD_DIR, f'%(title)s.{fmt.lower()}')
                    }
                    if check_ffmpeg():
                        opts['postprocessors'] = [{
                            'key': 'FFmpegExtractAudio',
                            'preferredcodec': fmt.lower(),
                            'preferredquality': quality
                        }]
                    
                    status.write("📡 Connecting...")
                    with YoutubeDL(opts) as ydl:
                        status.write("⬇️ Downloading...")
                        result = ydl.extract_info(audio_url, download=True)
                        filename = ydl.prepare_filename(result).rsplit('.', 1)[0] + f'.{fmt.lower()}'
                    
                    status.update(label="✅ Complete!", state="complete")
                    st.success(f"🎉 Extracted: **{result.get('title', 'Unknown')}**")
                    add_to_history(f"[AUDIO] {result.get('title', 'Unknown')}", audio_url, f"Audio - {fmt}")
                    
                    if os.path.exists(filename):
                        with open(filename, 'rb') as f:
                            file_data = f.read()
                        st.download_button(
                            label="💾 DOWNLOAD AUDIO FILE",
                            data=file_data,
                            file_name=os.path.basename(filename),
                            mime="audio/mpeg",
                            use_container_width=True,
                            key="dl_audio_" + str(time.time())
                        )
                        st.info(f"📂 File: {os.path.basename(filename)}")
                except Exception as e:
                    status.update(label="❌ Failed", state="error")
                    st.error(f"Error: {str(e)[:150]}")
        
        elif src == "📁 Upload File" and uploaded:
            if not check_ffmpeg():
                st.error("❌ FFmpeg Required for local extraction!")
            else:
                with st.status("🎵 Extracting...", expanded=True) as status:
                    try:
                        temp = os.path.join(DOWNLOAD_DIR, f"temp_{uploaded.name}")
                        status.write("💾 Saving...")
                        with open(temp, "wb") as f:
                            f.write(uploaded.getbuffer())
                        
                        base = os.path.splitext(uploaded.name)[0]
                        output = f"{base}_audio.{fmt.lower()}"
                        out_path = os.path.join(DOWNLOAD_DIR, output)
                        quality = '320' if 'Best' in qual else ('256' if 'High' in qual else '192')
                        
                        status.write("🎵 Extracting...")
                        codec = {'MP3': 'libmp3lame', 'M4A': 'aac', 'WAV': 'pcm_s16le'}
                        cmd = ['ffmpeg', '-i', temp, '-vn', '-acodec', codec[fmt]]
                        if fmt != 'WAV':
                            cmd.extend(['-b:a', f'{quality}k'])
                        cmd.extend(['-y', out_path])
                        
                        result = subprocess.run(cmd, capture_output=True, text=True)
                        
                        if result.returncode == 0:
                            os.remove(temp)
                            status.update(label="✅ Complete!", state="complete")
                            st.success(f"🎉 Extracted from: {uploaded.name}")
                            add_to_history(f"[LOCAL] {uploaded.name}", "Local File", f"Audio - {fmt}")
                            
                            if os.path.exists(out_path):
                                with open(out_path, 'rb') as f:
                                    file_data = f.read()
                                st.download_button(
                                    label="💾 DOWNLOAD AUDIO",
                                    data=file_data,
                                    file_name=output,
                                    mime="audio/mpeg",
                                    use_container_width=True,
                                    key="dl_local_" + str(time.time())
                                )
                                st.info(f"📂 File: {output}")
                        else:
                            raise Exception("FFmpeg error")
                    except Exception as e:
                        status.update(label="❌ Failed", state="error")
                        st.error(f"Error: {str(e)[:150]}")
                        if os.path.exists(temp):
                            os.remove(temp)

st.markdown("</div>", unsafe_allow_html=True)

# Download History
if st.session_state.download_history:
    st.markdown("<div class='guide-section'>", unsafe_allow_html=True)
    st.markdown("<h2 class='guide-title'>📜 Download History</h2>", unsafe_allow_html=True)
    for idx, item in enumerate(st.session_state.download_history[:10], 1):
        st.markdown(f"<div style='background: linear-gradient(135deg, #fff, #f8f9fa); padding: 25px; border-radius: 15px; margin-bottom: 15px; border-left: 5px solid #667eea; box-shadow: 0 5px 20px rgba(0,0,0,0.1);'><strong style='color: #2c3e50; font-size: 1.1em;'>#{idx} 🎬 {item['title']}</strong><br><small style='color: #6c757d; font-weight: 500;'>📦 {item['format']} | ⏰ {item['time']} | 🔗 {item['url'][:50]}...</small></div>", unsafe_allow_html=True)
    if st.button("🗑️ Clear History", key="clear_hist"):
        st.session_state.download_history = []
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# Features Section
st.markdown("<div class='guide-section'><h2 class='guide-title'>✨ Why Choose VidGrabX?</h2><div class='feature-grid'><div class='feature-card'><div class='feature-icon'>⚡</div><div class='feature-title'>Lightning Fast</div><div class='feature-desc'>Optimized for speed</div></div><div class='feature-card'><div class='feature-icon'>📋</div><div class='feature-title'>Batch Downloads</div><div class='feature-desc'>Multiple videos</div></div><div class='feature-card'><div class='feature-icon'>🎵</div><div class='feature-title'>Audio Extraction</div><div class='feature-desc'>MP3, M4A, WAV</div></div><div class='feature-card'><div class='feature-icon'>🌐</div><div class='feature-title'>1000+ Sites</div><div class='feature-desc'>All platforms</div></div><div class='feature-card'><div class='feature-icon'>🔒</div><div class='feature-title'>100% Secure</div><div class='feature-desc'>No registration</div></div><div class='feature-card'><div class='feature-icon'>📱</div><div class='feature-title'>Responsive</div><div class='feature-desc'>All devices</div></div></div></div>", unsafe_allow_html=True)

# Footer
st.markdown("<div style='text-align:center; color:#fff; padding: 50px; background: rgba(0,0,0,0.3); border-radius: 25px; margin-top: 50px; backdrop-filter: blur(15px);'><div style='font-size:3.5em; margin-bottom: 20px; filter: drop-shadow(0 0 15px rgba(255,255,255,0.4));'>🎯 <strong>VidGrabX</strong></div><div style='font-size:1.3em; opacity:0.95; margin-bottom: 20px; font-weight: 600; line-height: 1.6;'>The Ultimate Free Video Downloader<br>Powered by yt-dlp • Streamlit • Python • FFmpeg</div><div style='font-size:1.1em; opacity:0.9; margin: 20px 0;'>🌐 YouTube • TikTok • Facebook • Instagram • Twitter • Vimeo • 1000+ More</div><div style='font-size:1em; opacity:0.8; margin-top: 25px; padding-top: 25px; border-top: 2px solid rgba(255,255,255,0.2);'>© 2025 VidGrabX • Free & Open Source Forever 🚀<br><small style='opacity: 0.7;'>Made with ❤️ for video enthusiasts worldwide</small></div></div>", unsafe_allow_html=True)
