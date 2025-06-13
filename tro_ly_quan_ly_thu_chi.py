# Trợ lý theo dõi thu chi cá nhân - Giao diện No-code (Streamlit)

import streamlit as st
import datetime
import pandas as pd
import altair as alt

st.set_page_config(page_title="Trợ lý Thu Chi", layout="centered")
st.title("📘 Trợ lý Theo Dõi Thu Chi Cá Nhân")

# Khởi tạo danh sách giao dịch
if 'giao_dich' not in st.session_state:
    st.session_state.giao_dich = []

# Nhập thông tin giao dịch
st.subheader("➕ Thêm Giao Dịch")
col1, col2 = st.columns(2)
so_tien = col1.number_input("Số tiền (VND)", min_value=0, step=1000)
loai = col2.selectbox("Loại giao dịch", ["chi", "thu"])
mo_ta = st.text_input("Mô tả")
ngay = st.date_input("Ngày giao dịch", value=datetime.date.today())

if st.button("Thêm giao dịch"):
    giao_dich = {
        'ngay': ngay.isoformat(),
        'so_tien': so_tien,
        'loai': loai,
        'mo_ta': mo_ta
    }
    st.session_state.giao_dich.append(giao_dich)
    st.success(f"Đã thêm {loai}: {so_tien} VND - {mo_ta} vào ngày {ngay}")

# Hiển thị báo cáo
st.subheader("📊 Báo Cáo Giao Dịch")
if st.session_state.giao_dich:
    df = pd.DataFrame(st.session_state.giao_dich)
    df["ngay"] = pd.to_datetime(df["ngay"])

    for index, row in df.iterrows():
        st.write(f"- {row['ngay'].date()} | {row['loai'].upper()} | {row['so_tien']} VND | {row['mo_ta']}")

    tong_thu = df[df["loai"] == "thu"]["so_tien"].sum()
    tong_chi = df[df["loai"] == "chi"]["so_tien"].sum()
    con_lai = tong_thu - tong_chi

    st.markdown("---")
    st.markdown(f"**👉 Tổng thu:** {tong_thu} VND")
    st.markdown(f"**👉 Tổng chi:** {tong_chi} VND")
    st.markdown(f"**👉 Số dư còn lại:** {con_lai} VND")

    # Báo cáo tổng quan
    st.subheader("📈 Tổng Quan Giao Dịch")
    col3, col4 = st.columns(2)
    col3.metric("Số giao dịch", len(df))
    col4.metric("Khoảng thời gian", f"{df['ngay'].min().date()} → {df['ngay'].max().date()}")

    # Biểu đồ dòng tiền theo ngày
    df_grouped = df.groupby(["ngay", "loai"])["so_tien"].sum().reset_index()
    chart = alt.Chart(df_grouped).mark_bar().encode(
        x='ngay:T',
        y='so_tien:Q',
        color='loai:N',
        tooltip=['ngay:T', 'loai:N', 'so_tien:Q']
    ).properties(
        width=700,
        height=300,
        title="Chi tiêu và thu nhập theo ngày"
    )
    st.altair_chart(chart, use_container_width=True)
else:
    st.info("Chưa có giao dịch nào.")
