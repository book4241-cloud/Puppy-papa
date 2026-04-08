import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="실시간 회의 타이핑", page_icon="🎙️")
st.title("🎙️ 실시간 회의 기록기 (무료/실시간)")

st.write("아래 '🟢 실시간 인식 시작' 버튼을 누르고 마이크를 허용해 주세요. 말씀하시는 내용이 실시간으로 화면에 적힙니다!")

# 인터넷 브라우저의 실시간 음성 인식(Web Speech API) 기능을 사용하는 마법의 코드입니다.
html_code = """
<!DOCTYPE html>
<html>
<head>
<style>
  body { font-family: 'Malgun Gothic', sans-serif; }
  #result { 
    margin-top: 20px; 
    padding: 15px; 
    border: 2px solid #ddd; 
    border-radius: 10px; 
    min-height: 200px; 
    font-size: 16px;
    line-height: 1.5;
    background-color: #f9f9f9;
  }
  .btn { 
    padding: 12px 24px; 
    font-size: 16px; 
    cursor: pointer; 
    border-radius: 8px; 
    border: none; 
    color: white; 
    font-weight: bold;
    margin-right: 10px;
  }
  #start { background-color: #4CAF50; }
  #stop { background-color: #f44336; }
  .interim { color: #888; font-style: italic; }
</style>
</head>
<body>
  <div>
    <button id="start" class="btn">🟢 실시간 인식 시작</button>
    <button id="stop" class="btn">🔴 중지</button>
  </div>
  <div id="result">여기에 실시간으로 대화 내용이 표시됩니다... (마이크를 켜고 말씀해 보세요!)</div>

  <script>
    const startBtn = document.getElementById('start');
    const stopBtn = document.getElementById('stop');
    const resultDiv = document.getElementById('result');
    
    let recognition;
    // 브라우저가 실시간 음성 인식을 지원하는지 확인
    if ('webkitSpeechRecognition' in window) {
      recognition = new webkitSpeechRecognition();
      recognition.continuous = true; // 끊기지 않고 계속 듣기
      recognition.interimResults = true; // 말하는 도중에도 결과 보여주기
      
      // 언어 설정: 아래 코드를 'en-US'로 바꾸면 영어를 더 잘 인식합니다. 빈칸이면 자동 감지합니다.
      recognition.lang = ''; 
    } else {
      resultDiv.innerHTML = "현재 사용 중인 브라우저는 실시간 음성 인식을 지원하지 않습니다. 아이폰은 '사파리', 안드로이드나 PC는 '크롬(Chrome)' 브라우저를 사용해 주세요.";
    }

    if (recognition) {
      let final_transcript = '';

      recognition.onresult = (event) => {
        let interim_transcript = '';

        for (let i = event.resultIndex; i < event.results.length; ++i) {
          if (event.results[i].isFinal) {
            // 말이 한 문장 끝났을 때
            final_transcript += event.results[i][0].transcript + '<br><br>';
          } else {
            // 말하고 있는 도중일 때 (회색 글씨로 표시)
            interim_transcript += event.results[i][0].transcript;
          }
        }
        // 화면에 결과 즉시 업데이트
        resultDiv.innerHTML = final_transcript + '<span class="interim">' + interim_transcript + '</span>';
      };

      startBtn.onclick = () => {
        try {
          recognition.start();
          resultDiv.innerHTML = "🎤 듣고 있습니다... 말씀해 주세요!<br><br>";
        } catch(e) {
          console.log("이미 실행 중입니다.");
        }
      };

      stopBtn.onclick = () => {
        recognition.stop();
        resultDiv.innerHTML += "<br><b>(녹음 중지됨)</b>";
      };
    }
  </script>
</body>
</html>
"""

# 파이썬 화면에 HTML(웹 브라우저 기능)을 삽입하여 보여줍니다.
components.html(html_code, height=500)

st.info("💡 팁: 회의가 끝난 후 위 화면의 텍스트를 복사해서, 메모장에 붙여넣거나 챗GPT 등에 붙여넣고 '요약해 줘'라고 하시면 완벽합니다!")
