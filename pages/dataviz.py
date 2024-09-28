import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib  # 한글 폰트 적용
import seaborn as sns

# 데이터 로드
file_path = 'data/gdp_data.csv'  # 업로드된 파일의 경로
gdp_data = pd.read_csv(file_path)

# 데이터 클리닝 (Unnamed 열 제거)
gdp_data = gdp_data.drop(columns=[col for col in gdp_data.columns if 'Unnamed' in col])

# 국가 목록 가져오기
countries = gdp_data['Country Name'].unique()

# 페이지 제목
st.title("다중 국가 GDP 데이터 시각화")

# 국가 선택 (여러 국가 선택 가능)
selected_countries = st.multiselect("국가를 선택하세요", countries)

# 연도 선택 (슬라이더)
start_year, end_year = st.slider("연도 범위를 선택하세요", 1960, 2022, (2000, 2020))

# 시각화할 연도 필터링
years = [str(year) for year in range(start_year, end_year + 1)]

# 시각화 (여러 국가 비교)
st.subheader(f"선택된 국가의 GDP 시각화 ({start_year} - {end_year})")
fig, ax = plt.subplots(figsize=(10, 6))

# 각 선택된 국가에 대해 시각화
for country in selected_countries:
    country_data = gdp_data[gdp_data['Country Name'] == country]
    gdp_values = country_data[years].values.flatten()  # 해당 연도에 대한 GDP 값
    ax.plot(years, gdp_values, label=country, marker='o')  # 국가별 GDP 추세 그래프

# 그래프 꾸미기
ax.set_xlabel("year")
ax.set_ylabel("GDP (current US$)")
ax.set_title("GDP by Country")
plt.xticks(rotation=90)
plt.legend(title="Country")
plt.grid(True, linestyle='--', alpha=0.7)

# 그래프 출력
st.pyplot(fig)


# # 특정 연도의 국가별 GDP 히스토그램
# st.subheader("특정 연도의 국가별 GDP 히스토그램")

# # 연도 선택 슬라이더
# selected_year = st.slider("히스토그램을 위한 연도를 선택하세요", 1960, 2022, 2020)

# # 선택된 연도의 GDP 데이터 필터링
# selected_year_data = gdp_data[['Country Name', str(selected_year)]].dropna()

# # 최대 최소값을 계산하여 X축 고정
# gdp_min = gdp_data[years].min().min()  # 전체 데이터에서 최소값
# gdp_max = gdp_data[years].max().max()  # 전체 데이터에서 최대값

# # 히스토그램 시각화 (Seaborn)
# fig, ax = plt.subplots(figsize=(10, 6))
# sns.histplot(selected_year_data[str(selected_year)], binrange = [0, 10^13], color='skyblue', edgecolor='black', ax=ax)

# # X축과 Y축의 간격 고정
# ax.set_xlim(gdp_min, gdp_max)
# ax.set_ylim(0, 10)  # 빈도수 축 (히스토그램 높이)

# # 그래프 꾸미기
# ax.set_title(f"{selected_year}년 국가별 GDP 분포")
# ax.set_xlabel("GDP (current US$)")
# ax.set_ylabel("빈도수")
# plt.grid(True, linestyle='--', alpha=0.7)

# # 히스토그램 출력
# st.pyplot(fig)