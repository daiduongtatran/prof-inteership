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


def _gop_nhom_13_4_5(muc_so: pd.Series) -> pd.Series:
    """Gộp mức 1-5 thành 3 nhóm: Mức 1–3, Mức 4, Mức 5."""
    def _doi(x):
        if pd.isna(x):
            return np.nan
        x = int(x)
        if x in (1, 2, 3):
            return THU_TU_GOP[0]
        if x == 4:
            return THU_TU_GOP[1]
        if x == 5:
            return THU_TU_GOP[2]
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

    # 2. Tạo cột nhóm gộp và tính tỉ lệ bằng hàm của Hiếu
    d = df.copy()
    d["_muc_so"] = _lay_muc_so(d, ten_cot)
    d["Nhóm gộp"] = _gop_nhom_13_4_5(d["_muc_so"])
    d = d.dropna(subset=["Nhóm gộp", "GPA_muc"]).reset_index(drop=True)

    if d.empty:
        st.warning("Không đủ dữ liệu hợp lệ để phân tích yếu tố này.")
        return

    ty_le_chung = round(float(ty_le_toan_mau(d)), 1)

    # Tính bảng đối chiếu theo thứ tự nhóm gộp
    hang = []
    for nhom in THU_TU_GOP:
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

    # Kiểm định p-value qua hàm của Hiếu (kruskal / mann_whitney / spearman)
    kd_kruskal = kruskal(d, "Nhóm gộp")
    p_val = kd_kruskal.get("p", float("nan"))
    if pd.isna(p_val):
        # Nếu chỉ còn 2 nhóm có n >= 30 thì dùng Mann-Whitney hoặc Spearman
        nhom_du = [r["Nhóm gộp"] for r in hang if r["n"] >= N_TOI_THIEU]
        if len(nhom_du) == 2:
            p_val = mann_whitney(d, "Nhóm gộp", nhom_du[0], nhom_du[1]).get("p", float("nan"))
        else:
            _, p_val = spearman(d, ten_cot)

    # 3. Vẽ biểu đồ cột có đường chuẩn toàn mẫu và ghi n ở mỗi cột
    fig = px.bar(
        bang_gop,
        x="Nhãn cột",
        y="Tỉ lệ GPA từ 3.2 (%)",
        color="Đủ mẫu",
        color_discrete_map={
            "n ≥ 30": "#1f77b4",
            "n < 30 (quá ít mẫu)": "#b0b0b0",
        },
        text=bang_gop.apply(
            lambda r: f"{r['Tỉ lệ GPA từ 3.2 (%)']:.1f}% (n={int(r['n'])})", axis=1
        ),
        title=f"Tỉ lệ GPA từ 3.2 trở lên theo nhóm gộp: {nhan_chon}",
    )
    fig.add_hline(
        y=ty_le_chung,
        line_dash="dash",
        line_color="#d62728",
        annotation_text=f"Chuẩn toàn mẫu: {ty_le_chung:.1f}% (n={len(d)})",
        annotation_position="top right",
    )
    fig.update_layout(
        xaxis_title=None,
        yaxis_title="% sinh viên có GPA ≥ 3.2",
        legend_title=None,
        yaxis_range=[0, max(100, float(bang_gop["Tỉ lệ GPA từ 3.2 (%)"].max()) + 15)],
    )
    st.plotly_chart(fig, width="stretch")

    # 4. Tự sinh câu gợi ý theo mẫu quy định (không câu nào khẳng định nhân quả)
    st.markdown("#### 📌 Nhận xét theo nhóm gộp")
    for _, r in bang_gop.iterrows():
        ten_x = r["Nhóm gộp"]
        n_x = int(r["n"])
        a_pct = r["Tỉ lệ GPA từ 3.2 (%)"]

        if n_x < N_TOI_THIEU:
            st.warning(
                f"- **Nhóm {ten_x}** (n = {n_x}): **quá ít mẫu** (n < 30), không đưa ra nhận xét."
            )
        elif pd.isna(p_val) or p_val >= 0.05:
            st.info(
                f"- **Nhóm {ten_x}**: có tỉ lệ GPA từ 3.2 trở lên là {a_pct:.1f}% (n = {n_x}) "
                f"so với {ty_le_chung:.1f}% toàn mẫu — **chưa thấy liên hệ rõ** (p ≥ 0,05). "
                f"Mối liên hệ yếu, không phải nhân quả."
            )
        else:
            st.write(
                f"- *Nhóm {ten_x} có tỉ lệ GPA từ 3.2 trở lên là {a_pct:.1f}% (n = {n_x}) "
                f"so với {ty_le_chung:.1f}% toàn mẫu. Mối liên hệ yếu, không phải nhân quả.*"
            )

    # 5. Bảng đối chiếu bên dưới
    st.markdown("#### 📋 Bảng đối chiếu số liệu theo nhóm gộp")
    bang_hien_thi = bang_gop[
        ["Nhóm gộp", "n", "Số SV GPA ≥ 3.2", "Tỉ lệ GPA từ 3.2 (%)", "Đủ mẫu"]
    ].rename(columns={"n": "Số SV (n)"})
    st.dataframe(bang_hien_thi, width="stretch", hide_index=True)

    # 6. Mục "Gợi ý cho nhà trường" từ 2 yếu tố điểm thấp nhất (thích nghi 3,46, phương pháp học 3,62)
    st.markdown("---")
    st.markdown("#### 🏫 Gợi ý cho nhà trường")
    diem_thich_nghi = d["Mức độ thích nghi ĐH_so"].mean() if "Mức độ thích nghi ĐH_so" in d.columns else 3.46
    diem_pp_hoc = d["Phương pháp học tập_so"].mean() if "Phương pháp học tập_so" in d.columns else 3.62
    st.info(
        "Trong 9 câu đánh giá (thang 1–5), hai yếu tố có điểm trung bình thấp nhất trên tập khảo sát thật là "
        f"**Mức độ thích nghi ĐH (3,46)** và **Phương pháp học tập (3,62)** "
        f"*(trên bộ lọc hiện tại: Thích nghi = {diem_thich_nghi:.2f}, Phương pháp học = {diem_pp_hoc:.2f})*.\n\n"
        "- **Hỗ trợ thích nghi môi trường đại học (3,46):** Tăng cường các buổi định hướng đầu khóa, "
        "cố vấn học tập theo sát sinh viên và hoạt động kết nối đồng trang lứa để giảm bỡ ngỡ khi chuyển cấp.\n"
        "- **Bồi dưỡng phương pháp học tập (3,62):** Tổ chức chuyên đề hướng dẫn kỹ năng tự học, "
        "đọc tài liệu học thuật và quản lý thời gian ôn tập.\n"
        "- *Lưu ý học thuật:* Các con số thống kê chỉ phản ánh mức độ hài lòng/tự đánh giá của sinh viên; "
        "mối liên hệ với GPA là rất yếu (|ρ| ≤ 0,13) và **không khẳng định quan hệ nhân quả**."
    )