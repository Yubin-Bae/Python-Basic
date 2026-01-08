import streamlit as st
import pandas as pd

# 엑셀 파일 불러오기
df = pd.read_excel('project_테스트.xlsx')

# 제목, 헤더
st.title("20Hz: MBTI기반 심리테스트")
st.header("당신의 MBTI를 알려주세요.")

# 마크다운
st.markdown('''
            ## 입력해야 할 정보
            - 이름
            - 나이
            - MBTI
            ''')

# 입력
name = st.text_input('이름을 입력해주세요: ')
mbti = st.text_input('MBTI를 입력해주세요: ')

# 단순 텍스트
st.write(f'안녕하세요, {name}님! 당신의 MBTI는 {mbti} 맞나요?')

# 버튼
if st.button('네'):
    st.success('환영합니다! 심리테스트를 시작할게요!')
if st.button('아니요'):
    st.error('그럼 다시 입력하세요.')

# 사이드바
st.sidebar.selectbox('원하는 심리테스트 유형을 선택하세요:', 
                    ['스트레스 테스트', '성격 유형 테스트', '진로 적성 테스트'])

# 데이터프레임 출력
st.dataframe(df)