"""
Thống kê cho dashboard (Hiếu viết, Chính gọi).

HỢP ĐỒNG HÀM (6 hàm, xem khối chú thích "HỢP ĐỒNG HÀM" ở giữa file):
    chuan_bi(df)                  lọc dòng khảo sát thật, thêm cột số (GPA_muc, <cột>_so)
    ty_le_nhom(df, cot)           bảng tỉ lệ GPA từ 3.2 trở lên theo nhóm, kèm n
    ty_le_toan_mau(df)            % GPA từ 3.2 trở lên của cả mẫu
    spearman(df, cot_so)          (rho, p) giữa GPA và một cột số
    mann_whitney(df, cot, a, b)   dict so sánh mức GPA giữa hai nhóm
    kruskal(df, cot)              dict so sánh mức GPA giữa các nhóm

Ngoài ra có các hàm chi tiết dùng cho notebook 02 và file ket_qua_thong_ke.csv
(tan_suat_ty_le_gpa, ty_le_gpa_muc_4_5, gpa_trung_vi, diem_tb_likert, tuong_quan_spearman,
so_sanh_nhom, tao_bang_ket_qua) theo docs/chi_so_thong_ke.md mục 1.1 đến 1.6.

Dữ liệu vào: DataFrame đọc từ data/clean/vnu_that_sach.csv (cột tiếng Việt, giá trị đã giải mã
thành nhãn chữ). Các hàm cũng chấp nhận cột còn ở dạng mã số 1-5.

    import pandas as pd
    from thong_ke import chuan_bi, ty_le_nhom, ty_le_toan_mau
    df = chuan_bi(pd.read_csv("data/clean/vnu_that_sach.csv"))
    print(ty_le_toan_mau(df), ty_le_nhom(df, "Giới tính"))

Quy tắc: GPA chỉ có 5 mức thứ bậc, nên chỉ dùng tần suất, tỉ lệ, trung vị và kiểm định phi tham số.
Kết luận về sinh viên thật chỉ rút ra từ Nguon = "Khao sat that".

Chạy thử:  python dashboard/thong_ke.py
"""
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

# ----------------------------------------------------------------------------
# Cấu hình theo đúng tên cột trong file sạch
# ----------------------------------------------------------------------------
GPA_COL = "Điểm GPA"
COT_THOI_GIAN = ["TG tự học", "TG dành cho bạn bè", "TG dùng mạng xã hội"]
LIKERT = ["Mức độ thích nghi ĐH", "Phương pháp học tập", "Sự hỗ trợ từ Trường",
          "Sự hỗ trợ từ Giảng viên", "Cơ sở vật chất", "Chất lượng Giảng viên",
          "Chương trình đào tạo", "Sự cạnh tranh trong lớp", "Ảnh hưởng từ bạn bè"]
COT_NGUON = "Nguon"
COT_TRA_LOI_DEU = "Tra_loi_deu"
NGUON_THAT = "Khao sat that"
N_TOI_THIEU = 30

NHAN_GPA = {1: "Kém (Dưới 2.0)", 2: "Trung bình (2.0 - 2.5)", 3: "Khá (2.5 - 3.2)",
            4: "Giỏi (3.2 - 3.6)", 5: "Xuất sắc (Trên 3.6)"}

# Nhãn trong file sạch -> mức số (đúng thứ tự thứ bậc)
_GPA_SO = {"Kém (Dưới 2.0)": 1, "Trung bình (2.0 - 2.5)": 2, "Khá (2.5 - 3.2)": 3,
           "Giỏi (3.2 - 3.6)": 4, "Xuất sắc (Trên 3.6)": 5}
_LIKERT_SO = {"Hoàn toàn không": 1, "Ít": 2, "Bình thường": 3, "Nhiều": 4, "Rất nhiều": 5}
_TG_NGAN = ["Dưới 1 giờ", "Từ 1 đến dưới 2 giờ", "Từ 2 đến dưới 3 giờ",
            "Từ 3 đến dưới 4 giờ", "Hơn 4 giờ"]
_TG_HOC = ["Dưới 2 giờ", "Từ 2 đến dưới 4 giờ", "Từ 4 đến dưới 6 giờ",
           "Từ 6 đến dưới 8 giờ", "Hơn 8 giờ"]
