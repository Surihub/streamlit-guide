import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# 데이터 로드
file_path = 'data/gdp_data.csv'  # 업로드된 파일의 경로
gdp_data = pd.read_csv(file_path)

# 데이터 클리닝 (Unnamed 열 제거)
gdp_data = gdp_data.drop(columns=[col for col in gdp_data.columns if 'Unnamed' in col])

# 국가 목록 가져오기
countries = gdp_data['Country Name'].unique()

# 페이지 제목
st.title("GDP 데이터 시각화")

# 국가 선택 (여러 국가 선택 가능)
selected_countries = st.multiselect("국가를 선택해주세요.", countries)

# 연도 선택 (슬라이더)
start_year, end_year = st.slider("조회할 연도 범위를 지정해주세요.", 1960, 2022, (2000, 2020))

# 연도 필터링
years = [str(year) for year in range(start_year, end_year + 1)]

# 대시보드 상단에 국가별 주요 지표 요약 (Total GDP, Average GDP, Year-over-year growth)
st.subheader(f"{start_year}~{end_year}까지 주요 지표 살펴보기")

col1, col2 = st.columns(2)
with col1:
    for country in selected_countries:
        country_data = gdp_data[gdp_data['Country Name'] == country]
        total_gdp = country_data[years].sum(axis=1).values[0] / 1e12  # 조 단위
        avg_gdp = country_data[years].mean(axis=1).values[0] / 1e12   # 조 단위
        st.metric(label=f"Total GDP of {country} (Trillion US$)", value=f"{total_gdp:.2f}T", delta=f"{avg_gdp:.2f}T")

with col2:
    for country in selected_countries:
        country_data = gdp_data[gdp_data['Country Name'] == country]
        max_gdp = country_data[years].max(axis=1).values[0] / 1e12  # 최대값 (조 단위)
        min_gdp = country_data[years].min(axis=1).values[0] / 1e12  # 최소값 (조 단위)
        last_year = str(end_year - 1)
        current_year = str(end_year)
        if last_year in gdp_data.columns and current_year in gdp_data.columns:
            last_year_gdp = country_data[last_year].values[0]
            current_year_gdp = country_data[current_year].values[0]
            growth_rate = ((current_year_gdp - last_year_gdp) / last_year_gdp) * 100 if last_year_gdp > 0 else 0
        else:
            growth_rate = None
        if growth_rate is not None:
            st.metric(label=f"Year-over-year growth of {country} (%)", value=f"{growth_rate:.2f}%", delta=f"{growth_rate:.2f}%")

# 선택된 국가의 GDP 시각화 (연도별 추세)
st.subheader(f"위 국가들의 GDP 트렌드({start_year} - {end_year})")
fig = go.Figure()
for country in selected_countries:
    country_data = gdp_data[gdp_data['Country Name'] == country]
    gdp_values = country_data[years].values.flatten() / 1e12  # 조 단위 변환
    fig.add_trace(go.Scatter(x=years, y=gdp_values, mode='lines+markers', name=country))
fig.update_layout(title="GDP Trend by Country (Trillion US$)", xaxis_title="Year", yaxis_title="GDP (Trillion US$)", template="plotly_white")
st.plotly_chart(fig)

# 특정 연도의 국가별 GDP 히스토그램
st.subheader("국가별 GDP 분포")
selected_year = st.slider("히스토그램을 그릴 연도를 선택해주세요.", 1960, 2022, 2020)
selected_year_data = gdp_data[['Country Name', str(selected_year)]].dropna()
selected_year_data[str(selected_year)] = selected_year_data[str(selected_year)] / 1e12
hist_fig = px.histogram(selected_year_data, x=str(selected_year), nbins=20, title=f"GDP Distribution in {selected_year} (Trillion US$)", labels={str(selected_year): "GDP (Trillion US$)"}, template="plotly_white")
st.plotly_chart(hist_fig)
