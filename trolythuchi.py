# Trợ lý theo dõi thu chi cá nhân - Giao diện No-code (Streamlit)

import streamlit as st
import datetime

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
    for gd in st.session_state.giao_dich:
        st.write(f"- {gd['ngay']} | {gd['loai'].upper()} | {gd['so_tien']} VND | {gd['mo_ta']}")

    tong_thu = sum(gd['so_tien'] for gd in st.session_state.giao_dich if gd['loai'] == 'thu')
    tong_chi = sum(gd['so_tien'] for gd in st.session_state.giao_dich if gd['loai'] == 'chi')
    con_lai = tong_thu - tong_chi

    st.markdown("---")
    st.markdown(f"**👉 Tổng thu:** {tong_thu} VND")
    st.markdown(f"**👉 Tổng chi:** {tong_chi} VND")
    st.markdown(f"**👉 Số dư còn lại:** {con_lai} VND")
else:
    st.info("Chưa có giao dịch nào.")
