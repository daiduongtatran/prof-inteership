"""
Tab thứ 5: Gợi ý học tập (Chính viết, gọi hàm thống kê của Hiếu từ thong_ke.py).
"""
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

try:
    from dashboard.thong_ke import (
        N_TOI_THIEU,
        kruskal,
        mann_whitney,
        spearman,
        ty_le_toan_mau,
    )
except ImportError:
    from thong_ke import (
        N_TOI_THIEU,
        kruskal,
        mann_whitney,
        spearman,
        ty_le_toan_mau,
    )

# 5 yếu tố theo yêu cầu: phương pháp học, thích nghi, tự học, mạng xã hội, bạn bè
YEU_TO_GOI_Y = {
    "Phương pháp học tập": "Phương pháp học tập",
    "Mức độ thích nghi ĐH": "Mức độ thích nghi ĐH",
    "Thời gian tự học": "TG tự học",
    "Thời gian dùng mạng xã hội": "TG dùng mạng xã hội",
    "Ảnh hưởng từ bạn bè": "Ảnh hưởng từ bạn bè",
}

THU_TU_GOP = ["Mức 1–3 (Thấp/TB)", "Mức 4 (Cao)", "Mức 5 (Rất cao)"]

_LIKERT_MAP = {
    "Hoàn toàn không": 1,
    "Ít": 2,
    "Bình thường": 3,
    "Nhiều": 4,
    "Rất nhiều": 5,
}
_TG_HOC_MAP = {
    "Dưới 2 giờ": 1,
    "Từ 2 đến dưới 4 giờ": 2,
    "Từ 4 đến dưới 6 giờ": 3,
    "Từ 6 đến dưới 8 giờ": 4,
    "Hơn 8 giờ": 5,
}
_TG_NGAN_MAP = {
    "Dưới 1 giờ": 1,
    "Từ 1 đến dưới 2 giờ": 2,
    "Từ 2 đến dưới 3 giờ": 3,
    "Từ 3 đến dưới 4 giờ": 4,
    "Hơn 4 giờ": 5,
}


def _lay_muc_so(df: pd.DataFrame, ten_cot: str) -> pd.Series:
    """Chuyển cột yếu tố về thang số 1-5."""
    if ten_cot + "_so" in df.columns:
        return df[ten_cot + "_so"].astype(float)
    s = df[ten_cot]
    if pd.api.types.is_numeric_dtype(s):
        return s.astype(float)
    if ten_cot == "TG tự học":
        return s.map(_TG_HOC_MAP).astype(float)
    if ten_cot in ("TG dùng mạng xã hội", "TG dành cho bạn bè"):
        return s.map(_TG_NGAN_MAP).astype(float)
    return s.map(_LIKERT_MAP).astype(float)


def _gop_nhom_dong(muc_so: pd.Series, nhan_gop: list) -> pd.Series:
    """Gộp mức 1-5 thành 3 nhóm linh hoạt theo nhãn được truyền vào."""
    def _doi(x):
        if pd.isna(x):
            return np.nan
        x = int(x)
        if x in (1, 2, 3):
            return nhan_gop[0]
        if x == 4:
            return nhan_gop[1]
        if x == 5:
            return nhan_gop[2]
        return np.nan
    return muc_so.map(_doi)

