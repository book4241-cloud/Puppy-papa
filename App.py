import streamlit as st
from openai import OpenAI
from audio_recorder_streamlit import audio_recorder
import io

# 1. 웹 앱의 기본 화면 설정
st.set_page_config(page_title="글로벌 회의 요약기", page_icon="🌍")
st.title("🌍 다국어 회의 요약 앱")

# 2. 사이드바에 API 키 입력란 만들기
with st.sidebar:
    st.header("⚙️ 설정")
    api_key = st.text_input("OpenAI API 키를 입력하세요", type="password")
    st.markdown("[API 키 발급받기](https://platform.openai.com/api-keys)")

# API 키가 없으면 작동을 멈추고 안내 메시지를 띄웁니다.
if not api_key:
    st.warning("👈 왼쪽 사이드바에 OpenAI API 키를 입력해야 앱이 작동합니다.")
    st.stop()

# OpenAI 클라이언트 연결
client = OpenAI(api_key=api_key)

st.subheader("1. 회의 녹음하기")
st.write("아래 마이크 아이콘을 클릭하여 녹음을 시작하고, 다시 클릭하여 종료하세요.")

# 3. 웹 브라우저용 마이크 녹음 버튼 생성
audio_bytes = audio_recorder(text="클릭하여 녹음 시작/종료", icon_size="2x")

if audio_bytes:
    # 녹음된 음성 미리듣기 제공
    st.audio(audio_bytes, format="audio/wav")
    
    # 버튼을 누르면 AI 분석 시작
    if st.button("🚀 이 녹음 파일 분석 및 요약하기"):
        with st.spinner("음성을 텍스트로 변환 중입니다... (잠시만 기다려주세요)"):
            # 컴퓨터에 파일을 저장하지 않고 메모리 상에서 바로 AI에게 전달합니다.
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "meeting.wav"
            
            try:
                # Whisper API로 다국어 음성을 텍스트로 변환
                transcript = client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file
                )
                meeting_text = transcript.text
                
                st.success("텍스트 변환 완료!")
                st.text_area("인식된 전체 텍스트", value=meeting_text, height=150)
                
                with st.spinner("내용을 요약하고 있습니다..."):
                    # GPT 모델로 한국어 요약 생성
                    response = client.chat.completions.create(
                        model="gpt-4o",
                        messages=[
                            {"role": "system", "content": "너는 글로벌 비즈니스 전문 비서야. 제공된 텍스트의 언어를 파악하고, 전체 내용을 명확하게 이해한 뒤 핵심 내용만 Bullet Point(글머리 기호)로 요약해 줘. 요약은 한국어로 제공해 줘."},
                            {"role": "user", "content": meeting_text}
                        ]
                    )
                    summary = response.choices[0].message.content
                    
                    st.subheader("✨ 회의 핵심 요약 ✨")
                    st.info(summary)
                    
            except Exception as e:
                st.error(f"오류가 발생했습니다. API 키가 정확한지 확인해 주세요. 상세 내용: {e}")
