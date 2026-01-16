import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.font_manager as fm
import os

# =====================================================
# 1️⃣ 한글 폰트 설정 (단일 · 덮어쓰기 없음)
# =====================================================
font_path = os.path.join(os.getcwd(), "malgun.ttf")

if os.path.exists(font_path):
    fm.fontManager.addfont(font_path)
    font_name = fm.FontProperties(fname=font_path).get_name()
    plt.rcParams["font.family"] = font_name
else:
    st.warning("⚠ malgun.ttf 폰트 파일을 찾을 수 없습니다.")

plt.rcParams["axes.unicode_minus"] = False

# =====================================================
# 2️⃣ Streamlit UI
# =====================================================
st.title("🐶 경기도 반려동물 등록현황 분석기")

file_path = "반려동물등록현황.csv"

try:
    # -------------------------------------------------
    # 데이터 로드
    # -------------------------------------------------
    df = pd.read_csv(file_path, encoding="cp949")
    st.success("반려동물 데이터를 성공적으로 불러왔습니다!")

    with st.expander("데이터 원본 보기"):
        st.write(df.head())

    # -------------------------------------------------
    # 분석 컬럼 선택
    # -------------------------------------------------
    numeric_cols = df.select_dtypes(include=["number"]).columns.tolist()
    if "기준년도" in numeric_cols:
        numeric_cols.remove("기준년도")

    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        selected_city = st.selectbox(
            "확인하고 싶은 시군을 선택하세요:",
            ["전체"] + list(df["시군명"].unique())
        )
    with col2:
        selected_val = st.selectbox(
            "비교할 항목을 선택하세요:",
            numeric_cols
        )

    # -------------------------------------------------
    # 데이터 필터링
    # -------------------------------------------------
    if selected_city == "전체":
        plot_df = df.groupby("시군명")[selected_val].sum().reset_index()
        x_axis = "시군명"
    else:
        plot_df = df[df["시군명"] == selected_city]
        x_axis = "읍면동명"

    # -------------------------------------------------
    # 그래프
    # -------------------------------------------------
    st.subheader(f"📍 {selected_city} - {selected_val} 현황")

    fig, ax = plt.subplots(figsize=(12, 7))

    plot_df = plot_df.sort_values(by=selected_val, ascending=False)

    sns.barplot(
        data=plot_df,
        x=x_axis,
        y=selected_val,
        palette="magma",
        ax=ax
    )

    ax.set_title(f"{selected_city} 지역별 {selected_val} 비교", fontsize=16)
    ax.set_xlabel(x_axis)
    ax.set_ylabel(selected_val)
    plt.xticks(rotation=45)

    st.pyplot(fig)

    st.info(
        f"💡 선택된 데이터의 총 {selected_val} 합계는 "
        f"**{plot_df[selected_val].sum():,.0f}** 입니다."
    )

except FileNotFoundError:
    st.error(f"파일을 찾을 수 없습니다: {file_path}")
except Exception as e:
    st.error(f"오류가 발생했습니다: {e}")