_TG_SO = {"TG tự học": _TG_HOC, "TG dành cho bạn bè": _TG_NGAN, "TG dùng mạng xã hội": _TG_NGAN}
_THU_TU_NHOM = {
    "Năm học": ["Năm nhất", "Năm hai", "Năm ba", "Năm tư", "Đã tốt nghiệp"],
    "Học vấn của Bố": ["Tiểu học", "THCS", "THPT", "Cao đẳng", "Đại học/Sau đại học", "Khác"],
    "Học vấn của Mẹ": ["Tiểu học", "THCS", "THPT", "Cao đẳng", "Đại học/Sau đại học", "Khác"],
    "TG tự học": _TG_HOC,
}


# ----------------------------------------------------------------------------
# Hàm phụ trợ (không thuộc 6 hàm của hợp đồng)
# ----------------------------------------------------------------------------
def doc_du_lieu(duong_dan=None, chi_dong_that=True):
    """Đọc vnu_that_sach.csv. Mặc định chỉ giữ dòng khảo sát thật (Nguon = 'Khao sat that')."""
    if duong_dan is None:
        goc = Path(__file__).resolve().parents[1]
        duong_dan = goc / "data" / "clean" / "vnu_that_sach.csv"
    df = pd.read_csv(duong_dan)
    if chi_dong_that and COT_NGUON in df.columns:
        df = df[df[COT_NGUON] == NGUON_THAT].reset_index(drop=True)
    return df


def _so_hoa(cot, bang):
    """Đổi một cột (nhãn chữ hoặc số) thành mức số 1-5; giá trị lạ thành NaN."""
    if pd.api.types.is_numeric_dtype(cot):
        return cot.astype(float)
    return cot.map(bang).astype(float)


def _gpa_so(df):
    return _so_hoa(df[GPA_COL], _GPA_SO)


def _likert_so(df, ten_cot):
    return _so_hoa(df[ten_cot], _LIKERT_SO)


def _thoi_gian_so(df, ten_cot):
    thu_tu = _TG_SO[ten_cot]
    return _so_hoa(df[ten_cot], {v: i + 1 for i, v in enumerate(thu_tu)})


# ----------------------------------------------------------------------------
# 1.1  Tần suất và tỉ lệ từng mức GPA
# ----------------------------------------------------------------------------
def tan_suat_ty_le_gpa(df):
    """Trả về bảng 5 dòng (mức 1-5): Mức, Nhãn, Số SV (f_i), Tỉ lệ (%) = f_i / n * 100.
    Mức không có ai vẫn hiện với 0."""
    muc = _gpa_so(df).dropna().astype(int)
    n = len(muc)
    dem = muc.value_counts().reindex(range(1, 6), fill_value=0)
    return pd.DataFrame({
        "Mức": dem.index,
        "Nhãn": [NHAN_GPA[i] for i in dem.index],
        "Số SV": dem.values,
        "Tỉ lệ (%)": (dem.values / n * 100).round(2) if n else np.zeros(5),
    })


# ----------------------------------------------------------------------------
# 1.2  Tỉ lệ đạt mức 4-5 (GPA từ 3.2 trở lên)
# ----------------------------------------------------------------------------
def ty_le_gpa_muc_4_5(df):
    """Trả về (tỉ lệ %, số SV mức 4-5, n). Chỉ tính Giỏi + Xuất sắc, không gộp Khá."""
    muc = _gpa_so(df).dropna()
    n = len(muc)
    so_dat = int((muc >= 4).sum())
    return (so_dat / n * 100 if n else float("nan")), so_dat, n


# ----------------------------------------------------------------------------
# 1.3  Mức GPA trung vị
# ----------------------------------------------------------------------------
def gpa_trung_vi(df):
    """Trả về (mức trung vị, nhãn). Là một MỨC thứ bậc, không phải điểm lẻ hệ 4.
    Nếu n chẵn và hai giá trị giữa khác nhau thì mức có dạng x.5 và nhãn là 'giữa mức x và x+1'."""
    muc = _gpa_so(df).dropna()
    if muc.empty:
        return float("nan"), "Không có dữ liệu"
    tv = float(muc.median())
    if tv.is_integer():
        return int(tv), NHAN_GPA[int(tv)]
    return tv, f"Giữa mức {int(tv)} và {int(tv) + 1}"


