"""
Dashboard tương tác: phân tích mức học lực của sinh viên (khảo sát ĐH Giáo dục, ĐHQGHN).

Đặt file này tại  dashboard/app.py  và chạy từ thư mục gốc dự án:
    streamlit run dashboard/app.py

Dữ liệu: data/clean/vnu*sach*.csv (file sạch do nhóm tạo).
Lưu ý: GPA là tự khai, chỉ có 5 mức; dòng "Mô phỏng bổ sung" chỉ để minh họa.
"""
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st
from scipy import stats

st.set_page_config(page_title="Dashboard kết quả học tập", page_icon="📊", layout="wide")

# ----------------------------------------------------------------------------
# Cấu hình theo đúng tên cột trong file sạch
# ----------------------------------------------------------------------------
GPA_COL = "Điểm GPA"
LIKERT = ["Mức độ thích nghi ĐH", "Phương pháp học tập", "Sự hỗ trợ từ Trường",
          "Sự hỗ trợ từ Giảng viên", "Cơ sở vật chất", "Chất lượng Giảng viên",
          "Chương trình đào tạo", "Sự cạnh tranh trong lớp", "Ảnh hưởng từ bạn bè"]

EDU = ["Tiểu học", "THCS", "THPT", "Cao đẳng", "Đại học/Sau đại học", "Khác"]
TG_NGAN = ["Dưới 1 giờ", "Từ 1 đến dưới 2 giờ", "Từ 2 đến dưới 3 giờ",
           "Từ 3 đến dưới 4 giờ", "Hơn 4 giờ"]
TG_HOC = ["Dưới 2 giờ", "Từ 2 đến dưới 4 giờ", "Từ 4 đến dưới 6 giờ",
          "Từ 6 đến dưới 8 giờ", "Hơn 8 giờ"]
ORDER = {
    "Năm học": ["Năm nhất", "Năm hai", "Năm ba", "Năm tư", "Đã tốt nghiệp"],
    "Học vấn của Bố": EDU, "Học vấn của Mẹ": EDU,
    "TG dành cho bạn bè": TG_NGAN, "TG dùng mạng xã hội": TG_NGAN,
    "TG tự học": TG_HOC,
}
NHOM_SO_SANH = ["Năm học", "Giới tính", "Diện chính sách", "Hộ nghèo", "Dân tộc thiểu số",
                "Học vấn của Bố", "Học vấn của Mẹ", "TG tự học",
                "TG dùng mạng xã hội", "TG dành cho bạn bè"]

MUC_GPA = {1: "1. Dưới 2.0", 2: "2. TB (2.0–2.5)", 3: "3. Khá (2.5–3.2)",
           4: "4. Giỏi (3.2–3.6)", 5: "5. Xuất sắc (>3.6)"}
MAU_GPA = {MUC_GPA[1]: "#d62728", MUC_GPA[2]: "#ff9f40", MUC_GPA[3]: "#f2d45c",
           MUC_GPA[4]: "#6fb98f", MUC_GPA[5]: "#1f77b4"}
TEN_NGUON = {"Khao sat that": "Khảo sát thật", "Mo phong bo sung": "Mô phỏng bổ sung"}
N_TOI_THIEU = 30


# ----------------------------------------------------------------------------
# Chuyển nhãn chữ về số (không phụ thuộc cách đặt nhãn cụ thể)
# ----------------------------------------------------------------------------
def gpa_to_num(label):
    s = str(label).lower()
    if "xuất sắc" in s:
        return 5
    if "giỏi" in s:
        return 4
    if "khá" in s:
        return 3
    if "trung bình" in s:
        return 2
    if "kém" in s or "yếu" in s or "dưới 2" in s:
        return 1
    return np.nan


def likert_to_num(label):
    s = str(label).lower()
    if "hoàn toàn không" in s:
        return 1
    if "rất" in s:
        return 5
    if "nhiều" in s:          # "Nhiều" hoặc "Khá nhiều"
        return 4
    if "bình thường" in s or "vừa phải" in s:
        return 3
    if "ít" in s:
        return 2
    return np.nan


def ordered(col, values):
    known = ORDER.get(col, [])
    values = list(values)
    return [v for v in known if v in values] + sorted(v for v in values if v not in known)


