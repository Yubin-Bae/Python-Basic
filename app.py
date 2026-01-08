
import streamlit as st
import pandas as pd
from datetime import datetime

# ---------------- CSS 디자인 시작 ----------------
css_code = '''
<style>
    /* [요청사항 1] 전체 핑크색 배경 */
    .stApp {
        background-color: #FFC0CB !important;
        background-image: none;
    }

    /* 제목 스타일 */
    h1 {
        color: #C2185B;
        text-align: center;
        font-family: sans-serif;
        font-weight: 800;
        margin-bottom: 20px;
        text-shadow: 1px 1px 2px rgba(255,255,255,0.5);
    }

    /* 카드 디자인 */
    .book-card {
        background: #FFFFFF;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
        text-align: center;
        border: 2px solid #F8BBD0;
        
        /* [요청사항 2] 카드 밑 여백 추가 (슬라이더와 거리 벌리기) */
        margin-bottom: 40px !important; 
    }

    /* 슬라이더 스타일 (오디오 플레이어 스타일) */
    div[data-baseweb="slider"] {
        padding-top: 10px !important;
        padding-bottom: 0px !important;
    }

    /* 트랙 (빈 부분) - 회색 */
    div[data-baseweb="slider"] > div > div:first-child {
        background-color: #9E9E9E !important;
        height: 4px !important;
    }

    /* 진행 바 (채워진 부분) - 검은색 */
    div[data-baseweb="slider"] > div > div:nth-child(2) {
        background-color: #212121 !important; 
        height: 4px !important;
    }

    /* 핸들 (손잡이) - 검은색 동그라미 */
    div[data-baseweb="slider"] div[role="slider"] {
        background-color: #212121 !important;
        box-shadow: none !important;
        width: 18px !important;
        height: 18px !important;
        top: -8px !important; 
    }

    /* 숫자 팝업 숨김 */
    div[data-testid="stSliderTickBarMin"], 
    div[data-testid="stSliderTickBarMax"],
    div[data-baseweb="tooltip"] {
        display: none !important;
    }

    /* 탭 스타일 */
    .stTabs [data-baseweb="tab"] { 
        background: rgba(255,255,255,0.6); 
        border-radius: 10px; 
        border: none;
        margin-right: 5px; 
    }
    .stTabs [aria-selected="true"] { 
        background: #EC407A !important; 
        color: white !important; 
        font-weight: bold;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        border: none;
        background: white;
        color: #000;
        border-radius: 50%;
        width: 45px;
        height: 45px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        transition: 0.2s;
    }
    .stButton > button:hover {
        background: #F8BBD0;
        transform: scale(1.1);
    }
</style>
'''
# ---------------- CSS 디자인 끝 ----------------

st.set_page_config(page_title="Pink Audio Player", layout="centered")
st.markdown(css_code, unsafe_allow_html=True)

if 'reading_list' not in st.session_state:
    st.session_state.reading_list = [{
        "id": 1, 
        "title": "도파민네이션", 
        "author": "애나 렘키", 
        "progress": 45, 
        "total": 300
    }]
if 'finished_list' not in st.session_state:
    st.session_state.finished_list = []

st.title("🎧 My Reading Playlist")

tab1, tab2 = st.tabs(["▶ Now Playing", "✔ Done"])

with tab1:
    with st.expander("➕ 새 책 추가하기"):
        with st.form("add"):
            t = st.text_input("제목")
            a = st.text_input("저자")
            p = st.number_input("총 페이지", value=300)
            if st.form_submit_button("추가 💖") and t:
                new_book = {
                    "id": datetime.now().timestamp(), 
                    "title": t, 
                    "author": a, 
                    "progress": 0, 
                    "total": p
                }
                st.session_state.reading_list.append(new_book)
                st.rerun()

    for i, book in enumerate(st.session_state.reading_list):
        # 1. 카드
        st.markdown(f'''
        <div class="book-card">
            <h3 style="margin:0; font-size:1.4rem; color:#333;">🎵 {book['title']}</h3>
            <p style="color:#666; font-size:1rem; margin-top:8px;">{book['author']}</p>
            <p style="color:#EC407A; font-weight:bold; font-size:1.2rem; margin-top:10px;">
                {book['progress']}%
            </p>
        </div>
        ''', unsafe_allow_html=True)

        # 2. 슬라이더
        val = st.slider(f"s_{i}", 0, 100, book['progress'], label_visibility="collapsed")

        # 3. 컨트롤러 및 페이지 정보
        c_left, c_mid, c_right = st.columns([2, 6, 2])
        
        # 현재 페이지 계산 (여기서 계산하므로 NameError 발생 안 함)
        curr_p = int(book['total'] * val / 100)
        
        with c_left:
            st.markdown(f"<div style='margin-top:12px; font-weight:bold; color:#555;'>{curr_p} p</div>", unsafe_allow_html=True)
            
        with c_mid:
            col_b1, col_b2, col_b3 = st.columns(3)
            with col_b1: st.button("⏮", key=f"prev_{i}")
            with col_b2:
                if st.button("■", key=f"fin_{i}", help="완독 처리"):
                    book['date'] = datetime.now().strftime("%Y-%m-%d")
                    st.session_state.finished_list.append(book)
                    st.session_state.reading_list.pop(i)
                    st.rerun()
            with col_b3: st.button("⏭", key=f"next_{i}")

        with c_right:
            st.markdown(f"<div style='text-align:right; margin-top:12px; color:#555;'>{book['total']} p</div>", unsafe_allow_html=True)

        # 값 업데이트
        if val != book['progress']:
            st.session_state.reading_list[i]['progress'] = val
            st.rerun()
            
        st.markdown("<br><br>", unsafe_allow_html=True) 

with tab2:
    if st.session_state.finished_list:
        st.balloons()
        st.markdown("### 🏆 명예의 전당")
        df = pd.DataFrame(st.session_state.finished_list)[['title', 'author', 'date']]
        st.table(df)
    else:
        st.info("아직 완독한 책이 없어요 🍰")