# ----------------------------------------------------------------------------
# 1.4  Điểm trung bình các câu Likert (nhóm B)
# ----------------------------------------------------------------------------
def diem_tb_likert(df, bo_tra_loi_deu=False):
    """Trả về bảng 9 yếu tố: Yếu tố, Điểm TB (1-5), n, sắp giảm dần.
    bo_tra_loi_deu=True: loại các dòng gắn cờ Tra_loi_deu (chọn một mức ở cả 9 câu) để kiểm tra độ nhạy."""
    if bo_tra_loi_deu and COT_TRA_LOI_DEU in df.columns:
        df = df[~df[COT_TRA_LOI_DEU].astype(bool)]
    hang = []
    for c in LIKERT:
        x = _likert_so(df, c).dropna()
        hang.append({"Yếu tố": c, "Điểm TB (1-5)": round(float(x.mean()), 2) if len(x) else np.nan,
                     "n": int(len(x))})
    return pd.DataFrame(hang).sort_values("Điểm TB (1-5)", ascending=False, ignore_index=True)


# ----------------------------------------------------------------------------
# 1.5  Tương quan hạng Spearman với GPA
# ----------------------------------------------------------------------------
def _muc_do(rho):
    r = abs(rho)
    return "Rất yếu" if r < 0.2 else "Yếu" if r < 0.4 else "Trung bình" if r < 0.6 else "Mạnh"


def tuong_quan_spearman(df, cac_cot=None):
    """Trả về bảng Spearman giữa GPA và từng biến thời gian (mặc định 3 biến thời gian).
    Cột: Biến, Hệ số Spearman, p-value, n, Mức độ. Biến không đổi giá trị thì bỏ qua."""
    gpa = _gpa_so(df)
    hang = []
    for c in (cac_cot or COT_THOI_GIAN):
        x = _thoi_gian_so(df, c)
        m = x.notna() & gpa.notna()
        if m.sum() > 2 and x[m].nunique() > 1 and gpa[m].nunique() > 1:
            rho, p = stats.spearmanr(x[m], gpa[m])
            hang.append({"Biến": c, "Hệ số Spearman": round(float(rho), 3),
                         "p-value": float(p), "n": int(m.sum()), "Mức độ": _muc_do(rho)})
    return pd.DataFrame(hang, columns=["Biến", "Hệ số Spearman", "p-value", "n", "Mức độ"])


# ----------------------------------------------------------------------------
# 1.6  So sánh theo nhóm nhân khẩu học
# ----------------------------------------------------------------------------
def so_sanh_nhom(df, nhom, bien="GPA"):
    """So sánh `bien` giữa các nhóm của cột `nhom` (Năm học, Giới tính, Diện chính sách,
    Học vấn của Bố/Mẹ, TG tự học, ...). `bien` = "GPA" hoặc tên một cột Likert.

    Trả về (bang, kiem_dinh):
      bang: mỗi nhóm một dòng: Nhóm, n, Trung vị, % GPA từ 3.2 (chỉ khi bien = GPA) hoặc Điểm TB (Likert), Đủ mẫu.
      kiem_dinh: dict {Kiểm định, Thống kê, p-value, Ghi chú}. 2 nhóm: Mann-Whitney U;
                 trên 2 nhóm: Kruskal-Wallis H. Nhóm n < 30 không đưa vào kiểm định.
    """
    y = _gpa_so(df) if bien == "GPA" else _likert_so(df, bien)
    d = pd.DataFrame({"nhom": df[nhom], "y": y}).dropna()
    nhan = d["nhom"].unique()
    thu_tu = _THU_TU_NHOM.get(nhom, [])
    nhan = [v for v in thu_tu if v in nhan] + sorted(v for v in nhan if v not in thu_tu)

    hang, du_mau = [], {}
    for g in nhan:
        v = d.loc[d["nhom"] == g, "y"]
        r = {"Nhóm": g, "n": int(len(v)), "Trung vị": float(v.median()),
             "Đủ mẫu": len(v) >= N_TOI_THIEU}
        if bien == "GPA":
            r["% GPA từ 3.2"] = round(float((v >= 4).mean() * 100), 2)
        else:
            r["Điểm TB"] = round(float(v.mean()), 2)
        hang.append(r)
        if len(v) >= N_TOI_THIEU:
            du_mau[g] = v.values
    bang = pd.DataFrame(hang)

    kd = {"Kiểm định": None, "Thống kê": np.nan, "p-value": np.nan, "Ghi chú": ""}
    if len(du_mau) < 2:
        kd["Ghi chú"] = "Cần ít nhất 2 nhóm có n >= 30 để kiểm định."
    else:
        try:
            if len(du_mau) == 2:
                s, p = stats.mannwhitneyu(*du_mau.values(), alternative="two-sided")
                kd["Kiểm định"] = "Mann-Whitney U"
            else:
                s, p = stats.kruskal(*du_mau.values())
                kd["Kiểm định"] = "Kruskal-Wallis H"
            kd["Thống kê"], kd["p-value"] = float(s), float(p)
        except ValueError as e:        # ví dụ mọi giá trị giống hệt nhau
            kd["Ghi chú"] = f"Không kiểm định được: {e}"
        loai = [g for g in nhan if g not in du_mau]
        if loai:
            kd["Ghi chú"] = "Bỏ nhóm n < 30: " + ", ".join(map(str, loai))
    return bang, kd