@st.cache_data
def load_data():
    root = Path(__file__).resolve().parents[1]
    files = sorted((root / "data" / "clean").glob("vnu*sach*.csv"))
    if not files:
        return None, root
    df = pd.read_csv(files[0])
    df["GPA_muc"] = df[GPA_COL] if pd.api.types.is_numeric_dtype(df[GPA_COL]) else df[GPA_COL].map(gpa_to_num)
    df["Muc_GPA"] = df["GPA_muc"].map(MUC_GPA)
    for c in LIKERT:
        df[c + "_so"] = df[c] if pd.api.types.is_numeric_dtype(df[c]) else df[c].map(likert_to_num)
    df["Nguồn dữ liệu"] = df["Nguon"].map(TEN_NGUON).fillna(df["Nguon"])
    if "Tra_loi_deu" not in df.columns:
        df["Tra_loi_deu"] = False
    return df, files[0]


df, nguon_file = load_data()
if df is None:
    st.error(f"Không tìm thấy file dữ liệu sạch trong {nguon_file / 'data' / 'clean'} "
             "(tên cần dạng vnu*sach*.csv). Hãy chạy bước làm sạch trước.")
    st.stop()

# ----------------------------------------------------------------------------
# Thanh bên: bộ lọc
# ----------------------------------------------------------------------------
st.sidebar.header("Bộ lọc")
nguon_opts = sorted(df["Nguồn dữ liệu"].unique())
nguon_mac_dinh = ["Khảo sát thật"] if "Khảo sát thật" in nguon_opts else nguon_opts
sel_nguon = st.sidebar.multiselect("Nguồn dữ liệu", nguon_opts, default=nguon_mac_dinh)
sel_nam = st.sidebar.multiselect("Năm học", ordered("Năm học", df["Năm học"].unique()),
                                 default=ordered("Năm học", df["Năm học"].unique()))
sel_gioi = st.sidebar.multiselect("Giới tính", sorted(df["Giới tính"].unique()),
                                  default=sorted(df["Giới tính"].unique()))
sel_cs = st.sidebar.multiselect("Diện chính sách", sorted(df["Diện chính sách"].unique()),
                                default=sorted(df["Diện chính sách"].unique()))
sel_ngheo = st.sidebar.multiselect("Hộ nghèo", sorted(df["Hộ nghèo"].unique()),
                                   default=sorted(df["Hộ nghèo"].unique()))
bo_mot_muc = st.sidebar.checkbox("Loại các dòng trả lời một mức ở cả 9 câu đánh giá", value=False)

f = df[df["Nguồn dữ liệu"].isin(sel_nguon) & df["Năm học"].isin(sel_nam)
       & df["Giới tính"].isin(sel_gioi) & df["Diện chính sách"].isin(sel_cs)
       & df["Hộ nghèo"].isin(sel_ngheo)]
if bo_mot_muc:
    f = f[~f["Tra_loi_deu"]]

# ----------------------------------------------------------------------------
# Tiêu đề và cảnh báo
# ----------------------------------------------------------------------------
st.title("📊 Phân tích mức học lực của sinh viên")
st.caption("Nguồn: khảo sát sinh viên Trường ĐH Giáo dục, ĐHQGHN (Mendeley Data, "
           "DOI 10.17632/23ppcdbmhc.1). GPA do sinh viên tự khai, chia thành 5 mức.")

if "Mô phỏng bổ sung" in sel_nguon:
    st.warning("Bộ lọc đang bao gồm dòng **mô phỏng bổ sung**. Các dòng này chỉ để minh họa "
               "dashboard, không dùng để rút ra kết luận về sinh viên thật.")
if f.empty:
    st.warning("Không có dòng nào khớp bộ lọc hiện tại.")
    st.stop()

# ----------------------------------------------------------------------------
# Thẻ KPI
# ----------------------------------------------------------------------------
n = len(f)
ty_le_dat = (f["GPA_muc"] >= 4).mean() * 100
ty_le_thap = (f["GPA_muc"] <= 2).mean() * 100
trung_vi = f["GPA_muc"].median()
nhan_trung_vi = (MUC_GPA[int(trung_vi)] if float(trung_vi).is_integer()
                 else f"giữa mức {int(trung_vi)} và {int(trung_vi) + 1}")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Số mẫu (n)", f"{n:,}".replace(",", "."))
