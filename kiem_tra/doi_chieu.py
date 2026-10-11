"""
Đối chiếu số liệu: 4 thẻ KPI của dashboard (đọc bằng AppTest) so với pandas tính độc lập.

Với 12 tổ hợp bộ lọc, script:
  1. tính 4 chỉ số bằng pandas thuần (không dùng dashboard/thong_ke.py, không dùng code của app.py);
  2. chạy dashboard/app.py bằng streamlit.testing.v1.AppTest, đặt bộ lọc ở thanh bên rồi đọc thuộc tính
     `value` của các thẻ `st.metric`;
  3. so hai bên và ghi docs/doi_chieu_so_lieu.csv (cột: Tổ hợp, Chỉ số, Dashboard, Pandas, Khớp, Lý do).

Chạy từ thư mục gốc dự án:
    pip install -r requirements.txt
    python kiem_tra/doi_chieu.py              # đối chiếu đầy đủ, ghi docs/doi_chieu_so_lieu.csv
    python kiem_tra/doi_chieu.py --chi-pandas # chỉ in số pandas (không cần streamlit)

Cần data/clean/vnu_that_sach.csv (dashboard đọc file này).
Thoát với mã 1 nếu có dòng không khớp mà không có lý do.
"""
import argparse
import re
import sys
from pathlib import Path

import pandas as pd

GOC = Path(__file__).resolve().parents[1]
APP = GOC / "dashboard" / "app.py"
CSV = GOC / "data" / "clean" / "vnu_that_sach.csv"
DAU_RA = GOC / "docs" / "doi_chieu_so_lieu.csv"

# Nhãn thẻ KPI đúng như trong dashboard/app.py
CHI_SO = ["Số mẫu (n)", "Tỉ lệ GPA từ 3.2 trở lên", "Mức GPA trung vị", "Tỉ lệ GPA dưới 2.5"]

# Bảng giải mã GPA viết riêng ở đây để pandas độc lập với code dashboard
GPA_MUC = {"Kém (Dưới 2.0)": 1, "Trung bình (2.0 - 2.5)": 2, "Khá (2.5 - 3.2)": 3,
           "Giỏi (3.2 - 3.6)": 4, "Xuất sắc (Trên 3.6)": 5}
TEN_NGUON = {"Khao sat that": "Khảo sát thật", "Mo phong bo sung": "Mô phỏng bổ sung"}
# Bộ lọc ở thanh bên -> cột trong file sạch
COT = {"Nguồn dữ liệu": "Nguồn dữ liệu", "Năm học": "Năm học", "Giới tính": "Giới tính",
       "Diện chính sách": "Diện chính sách", "Hộ nghèo": "Hộ nghèo"}

# 12 tổ hợp bộ lọc. Khoá bỏ trống = giữ mặc định của dashboard
# (mặc định: nguồn = chỉ "Khảo sát thật", các bộ lọc còn lại chọn hết, không loại dòng trả lời một mức).
TO_HOP = [
    ("1. Mặc định (khảo sát thật)", {}),
    ("2. Chỉ nữ", {"Giới tính": ["Nữ"]}),
    ("3. Chỉ nam", {"Giới tính": ["Nam"]}),
    ("4. Chỉ năm ba", {"Năm học": ["Năm ba"]}),
    ("5. Chỉ năm tư", {"Năm học": ["Năm tư"]}),
    ("6. Chỉ đã tốt nghiệp", {"Năm học": ["Đã tốt nghiệp"]}),
    ("7. Chỉ có diện chính sách", {"Diện chính sách": ["Có"]}),
    ("8. Không thuộc diện chính sách", {"Diện chính sách": ["Không"]}),
    ("9. Chỉ hộ nghèo", {"Hộ nghèo": ["Có"]}),
    ("10. Nữ và có diện chính sách", {"Giới tính": ["Nữ"], "Diện chính sách": ["Có"]}),
    ("11. Mặc định, loại dòng trả lời một mức", {"bo_mot_muc": True}),
    ("12. Gồm cả dòng mô phỏng", {"Nguồn dữ liệu": ["Khảo sát thật", "Mô phỏng bổ sung"]}),
]


# ----------------------------------------------------------------------------
# Phía pandas (độc lập)
# ----------------------------------------------------------------------------
def doc_csv():
    df = pd.read_csv(CSV)
    df["muc"] = df["Điểm GPA"].map(GPA_MUC)
    df["Nguồn dữ liệu"] = df["Nguon"].map(TEN_NGUON).fillna(df["Nguon"])
    return df


def tinh_pandas(df, bo_loc):
    """Áp bộ lọc như người dùng chọn trên thanh bên rồi tính 4 chỉ số. Trả về dict số thật."""
    f = df
    mac_dinh_nguon = ["Khảo sát thật"] if "Khảo sát thật" in set(df["Nguồn dữ liệu"]) else sorted(
        df["Nguồn dữ liệu"].unique())
    for ten, cot in COT.items():
        chon = bo_loc.get(ten, mac_dinh_nguon if ten == "Nguồn dữ liệu" else None)
        if chon is not None:
            f = f[f[cot].isin(chon)]
    if bo_loc.get("bo_mot_muc"):
        f = f[~f["Tra_loi_deu"].astype(bool)]
    if f.empty:
        return None
    return {"Số mẫu (n)": len(f),
            "Tỉ lệ GPA từ 3.2 trở lên": (f["muc"] >= 4).mean() * 100,
            "Mức GPA trung vị": float(f["muc"].median()),
            "Tỉ lệ GPA dưới 2.5": (f["muc"] <= 2).mean() * 100}