# ----------------------------------------------------------------------------
# HỢP ĐỒNG HÀM (Chính gọi từ dashboard):
#   chuan_bi(df)                    -> df đã lọc dòng thật, thêm cột số
#   ty_le_nhom(df, cot)             -> bảng: tỉ lệ GPA từ 3.2 trở lên theo từng nhóm của `cot`, kèm n
#   ty_le_toan_mau(df)              -> % GPA từ 3.2 trở lên của cả mẫu
#   spearman(df, cot_so)            -> (rho, p) giữa GPA và cột số `cot_so`
#   mann_whitney(df, cot, a, b)     -> dict so sánh mức GPA giữa nhóm a và nhóm b của `cot`
#   kruskal(df, cot)                -> dict so sánh mức GPA giữa mọi nhóm của `cot`
# Các hàm chạy được cả trên df thô lẫn df đã qua chuan_bi (chạy lại chuan_bi không hại gì).
# ----------------------------------------------------------------------------
def chuan_bi(df):
    """Lọc dòng khảo sát thật (Nguon = 'Khao sat that') và thêm cột số: GPA_muc, <Likert>_so,
    <biến thời gian>_so (mức 1-5). Không xóa dòng trả lời một mức (cờ Tra_loi_deu vẫn giữ nguyên)."""
    d = df.copy()
    if COT_NGUON in d.columns:
        d = d[d[COT_NGUON] == NGUON_THAT]
    d = d.reset_index(drop=True)
    d["GPA_muc"] = _gpa_so(d)
    for c in LIKERT:
        if c in d.columns:
            d[c + "_so"] = _likert_so(d, c)
    for c in COT_THOI_GIAN:
        if c in d.columns:
            d[c + "_so"] = _thoi_gian_so(d, c)
    return d


def _cot_so(df, cot):
    """Lấy cột `cot` dạng số: nhận tên cột số có sẵn (vd 'TG tự học_so') hoặc tên cột nhãn chữ."""
    if cot in df.columns and cot.endswith("_so"):
        return df[cot].astype(float)
    base = cot[:-3] if cot.endswith("_so") else cot
    if base == GPA_COL or base == "GPA_muc":
        return _gpa_so(df)
    if base in _TG_SO:
        return _thoi_gian_so(df, base)
    if base in LIKERT:
        return _likert_so(df, base)
    if base in df.columns and pd.api.types.is_numeric_dtype(df[base]):
        return df[base].astype(float)
    raise KeyError(f"Không có cột số '{cot}'")


def _thu_tu(cot, nhan):
    nhan = list(nhan)
    thu_tu = _THU_TU_NHOM.get(cot, [])
    return [v for v in thu_tu if v in nhan] + sorted(v for v in nhan if v not in thu_tu)


def ty_le_toan_mau(df):
    """% sinh viên có GPA từ 3.2 trở lên (mức 4-5) trên cả mẫu (số thực, 0-100)."""
    return ty_le_gpa_muc_4_5(df)[0]


def ty_le_nhom(df, cot):
    """Bảng một dòng mỗi nhóm của `cot`: cột `cot`, n, 'Số SV GPA từ 3.2', 'Tỉ lệ GPA từ 3.2 (%)'.
    Nhóm xếp theo thứ tự tự nhiên (năm học, học vấn...) nếu biết, còn lại theo bảng chữ cái."""
    d = pd.DataFrame({"nhom": df[cot], "muc": _gpa_so(df)}).dropna()
    hang = []
    for g in _thu_tu(cot, d["nhom"].unique()):
        m = d.loc[d["nhom"] == g, "muc"]
        hang.append({cot: g, "n": int(len(m)), "Số SV GPA từ 3.2": int((m >= 4).sum()),
                     "Tỉ lệ GPA từ 3.2 (%)": round(float((m >= 4).mean() * 100), 2)})
    return pd.DataFrame(hang, columns=[cot, "n", "Số SV GPA từ 3.2", "Tỉ lệ GPA từ 3.2 (%)"])