def ve_tab_goi_y(df: pd.DataFrame):
    """Hiển thị tab Gợi ý học tập trên Dashboard."""
    st.subheader("💡 Gợi ý học tập & Khuyến nghị từ dữ liệu")

    if df is None or df.empty:
        st.warning("Không có dòng nào khớp bộ lọc hiện tại.")
        return

    # 1. Ô chọn yếu tố
    nhan_chon = st.selectbox(
        "Chọn yếu tố để xem tỉ lệ GPA từ 3.2 trở lên theo nhóm gộp",
        list(YEU_TO_GOI_Y.keys()),
        key="sb_goi_y_yeu_to",
    )
    ten_cot = YEU_TO_GOI_Y[nhan_chon]

    # 2. XÁC ĐỊNH NHÃN ĐỘNG CHO TỪNG BIẾN (Theo yêu cầu Task 4)
    if ten_cot == "TG tự học":
        nhan_gop = ["Dưới 6 giờ", "6–8 giờ", "Trên 8 giờ"]
    elif ten_cot in ("TG dùng mạng xã hội", "TG dành cho bạn bè"):
        nhan_gop = ["Dưới 3 giờ", "3–4 giờ", "Trên 4 giờ"]
    else:
        nhan_gop = ["Mức 1–3 (Thấp/TB)", "Mức 4 (Cao)", "Mức 5 (Rất cao)"]

    d = df.copy()
    d["_muc_so"] = _lay_muc_so(d, ten_cot)
    d["Nhóm gộp"] = _gop_nhom_dong(d["_muc_so"], nhan_gop)
    d = d.dropna(subset=["Nhóm gộp", "GPA_muc"]).reset_index(drop=True)

    if d.empty:
        st.warning("Không đủ dữ liệu hợp lệ để phân tích yếu tố này.")
        return

    ty_le_chung = round(float(ty_le_toan_mau(d)), 1)
    
    # Tính tương quan Spearman để lấy rho (Theo yêu cầu Task 4)
    rho, p_val_spearman = spearman(d, ten_cot)
    chuoi_rho = f"|ρ| = {abs(rho):.2f}" if not pd.isna(rho) else "|ρ| không tính được"

    # Tính bảng đối chiếu
    hang = []
    for nhom in nhan_gop:
        sub = d[d["Nhóm gộp"] == nhom]
        n_nhom = int(len(sub))
        so_dat = int((sub["GPA_muc"] >= 4).sum()) if n_nhom > 0 else 0
        tl_nhom = round(float((sub["GPA_muc"] >= 4).mean() * 100), 1) if n_nhom > 0 else 0.0
        hang.append({
            "Nhóm gộp": nhom,
            "n": n_nhom,
            "Số SV GPA ≥ 3.2": so_dat,
            "Tỉ lệ GPA từ 3.2 (%)": tl_nhom,
            "Nhãn cột": f"{nhom} (n={n_nhom})",
            "Đủ mẫu": "n ≥ 30" if n_nhom >= N_TOI_THIEU else "n < 30 (quá ít mẫu)",
        })
    bang_gop = pd.DataFrame(hang)

    kd_kruskal = kruskal(d, "Nhóm gộp")
    p_val = kd_kruskal.get("p", float("nan"))
    if pd.isna(p_val):
        nhom_du = [r["Nhóm gộp"] for r in hang if r["n"] >= N_TOI_THIEU]
        if len(nhom_du) == 2:
            p_val = mann_whitney(d, "Nhóm gộp", nhom_du[0], nhom_du[1]).get("p", float("nan"))
        else:
            p_val = p_val_spearman

    # 3. Vẽ biểu đồ cột
    fig = px.bar(
        bang_gop,
        x="Nhãn cột",
        y="Tỉ lệ GPA từ 3.2 (%)",
        color="Đủ mẫu",
        color_discrete_map={"n ≥ 30": "#1f77b4", "n < 30 (quá ít mẫu)": "#b0b0b0"},
        text=bang_gop.apply(lambda r: f"{r['Tỉ lệ GPA từ 3.2 (%)']:.1f}%", axis=1),
        title=f"Tỉ lệ GPA từ 3.2 trở lên theo nhóm gộp: {nhan_chon}",
    )
    fig.add_hline(
        y=ty_le_chung, line_dash="dash", line_color="#d62728",
        annotation_text=f"Chuẩn toàn mẫu: {ty_le_chung:.1f}% (n={len(d)})",
        annotation_position="top right",
    )
    fig.update_layout(xaxis_title=None, yaxis_title="% sinh viên có GPA ≥ 3.2", legend_title=None)
    st.plotly_chart(fig, width="stretch")

    # 4. Tự sinh câu gợi ý
    st.markdown("#### 📌 Nhận xét theo nhóm gộp")
    for _, r in bang_gop.iterrows():
        ten_x = r["Nhóm gộp"]
        n_x = int(r["n"])
        a_pct = r["Tỉ lệ GPA từ 3.2 (%)"]

        if n_x < N_TOI_THIEU:
            st.warning(f"- **Nhóm {ten_x}** (n = {n_x}): **quá ít mẫu**, không nhận xét.")
        elif pd.isna(p_val) or p_val >= 0.05:
            st.info(
                f"- **Nhóm {ten_x}**: tỉ lệ GPA ≥ 3.2 là {a_pct:.1f}% (n = {n_x}) so với {ty_le_chung:.1f}% toàn mẫu "
                f"— **chưa thấy liên hệ rõ** (p ≥ 0,05). Mối liên hệ yếu ({chuoi_rho}), không phải nhân quả."
            )
        else:
            st.write(
                f"- *Nhóm {ten_x} có tỉ lệ GPA ≥ 3.2 là {a_pct:.1f}% (n = {n_x}) so với {ty_le_chung:.1f}% toàn mẫu. "
                f"Mối liên hệ yếu ({chuoi_rho}), không phải nhân quả.*"
            )

    # 5. Bảng đối chiếu bên dưới
    st.markdown("#### 📋 Bảng đối chiếu số liệu theo nhóm gộp")
    bang_hien_thi = bang_gop[["Nhóm gộp", "n", "Số SV GPA ≥ 3.2", "Tỉ lệ GPA từ 3.2 (%)", "Đủ mẫu"]]
    st.dataframe(bang_hien_thi.rename(columns={"n": "Số SV (n)"}), width="stretch", hide_index=True)

    # 6. Gợi ý cho nhà trường
    st.markdown("---")
    st.markdown("#### 🏫 Gợi ý cho nhà trường")
    st.info(
        "Hai yếu tố có điểm trung bình thấp nhất là **Mức độ thích nghi ĐH (3,46)** và **Phương pháp học tập (3,62)**.\n\n"
        "- **Hỗ trợ thích nghi:** Tăng cường buổi định hướng, cố vấn học tập.\n"
        "- **Bồi dưỡng phương pháp:** Tổ chức chuyên đề tự học, quản lý thời gian.\n"
        f"- *Lưu ý:* Mối liên hệ với GPA là rất yếu ({chuoi_rho}) và **không khẳng định quan hệ nhân quả**."
    )