def dinh_dang_pandas(chi_so, v):
    """Chuỗi hiển thị của số pandas, cùng cách làm tròn với dashboard (để so sánh được)."""
    if chi_so == "Số mẫu (n)":
        return f"{int(v):,}".replace(",", ".")
    if chi_so == "Mức GPA trung vị":
        return f"{v:g}"
    return f"{v:.1f}%"


# ----------------------------------------------------------------------------
# Phía dashboard (AppTest)
# ----------------------------------------------------------------------------
def doc_dashboard(bo_loc):
    """Chạy app.py, đặt bộ lọc, trả về ({nhãn thẻ: giá trị chữ}, thông báo lỗi hoặc '')."""
    from streamlit.testing.v1 import AppTest      # import muộn để --chi-pandas không cần streamlit

    at = AppTest.from_file(str(APP), default_timeout=120)
    at.run()
    if at.exception:
        return {}, "app.py báo lỗi khi mở: " + str(at.exception[0].value)[:200]
    for nhan, gia_tri in bo_loc.items():
        if nhan == "bo_mot_muc":
            hop = [c for c in at.sidebar.checkbox if c.label.startswith("Loại các dòng")]
            if not hop:
                return {}, "Không tìm thấy ô 'Loại các dòng trả lời một mức' ở thanh bên"
            hop[0].set_value(bool(gia_tri))
        else:
            o = [m for m in at.sidebar.multiselect if m.label == nhan]
            if not o:
                return {}, f"Không tìm thấy bộ lọc '{nhan}' ở thanh bên"
            o[0].set_value(gia_tri)
    at.run()
    if at.exception:
        return {}, "app.py báo lỗi sau khi đặt bộ lọc: " + str(at.exception[0].value)[:200]
    return {m.label: m.value for m in at.metric}, ""


def so_dashboard_ve_so(chi_so, chuoi):
    """Chuỗi hiển thị của dashboard -> số, để so dung sai (trung vị có thể là 'giữa mức a và b')."""
    if chi_so == "Số mẫu (n)":
        return float(chuoi.replace(".", "").replace(",", ""))
    if chi_so == "Mức GPA trung vị":
        m = re.search(r"giữa mức (\d)", chuoi)
        if m:
            return int(m.group(1)) + 0.5
        m = re.match(r"\s*(\d)\.", chuoi)               # nhãn dạng "3. Khá (2.5–3.2)"
        return float(m.group(1)) if m else float("nan")
    return float(chuoi.strip().rstrip("%"))



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chi-pandas", action="store_true", help="chỉ in số pandas, không chạy dashboard")
    args = ap.parse_args()

    if not CSV.exists():
        sys.exit(f"Không thấy {CSV}. Hãy chạy notebooks/01_lam_sach.ipynb để tạo file sạch.")
    df = doc_csv()

    if args.chi_pandas:
        for ten, bo_loc in TO_HOP:
            kq = tinh_pandas(df, bo_loc)
            print(ten, "->", "bộ lọc rỗng" if kq is None else
                  {k: dinh_dang_pandas(k, v) for k, v in kq.items()})
        return

    hang = []
    for ten, bo_loc in TO_HOP:
        pd_kq = tinh_pandas(df, bo_loc)
        db_kq, loi = doc_dashboard(bo_loc)
        for cs in CHI_SO:
            p_txt = "(bộ lọc rỗng)" if pd_kq is None else dinh_dang_pandas(cs, pd_kq[cs])
            d_txt = db_kq.get(cs, "(không có thẻ)")
            ly_do = loi
            if pd_kq is None:
                khop = d_txt == "(không có thẻ)"
                ly_do = ly_do or "Bộ lọc không còn dòng nào; dashboard dừng và không hiện thẻ KPI (đúng thiết kế)."
            elif cs not in db_kq:
                khop, ly_do = False, ly_do or "Dashboard không hiện thẻ này"
            else:
                a, b = so_dashboard_ve_so(cs, d_txt), pd_kq[cs]
                dung_sai = 0.05 if cs.startswith("Tỉ lệ") else 0.0   # dashboard làm tròn 1 chữ số thập phân
                khop = abs(a - b) <= dung_sai + 1e-9
                if not khop and not ly_do:
                    ly_do = "Số lệch nhau, cần kiểm tra"
            hang.append({"Tổ hợp": ten, "Chỉ số": cs, "Dashboard": d_txt, "Pandas": p_txt,
                         "Khớp": bool(khop), "Lý do": ly_do})
        print(f"{ten}: " + ("khớp" if all(r["Khớp"] for r in hang[-4:]) else "CÓ DÒNG LỆCH"))

    kq_df = pd.DataFrame(hang)
    DAU_RA.parent.mkdir(parents=True, exist_ok=True)
    kq_df.to_csv(DAU_RA, index=False, encoding="utf-8-sig")
    lech = kq_df[(~kq_df["Khớp"]) & (kq_df["Lý do"] == "")]
    print(f"\nĐã ghi {DAU_RA} ({len(kq_df)} dòng). Khớp: {int(kq_df['Khớp'].sum())}/{len(kq_df)}")
    if len(lech):
        print("Dòng lệch không có lý do:\n", lech.to_string(index=False))
        sys.exit(1)


if __name__ == "__main__":
    main()