def spearman(df, cot_so):
    """(rho, p) giữa mức GPA và cột số `cot_so`. Trả (nan, nan) nếu một bên không đổi giá trị."""
    x, y = _cot_so(df, cot_so), _gpa_so(df)
    m = x.notna() & y.notna()
    if m.sum() < 3 or x[m].nunique() < 2 or y[m].nunique() < 2:
        return float("nan"), float("nan")
    rho, p = stats.spearmanr(x[m], y[m])
    return float(rho), float(p)


def mann_whitney(df, cot, a, b):
    """Mann-Whitney U (hai phía) cho mức GPA giữa nhóm `a` và nhóm `b` của cột `cot`.
    Trả về dict: nhom_a, nhom_b, n_a, n_b, U, p, ghi_chu (U và p là nan nếu không tính được)."""
    muc = _gpa_so(df)
    xa, xb = muc[df[cot] == a].dropna(), muc[df[cot] == b].dropna()
    kq = {"nhom_a": a, "nhom_b": b, "n_a": int(len(xa)), "n_b": int(len(xb)),
          "U": float("nan"), "p": float("nan"), "ghi_chu": ""}
    if len(xa) == 0 or len(xb) == 0:
        kq["ghi_chu"] = "Một trong hai nhóm không có dòng nào"
        return kq
    try:
        u, p = stats.mannwhitneyu(xa, xb, alternative="two-sided")
        kq["U"], kq["p"] = float(u), float(p)
    except ValueError as e:
        kq["ghi_chu"] = f"Không kiểm định được: {e}"
    if min(len(xa), len(xb)) < N_TOI_THIEU:
        kq["ghi_chu"] = (kq["ghi_chu"] + "; " if kq["ghi_chu"] else "") + "Có nhóm n < 30, không nên kết luận"
    return kq


def kruskal(df, cot):
    """Kruskal-Wallis H cho mức GPA giữa các nhóm của `cot` (chỉ nhóm n >= 30 tham gia).
    Trả về dict: H, p, bac_tu_do, so_nhom, n, ghi_chu (H và p là nan nếu không tính được)."""
    d = pd.DataFrame({"nhom": df[cot], "muc": _gpa_so(df)}).dropna()
    lon, nho = [], []
    for g in _thu_tu(cot, d["nhom"].unique()):
        v = d.loc[d["nhom"] == g, "muc"].values
        (lon if len(v) >= N_TOI_THIEU else nho).append((g, v))
    kq = {"H": float("nan"), "p": float("nan"), "bac_tu_do": max(len(lon) - 1, 0),
          "so_nhom": len(lon), "n": int(sum(len(v) for _, v in lon)), "ghi_chu": ""}
    if nho:
        kq["ghi_chu"] = "Bỏ nhóm n < 30: " + ", ".join(str(g) for g, _ in nho)
    if len(lon) < 2:
        kq["ghi_chu"] = (kq["ghi_chu"] + "; " if kq["ghi_chu"] else "") + \
            "Cần ít nhất 2 nhóm có n >= 30 để kiểm định"
        return kq
    try:
        h, p = stats.kruskal(*[v for _, v in lon])
        kq["H"], kq["p"] = float(h), float(p)
    except ValueError as e:
        kq["ghi_chu"] = (kq["ghi_chu"] + "; " if kq["ghi_chu"] else "") + f"Không kiểm định được: {e}"
    return kq


# ----------------------------------------------------------------------------
# Hàm phụ: gom mọi chỉ số thành một bảng dài để xuất data/clean/ket_qua_thong_ke.csv
# ----------------------------------------------------------------------------
NHOM_MANN_WHITNEY = ["Giới tính", "Diện chính sách", "Hộ nghèo", "Dân tộc thiểu số"]
NHOM_KRUSKAL = ["Năm học", "Học vấn của Bố", "Học vấn của Mẹ", "TG tự học"]


