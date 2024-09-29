import streamlit as st
import pandas as pd
from datetime import datetime
from streamlit_gsheets import GSheetsConnection

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(worksheet="시트1", usecols = list(range(4)), ttl=5)
df = df.dropna(how='all')


st.title("상담 신청 현황")

st.write(df.groupby('상담신청일').size().reset_index(name='신청 인원'))

st.title("구글 시트에 데이터 입력하기")

# https://github.com/streamlit/gsheets-connection

# example/st_app_gsheets_using_service_account.py




# 미리 정해놓은 날짜와 시간 리스트
datetime_options = [
    datetime(2024, 9, 29, 14, 0),
    datetime(2024, 9, 30, 16, 30),
    datetime(2024, 10, 1, 9, 0),
    datetime(2024, 10, 2, 11, 15)
]

# Streamlit Form
with st.form(key='form1'):
    # 학번 입력
    id = st.text_input(label="학번을 입력해주세요. ")

    # 이름 입력
    name = st.text_input(label="이름을 작성해주세요. ")

    # 미리 정의된 날짜 및 시간 선택 (리스트에서 선택)
    selected_datetime = st.selectbox(
        label="원하는 날짜와 시간을 선택해주세요.",
        options=datetime_options,
        format_func=lambda x: x.strftime("%Y-%m-%d %H:%M")  # 보기 쉽게 날짜와 시간 형식 지정
    )

    # 제출 버튼
    submit_button = st.form_submit_button(label='제출')

# 날짜와 시간을 표시
if submit_button:
    if not name or not id:
        st.warning("모든 칸을 채워주세요.")
        st.stop()
    else:
        form_data = pd.DataFrame(
            [
                {
                    "일시": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # 현재 시간 포맷 적용
                    "학번": id,
                    "이름": name,
                    "상담신청일": selected_datetime.strftime("%Y-%m-%d %H:%M:%S")  # 선택된 날짜 및 시간 포맷 적용
                }
            ]
        )
        st.write(form_data)
        updated_df = pd.concat([df, form_data], ignore_index=True)
        conn.update(worksheet="시트1", data=updated_df)
        st.success("제출되었습니다.")