c2.metric("Tỉ lệ GPA từ 3.2 trở lên", f"{ty_le_dat:.1f}%", help="Mức 4 và 5 (Giỏi + Xuất sắc)")
c3.metric("Mức GPA trung vị", nhan_trung_vi)
c4.metric("Tỉ lệ GPA dưới 2.5", f"{ty_le_thap:.1f}%", help="Mức 1 và 2")
if n < N_TOI_THIEU:
    st.warning(f"Chỉ có {n} dòng, quá ít để kết luận.")

tab1, tab2, tab3, tab4 = st.tabs(["Tổng quan", "So sánh theo nhóm",
                                   "Tương quan với GPA", "Bảng số liệu"])

# ----------------------------------------------------------------------------
# Tab 1: tổng quan
# ----------------------------------------------------------------------------
with tab1:
    left, right = st.columns(2)
    with left:
        dem = f["Muc_GPA"].value_counts().reindex(list(MUC_GPA.values()), fill_value=0)
        d1 = pd.DataFrame({"Mức GPA": dem.index, "Số SV": dem.values})
        d1["Tỉ lệ (%)"] = (d1["Số SV"] / n * 100).round(1)
        d1["Nhãn"] = d1.apply(lambda r: f"{r['Số SV']} ({r['Tỉ lệ (%)']}%)", axis=1)
        fig = px.bar(d1, x="Mức GPA", y="Số SV", text="Nhãn", color="Mức GPA",
                     color_discrete_map=MAU_GPA, title="Phân bố 5 mức GPA")
        fig.update_layout(showlegend=False, xaxis_title=None)
        st.plotly_chart(fig, width="stretch")
    with right:
        tb = pd.DataFrame({"Yếu tố": LIKERT,
                           "Điểm TB (1–5)": [f[c + "_so"].mean() for c in LIKERT]})
        tb = tb.sort_values("Điểm TB (1–5)")
        fig = px.bar(tb, x="Điểm TB (1–5)", y="Yếu tố", orientation="h",
                     text=tb["Điểm TB (1–5)"].round(2), range_x=[1, 5],
                     title="Điểm trung bình các yếu tố khảo sát (thang 1–5)")
        fig.update_layout(yaxis_title=None)
        st.plotly_chart(fig, width="stretch")
    st.caption("Điểm trung bình các câu đánh giá chỉ mang tính mô tả (thang thứ bậc). "
               "Có thể bật bộ lọc 'loại các dòng trả lời một mức' ở thanh bên để so sánh.")

# ----------------------------------------------------------------------------
# Tab 2: so sánh theo nhóm
# ----------------------------------------------------------------------------
with tab2:
    nhom = st.selectbox("Chọn nhóm để so sánh", NHOM_SO_SANH)
    thu_tu = ordered(nhom, f[nhom].unique())
    g = f.groupby(nhom).agg(n=("GPA_muc", "size"),
                            dat=("GPA_muc", lambda s: (s >= 4).mean() * 100)).reindex(thu_tu)
    g["Nhãn nhóm"] = [f"{i} (n={int(r.n)})" for i, r in g.iterrows()]
    g["Đủ mẫu"] = np.where(g["n"] >= N_TOI_THIEU, "n ≥ 30", "n < 30 (không kết luận)")
    nho = g[g["n"] < N_TOI_THIEU]
    if len(nho):
        st.warning("Nhóm có dưới 30 người, không nên kết luận: " + ", ".join(map(str, nho.index)))

    a, b = st.columns(2)
    with a:
        fig = px.bar(g.reset_index(), x="Nhãn nhóm", y="dat", color="Đủ mẫu",
                     color_discrete_map={"n ≥ 30": "#1f77b4", "n < 30 (không kết luận)": "#b0b0b0"},
                     text=g["dat"].round(1).astype(str) + "%",
                     title=f"Tỉ lệ GPA từ 3.2 trở lên theo: {nhom}")
        fig.update_layout(xaxis_title=None, yaxis_title="% sinh viên", legend_title=None)
        st.plotly_chart(fig, width="stretch")
    with b:
        ct = pd.crosstab(f[nhom], f["GPA_muc"], normalize="index").reindex(thu_tu) * 100
        ct = ct.reindex(columns=[1, 2, 3, 4, 5], fill_value=0)
        ct.index = g["Nhãn nhóm"]
        long = ct.reset_index().melt(id_vars="Nhãn nhóm", var_name="Mức", value_name="Tỉ lệ")
        long["Mức GPA"] = long["Mức"].map(MUC_GPA)
        fig = px.bar(long, x="Nhãn nhóm", y="Tỉ lệ", color="Mức GPA", color_discrete_map=MAU_GPA,
                     category_orders={"Mức GPA": list(MUC_GPA.values())},
                     title=f"Cơ cấu 5 mức GPA theo: {nhom} (100%)")
        fig.update_layout(xaxis_title=None, yaxis_title="% sinh viên", legend_title=None)
        st.plotly_chart(fig, width="stretch")
    if nhom == "Năm học":
        st.caption("Dữ liệu thật chỉ có năm ba, năm tư và đã tốt nghiệp. "
                   "Năm nhất và năm hai chỉ xuất hiện ở dòng mô phỏng.")