def tao_bang_ket_qua(df, ten_mau):
    """Bảng dài, mỗi dòng một số: chi_so, nhom, n, gia_tri, p, mau, ghi_chu.
    - n: cỡ mẫu dùng để tính con số đó. p: p-value của phép kiểm định của chỉ số
      (với chỉ số theo nhóm, p là của cả phép so sánh nên lặp lại ở mọi nhóm cùng chỉ số).
    - mau: tên tập mẫu (để phân biệt lần chạy có / không có dòng trả lời một mức).
    """
    hang = []

    def them(chi_so, nhom, n, gia_tri, p=np.nan, ghi_chu=""):
        hang.append({"chi_so": chi_so, "nhom": nhom, "n": int(n),
                     "gia_tri": round(float(gia_tri), 4) if pd.notna(gia_tri) else np.nan,
                     "p": float(p) if pd.notna(p) else np.nan,
                     "mau": ten_mau, "ghi_chu": ghi_chu})

    n_all = int(_gpa_so(df).notna().sum())
    for _, r in tan_suat_ty_le_gpa(df).iterrows():                       # 1.1
        them("Tần suất GPA", r["Nhãn"], n_all, r["Số SV"])
        them("Tỉ lệ GPA (%)", r["Nhãn"], n_all, r["Tỉ lệ (%)"])
    tl, _, n_ = ty_le_gpa_muc_4_5(df)                                    # 1.2
    them("Tỉ lệ GPA mức 4-5 (%)", "Toàn mẫu", n_, tl)
    tv, nhan_tv = gpa_trung_vi(df)                                       # 1.3
    them("Mức GPA trung vị", "Toàn mẫu", n_all, tv, ghi_chu=nhan_tv)
    for _, r in diem_tb_likert(df).iterrows():                           # 1.4
        them(f"Điểm TB {r['Yếu tố']}", "Toàn mẫu", r["n"], r["Điểm TB (1-5)"])
    for _, r in tuong_quan_spearman(df).iterrows():                      # 1.5
        them(f"Spearman GPA ~ {r['Biến']}", "Toàn mẫu", r["n"], r["Hệ số Spearman"],
             r["p-value"], r["Mức độ"])
    for nhom in NHOM_MANN_WHITNEY + NHOM_KRUSKAL:                        # 1.6
        for bien in ["GPA"] + LIKERT:
            bang, kd = so_sanh_nhom(df, nhom, bien)
            for _, r in bang.iterrows():
                gc = "; ".join(x for x in [kd["Kiểm định"] or "",
                                           "" if r["Đủ mẫu"] else "n < 30, không kết luận"] if x)
                if bien == "GPA":
                    them(f"Tỉ lệ GPA mức 4-5 (%) theo {nhom}", r["Nhóm"], r["n"],
                         r["% GPA từ 3.2"], kd["p-value"], gc)
                    them(f"Trung vị mức GPA theo {nhom}", r["Nhóm"], r["n"],
                         r["Trung vị"], kd["p-value"], gc)
                else:
                    them(f"Điểm TB {bien} theo {nhom}", r["Nhóm"], r["n"],
                         r["Điểm TB"], kd["p-value"], gc)
    return pd.DataFrame(hang)


# ----------------------------------------------------------------------------
# Chạy thử nhanh:  python dashboard/thong_ke.py
# ----------------------------------------------------------------------------
if __name__ == "__main__":
    pd.set_option("display.width", 160, "display.max_columns", 20)
    data = doc_du_lieu()
    print(f"n = {len(data)} dòng khảo sát thật\n")
    print("--- Hợp đồng hàm ---")
    d = chuan_bi(data)
    print("ty_le_toan_mau:", round(ty_le_toan_mau(d), 2))
    print(ty_le_nhom(d, "Giới tính"), "\n")
    print("spearman(TG tự học_so):", spearman(d, "TG tự học_so"))
    print("mann_whitney:", mann_whitney(d, "Giới tính", "Nam", "Nữ"))
    print("kruskal:", kruskal(d, "Năm học"), "\n--- Chỉ số chi tiết ---\n")
    print("1.1 Tần suất & tỉ lệ GPA\n", tan_suat_ty_le_gpa(data), "\n")
    tl, so, n = ty_le_gpa_muc_4_5(data)
    print(f"1.2 Tỉ lệ GPA mức 4-5: {tl:.2f}% ({so}/{n})\n")
    print("1.3 Mức GPA trung vị:", gpa_trung_vi(data), "\n")
    print("1.4 Điểm TB Likert (toàn mẫu)\n", diem_tb_likert(data), "\n")
    print("1.4 Điểm TB Likert (bỏ trả lời đều)\n", diem_tb_likert(data, bo_tra_loi_deu=True), "\n")
    print("1.5 Spearman với GPA\n", tuong_quan_spearman(data), "\n")
    for nhom in ["Giới tính", "Diện chính sách", "Năm học", "Học vấn của Bố", "TG tự học"]:
        b, k = so_sanh_nhom(data, nhom)
        print(f"1.6 So sánh GPA theo {nhom}\n", b, "\n", k, "\n")