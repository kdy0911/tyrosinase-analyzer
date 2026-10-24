
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="티로시나아제 분석", page_icon="🧪")

st.title("🧪 티로시나아제 억제율 분석")
st.write("흡광도를 입력해 천연물별 억제 효과를 비교하세요.")

st.subheader("1. 대조군 흡광도")

c1, c2 = st.columns(2)
with c1:
    control = st.number_input(
        "대조군 반응액", min_value=0.0,
        value=0.800, step=0.001, format="%.3f"
    )
with c2:
    control_blank = st.number_input(
        "대조군 블랭크", min_value=0.0,
        value=0.100, step=0.001, format="%.3f"
    )

st.subheader("2. 천연물 데이터")
st.caption("예시값을 실제 측정값으로 바꿔 주세요.")

example = pd.DataFrame({
    "천연물": ["계피", "녹차", "블루베리", "마늘"],
    "시료 흡광도": [0.500, 0.600, 0.450, 0.650],
    "시료 블랭크": [0.100, 0.120, 0.080, 0.100]
})

data = st.data_editor(
    example, num_rows="dynamic", use_container_width=True
)

if st.button("억제율 계산하기", type="primary"):
    if control <= control_blank:
        st.error("대조군 반응액은 대조군 블랭크보다 커야 합니다.")
    elif data.empty or data.isnull().any().any():
        st.error("모든 항목을 입력해 주세요.")
    elif (data["시료 흡광도"] < data["시료 블랭크"]).any():
        st.error("시료 흡광도는 블랭크 이상이어야 합니다.")
    elif (data["천연물"].astype(str).str.strip() == "").any():
        st.error("천연물 이름을 입력해 주세요.")
    else:
        data["보정 흡광도"] = (
            data["시료 흡광도"] - data["시료 블랭크"]
        )
        data["억제율 (%)"] = (
            1 - data["보정 흡광도"] /
            (control - control_blank)
        ) * 100

        st.subheader("3. 분석 결과")
        st.dataframe(
            data.style.format({
                "보정 흡광도": "{:.3f}",
                "억제율 (%)": "{:.2f}"
            }),
            use_container_width=True
        )

        fig, ax = plt.subplots()
        ax.bar(data["천연물"], data["억제율 (%)"])
        ax.set_ylabel("억제율 (%)")
        ax.set_title("천연물별 티로시나아제 억제 효과")
        ax.axhline(0, linewidth=0.8)
        plt.xticks(rotation=20)
        fig.tight_layout()
        st.pyplot(fig)

        st.download_button(
            "결과 CSV 다운로드",
            data=data.to_csv(index=False).encode("utf-8-sig"),
            file_name="tyrosinase_results.csv",
            mime="text/csv"
        )
