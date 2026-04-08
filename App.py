import streamlit as st
import google.generativeai as genai
from audio_recorder_streamlit import audio_recorder

# 1. 웹 앱의 기본 화면 설정
st.set_page_config(page_title="무료 회의 요약기", page_icon="🌍")
st.title("🌍 다국어 회의 요약 앱 (무료 버전)")

# 2. 사이드바에 Google API 키 입력란 만들기
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("Google Gemini API 키를 입력하세요", type="password")
    st.markdown("[무료 API 키 발급받기](https://aistudio.google.com/app/apikey)")
    st.caption("구글 아이디로 로그인 후 'Create API key'를 누르면 바로 발급됩니다. 카드 등록이 필요 없습니다!")

if not api_key:
    st.warning("👈 왼쪽 사이드바에 무료로 발급받은 Google API 키를 입력해 주세요.")
    st.stop()

# 3. Google Gemini AI 설정
genai.configure(api_key=api_key)
# 무료로 제공되며 오디오 분석에 뛰어난 1.5 Flash 모델 사용
model = genai.GenerativeModel('gemini-1.5-flash')

st.subheader("1. 회의 녹음하기")
st.write("아래 마이크 아이콘을 클릭하여 녹음을 시작하고, 다시 클릭하여 종료하세요.")

audio_bytes = audio_recorder(text="클릭하여 녹음 시작/종료", icon_size="2x")

if audio_bytes:
    # 녹음된 음성 미리듣기
    st.audio(audio_bytes, format="audio/wav")
    
    if st.button("🚀 이 녹음 파일 무료로 분석 및 요약하기"):
        with st.spinner("AI가 음성을 분석하고 요약 중입니다... (잠시만 기다려주세요)"):
            try:
                # 구글 AI에게 음성 파일과 함께 내릴 지시사항
                prompt = "너는 글로벌 비즈니스 전문 비서야. 제공된 회의 음성 파일의 언어를 파악하고 전체 내용을 명확하게 이해한 뒤, 핵심 내용만 Bullet Point(글머리 기호)로 요약해 줘. 요약은 반드시 한국어로 작성해 줘."
                
                # 음성 데이터를 AI가 읽을 수 있는 형태로 준비
                audio_part = {
                    "mime_type": "audio/wav",
                    "data": audio_bytes
                }
                
                # AI에게 분석 요청 (음성을 통째로 보냅니다!)
                response = model.generate_content([prompt, audio_part])
                
                st.success("무료 분석 완료!")
                st.subheader("✨ 회의 핵심 요약 ✨")
                st.info(response.text)
                
            except Exception as e:
                st.error(f"오류가 발생했습니다. 구글 API 키가 정확한지 확인해 주세요. 상세 내용: {e}")
