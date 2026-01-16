import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

import matplotlib.font_manager as fm
import matplotlib.pyplot as plt
import os

# 폰트 파일 경로 지정 (파일이 파이썬 파일과 같은 폴더에 있어야 함)
font_path = os.path.join(os.getcwd(), 'malgun.ttf')

# 폰트가 있는지 확인 후 적용
if os.path.exists(font_path):
    font_prop = fm.FontProperties(fname=font_path)
    plt.rcParams['font.family'] = font_prop.get_name()
    plt.rc('font', family=font_prop.get_name())
else:
    st.warning("폰트 파일을 찾을 수 없어 기본 폰트를 사용합니다.")

plt.rcParams['axes.unicode_minus'] = False
# --- 한글 폰트 설정 ---
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False

st.title("🐶 경기도 반려동물 등록현황 분석기")
file_path = "반려동물등록현황.csv"

try:
    # 1. 데이터 불러오기 (인코딩 유지)
    df = pd.read_csv(file_path, encoding='cp949')
    st.success("반려동물 데이터를 성공적으로 불러왔습니다!")

    # 데이터 미리보기
    with st.expander("데이터 원본 보기"):
        st.write(df.head())

    # 2. 분석할 항목 필터링 (숫자로 된 열만 선택)
    # 기준년도, 시군명, 읍면동명 등 글자로 된 열은 제외하고 선택지를 만듭니다.
    numeric_cols = df.select_dtypes(include=['number']).columns.tolist()
    # '기준년도'는 통계 수치가 아니므로 제외 (선택사항)
    if '기준년도' in numeric_cols:
        numeric_cols.remove('기준년도')

    st.divider()

    # 3. 사용자 선택 UI
    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox("확인하고 싶은 시군을 선택하세요:", ["전체"] + list(df['시군명'].unique()))
    with col2:
        selected_val = st.selectbox("비교할 항목을 선택하세요:", numeric_cols)

    # 4. 데이터 필터링
    if selected_city == "전체":
        # 전체 데이터일 경우 시군별로 합산하여 그래프 그리기
        plot_df = df.groupby('시군명')[selected_val].sum().reset_index()
        x_axis = '시군명'
    else:
        # 특정 시군 선택 시 해당 시군의 읍면동별 데이터 추출
        plot_df = df[df['시군명'] == selected_city]
        x_axis = '읍면동명'

    # 5. 그래프 그리기
    st.subheader(f"📍 {selected_city} - {selected_val} 현황")
    
    fig, ax = plt.subplots(figsize=(12, 7))
    
    # 데이터가 너무 많을 수 있으므로 값이 큰 순서대로 정렬
    plot_df = plot_df.sort_values(by=selected_val, ascending=False)
    
    sns.barplot(data=plot_df, x=x_axis, y=selected_val, ax=ax, palette='magma')

    # 그래프 디테일 설정
    plt.xticks(rotation=45)
    ax.set_title(f"{selected_city} 지역별 {selected_val} 비교", fontsize=16)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(selected_val)

    st.pyplot(fig)

    # 6. 간단한 통계 요약
    st.info(f"💡 선택된 데이터의 총 {selected_val} 합계는 **{plot_df[selected_val].sum():,.0f}** 입니다.")

except FileNotFoundError:
    st.error(f"파일을 찾을 수 없습니다: {file_path}")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")