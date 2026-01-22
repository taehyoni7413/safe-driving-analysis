# Configuration for Safe Driving Analysis

# 11 Risky Driving Behaviors (User Provided Schema)
# Key: Internal English Key
# Value: Dictionary with 'penalty_points', 'fuel_loss_ml', 'label_ko' (Column Name in Excel)

RISKY_BEHAVIORS = {
    "Speeding": {"penalty": 20, "fuel_loss_ml": 100, "label_ko": "과속"},
    "Long Term Speeding": {"penalty": 30, "fuel_loss_ml": 200, "label_ko": "장기과속"},
    "Sudden Acceleration": {"penalty": 10, "fuel_loss_ml": 50, "label_ko": "급가속"},
    "Sudden Start": {"penalty": 10, "fuel_loss_ml": 50, "label_ko": "급출발"},
    "Sudden Deceleration": {"penalty": 10, "fuel_loss_ml": 10, "label_ko": "급감속"},
    "Sudden Stop": {"penalty": 10, "fuel_loss_ml": 10, "label_ko": "급정지"},
    "Sudden Left Turn": {"penalty": 15, "fuel_loss_ml": 20, "label_ko": "급좌회전"},
    "Sudden Right Turn": {"penalty": 15, "fuel_loss_ml": 20, "label_ko": "급우회전"},
    "Sudden U-Turn": {"penalty": 20, "fuel_loss_ml": 30, "label_ko": "급유턴"},
    "Sudden Overtaking": {"penalty": 25, "fuel_loss_ml": 40, "label_ko": "급앞지르기"},
    "Sudden Lane Change": {"penalty": 10, "fuel_loss_ml": 10, "label_ko": "급진로변경"}
}

# Fuel Prices (KRW per Liter) - Example average
FUEL_PRICE = {
    "Diesel": 1500,
    "Gasoline": 1600
}

# CO2 Emission Factors (kg CO2 per Liter)
CO2_EMISSION = {
    "Diesel": 2.68,
    "Gasoline": 2.30
}

# Report Strings (Korean Formal)
STRINGS = {
    "report_title": "운전자별 안전운전 분석 리포트",
    "total_score": "안전운전 종합 점수",
    "fuel_saved": "예상 연료 절감량",
    "co2_reduced": "탄소 배출 저감량",
    "ranking": "운전자 순위 (위험도 순)",
    "recommendation": "안전운전 가이드",
    "summary_header": "종합 분석 결과",
    "unit_fuel": "리터(L)",
    "unit_co2": "kgCO2eq",
    "unit_score": "점"
}
