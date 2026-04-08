import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="미니 몬스터 배틀", page_icon="👾")

st.title("👾 야생의 몬스터가 나타났다!")

# 1. 게임 상태(세션) 초기화
# 스트림릿은 버튼을 누를 때마다 코드가 처음부터 다시 실행됩니다.
# 체력과 전투 기록을 유지하기 위해 st.session_state에 값을 저장합니다.
if "player_hp" not in st.session_state:
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = 100
    st.session_state.battle_log = ["전투가 시작되었습니다!"]
    st.session_state.game_over = False

# 2. 게임 리셋 함수
def reset_game():
    st.session_state.player_hp = 100
    st.session_state.enemy_hp = 100
    st.session_state.battle_log = ["전투가 시작되었습니다!"]
    st.session_state.game_over = False

# 3. 적의 턴 (자동 반격) 함수
def enemy_turn():
    if st.session_state.enemy_hp > 0:
        damage = random.randint(5, 15)
        st.session_state.player_hp -= damage
        st.session_state.battle_log.insert(0, f"적의 공격! 플레이어는 {damage}의 피해를 입었다!")
        
        if st.session_state.player_hp <= 0:
            st.session_state.player_hp = 0
            st.session_state.game_over = True
            st.session_state.battle_log.insert(0, "플레이어가 쓰러졌습니다... 패배!")

# 4. 플레이어 행동 함수
def attack():
    damage = random.randint(10, 20)
    st.session_state.enemy_hp -= damage
    st.session_state.battle_log.insert(0, f"플레이어의 몸통박치기! 적에게 {damage}의 피해를 입혔다!")
    
    if st.session_state.enemy_hp <= 0:
        st.session_state.enemy_hp = 0
        st.session_state.game_over = True
        st.session_state.battle_log.insert(0, "적을 물리쳤습니다! 승리!")
    else:
        enemy_turn()

def heal():
    heal_amount = random.randint(15, 25)
    st.session_state.player_hp += heal_amount
    if st.session_state.player_hp > 100:
        st.session_state.player_hp = 100
    st.session_state.battle_log.insert(0, f"플레이어의 상처약 사용! 체력을 {heal_amount} 회복했다!")
    enemy_turn()

# --- UI 화면 구성 ---

# 체력바 표시 (메트릭 사용)
col1, col2 = st.columns(2)
with col1:
    st.metric(label="내 몬스터 HP", value=f"{st.session_state.player_hp} / 100")
with col2:
    st.metric(label="야생 몬스터 HP", value=f"{st.session_state.enemy_hp} / 100")

st.divider()

# 행동 버튼 표시 (게임 오버가 아닐 때만)
if not st.session_state.game_over:
    st.subheader("무엇을 할까?")
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        st.button("⚔️ 공격 (몸통박치기)", on_click=attack, use_container_width=True)
    with btn_col2:
        st.button("💊 회복 (상처약)", on_click=heal, use_container_width=True)
else:
    st.error("게임이 종료되었습니다.")
    st.button("🔄 다시 시작하기", on_click=reset_game, use_container_width=True)

st.divider()

# 전투 로그 표시
st.subheader("📜 전투 기록")
for log in st.session_state.battle_log:
    st.write(log)