# ----------------------------------------------------------------------------
# Tab 3: tương quan Spearman
# ----------------------------------------------------------------------------
with tab3:
    cac_bien = {}
    for c in ["TG tự học", "TG dành cho bạn bè", "TG dùng mạng xã hội"]:
        cac_bien[c] = f[c].map({v: i + 1 for i, v in enumerate(ORDER[c])})
    for c in ["Học vấn của Bố", "Học vấn của Mẹ"]:
        cac_bien[c] = f[c].map({v: i + 1 for i, v in enumerate(EDU[:-1])})  # bỏ "Khác"
    for c in LIKERT:
        cac_bien[c] = f[c + "_so"]

    def muc_do(r):
        r = abs(r)
        return "Rất yếu" if r < 0.2 else "Yếu" if r < 0.4 else "Trung bình" if r < 0.6 else "Mạnh"

    rows = []
    for ten, x in cac_bien.items():
        m = x.notna() & f["GPA_muc"].notna()
        if m.sum() > 2 and x[m].nunique() > 1:
            rho, p = stats.spearmanr(x[m], f.loc[m, "GPA_muc"])
            rows.append({"Biến": ten, "Hệ số Spearman": round(rho, 3), "p-value": p,
                         "n": int(m.sum()), "Mức độ": muc_do(rho)})
    tq = pd.DataFrame(rows).sort_values("Hệ số Spearman")
    fig = px.bar(tq, x="Hệ số Spearman", y="Biến", orientation="h", text="Hệ số Spearman",
                 range_x=[-1, 1], title="Tương quan hạng Spearman giữa từng biến và mức GPA")
    fig.update_layout(yaxis_title=None)
    st.plotly_chart(fig, width="stretch")
    tq["p-value"] = tq["p-value"].map(lambda p: "< 0.001" if p < 0.001 else f"{p:.3f}")
    st.dataframe(tq.sort_values("Hệ số Spearman", ascending=False), width="stretch",
                 hide_index=True)
    st.info("Hầu hết hệ số rất nhỏ. Với số mẫu lớn, p-value nhỏ không có nghĩa là mối liên hệ mạnh. "
            "Tương quan không phải quan hệ nhân quả.")

# ----------------------------------------------------------------------------
# Tab 4: bảng số liệu (để đối chiếu)
# ----------------------------------------------------------------------------
with tab4:
    st.subheader("Số liệu đằng sau các biểu đồ (dùng để đối chiếu)")
    st.write(f"File dữ liệu: `{Path(nguon_file).name}` | Số dòng sau lọc: **{n}**")
    t1 = f["Muc_GPA"].value_counts().reindex(list(MUC_GPA.values()), fill_value=0).rename("Số SV").to_frame()
    t1["Tỉ lệ (%)"] = (t1["Số SV"] / n * 100).round(2)
    st.markdown("**Phân bố 5 mức GPA**")
    st.dataframe(t1, width="stretch")
    st.markdown(f"**So sánh theo: {nhom}**")
    st.dataframe(g[["n", "dat"]].rename(columns={"n": "Số SV", "dat": "% GPA ≥ 3.2"}).round(2),
                 width="stretch")
    st.markdown("**Xem dữ liệu đã lọc**")
    st.dataframe(f.drop(columns=[c for c in f.columns if c.endswith("_so")] + ["Muc_GPA"]).head(200),
                 width="stretch", hide_index=True)
    st.download_button("Tải dữ liệu đã lọc (CSV)",
                       f.drop(columns=[c for c in f.columns if c.endswith("_so")] + ["Muc_GPA"])
                       .to_csv(index=False).encode("utf-8-sig"),
                       file_name="du_lieu_da_loc.csv", mime="text/csv")