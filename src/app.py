import streamlit as st
import pandas as pd
import plotly.express as px
from config import STRINGS, RISKY_BEHAVIORS
from data_loader import load_data, generate_dummy_data
from analysis import analyze_driver_risk
from calculator import calculate_impact

def main():
    st.set_page_config(page_title=STRINGS["report_title"], layout="wide")
    
    st.title(f"📊 {STRINGS['report_title']}")
    
    # Sidebar for File Upload
    st.sidebar.header("📁 데이터 업로드")
    uploaded_file = st.sidebar.file_uploader("엑셀 파일을 업로드하세요", type=["xlsx"])
    
    # Load Data
    # Reload trigger check
    if uploaded_file:
        df = load_data(uploaded_file)
    else:
        st.sidebar.info("업로드된 파일이 없어 샘플 데이터를 생성하여 사용합니다.")
        dummy_path = generate_dummy_data()
        df = load_data(dummy_path)
        
    if df is not None:
        # Preprocessing: Ensure date is datetime
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'])
            
        # Analysis
        risk_df = analyze_driver_risk(df)
        final_df = calculate_impact(risk_df)
        
        # Display Overview Metrics
        st.header(STRINGS["summary_header"])
        c1, c2, c3, c4 = st.columns(4)
        total_drivers = len(final_df)
        total_fuel_loss = final_df['Estimated Fuel Wasted (L)'].sum()
        total_co2 = final_df['CO2 Emission (kg)'].sum()
        
        total_distance = df['총운행거리(km)'].sum() if '총운행거리(km)' in df.columns else 0
        
        c1.metric("분석 대상 차량", f"{total_drivers}대")
        c2.metric("총 운행 거리", f"{total_distance:,.0f} km")
        c3.metric("총 예상 연료 낭비", f"{total_fuel_loss:,.1f} {STRINGS['unit_fuel']}")
        c4.metric("총 탄소 배출량", f"{total_co2:,.1f} {STRINGS['unit_co2']}")
        
        st.divider()
        
        # Main Layout
        tab1, tab2 = st.tabs(["종합 현황", "운전자별 상세 리포트"])
        
        with tab1:
            st.subheader(f"🏆 {STRINGS['ranking']}")
            
            # Top Risky Drivers Chart
            top_risky = final_df.sort_values('Total Penalty Score', ascending=False).head(10)
            fig = px.bar(
                top_risky, 
                x='Driver Name', 
                y='Total Penalty Score',
                color='Total Penalty Score',
                title='위험 운전 점수 상위 10인 (높을수록 위험)',
                labels={'Total Penalty Score': '위험 점수', 'Driver Name': '운전자명'},
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # Behavior Breakdown
            st.subheader("유형별 위험 행동 발생 건수")
            behavior_sums = df[[k for k in RISKY_BEHAVIORS.keys()]].sum().rename(
                index={k: v['label_ko'] for k, v in RISKY_BEHAVIORS.items()}
            ).sort_values(ascending=True)
            
            fig2 = px.bar(
                x=behavior_sums.values,
                y=behavior_sums.index,
                orientation='h',
                title="전체 위험 행동 분포",
                labels={'x': '발생 건수', 'y': '행동 유형'}
            )
            st.plotly_chart(fig2, use_container_width=True)

        with tab2:
            st.subheader("📋 개인별 안전운전 리포트")
            
            # Driver Selector
            driver_list = final_df['Driver Name'].unique()
            selected_driver = st.selectbox("운전자를 선택하세요", driver_list)
            
            if selected_driver:
                d_data = final_df[final_df['Driver Name'] == selected_driver].iloc[0]
                
                # Driver Score Card
                col1, col2 = st.columns([1, 2])
                
                with col1:
                    score = d_data['Safety Score']
                    score_color = "green" if score >= 80 else "orange" if score >= 60 else "red"
                    st.markdown(f"""
                    <div style="text-align: center; border: 2px solid #ddd; padding: 20px; border-radius: 10px;">
                        <h3>{STRINGS['total_score']}</h3>
                        <h1 style="color: {score_color}; font-size: 60px;">{int(score)}{STRINGS['unit_score']}</h1>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.write("")
                    st.metric(STRINGS["fuel_saved"] + " (절감 가능)", f"{d_data['Estimated Fuel Wasted (L)']:,.1f} L")
                    st.metric(STRINGS["co2_reduced"] + " (저감 가능)", f"{d_data['CO2 Emission (kg)']:,.1f} kg")

                with col2:
                    st.markdown(f"**{selected_driver}** 님의 운전 습관 분석:")
                    
                    # Radar Chart or Bar Chart for this driver's behaviors
                    driver_behaviors = d_data[list(RISKY_BEHAVIORS.keys())].rename(
                        {k: v['label_ko'] for k, v in RISKY_BEHAVIORS.items()}
                    )
                    # Filter only non-zero or top 5
                    driver_behaviors = driver_behaviors[driver_behaviors > 0]
                    
                    if not driver_behaviors.empty:
                        fig3 = px.pie(
                            values=driver_behaviors.values,
                            names=driver_behaviors.index,
                            title=f"{selected_driver}님의 주요 위험 행동",
                            hole=0.4
                        )
                        st.plotly_chart(fig3, use_container_width=True)
                    else:
                        st.success("위험 행동이 감지되지 않았습니다. 안전 운전 중입니다!")

    else:
        st.error("데이터 로드에 실패했습니다. 파일을 확인해주세요.")

if __name__ == "__main__":
    main()
