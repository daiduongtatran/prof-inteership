"""
Bổ sung dòng MÔ PHỎNG (có gắn nhãn) vào bộ dữ liệu khảo sát VNU để demo dashboard.

Nguyên tắc:
- KHÔNG sửa bất kỳ dòng khảo sát thật nào.
- Mọi dòng mô phỏng đều có Nguon = "Mo phong bo sung".
- Kết luận về sinh viên thật chỉ rút ra từ Nguon = "Khao sat that".
Đặt file này ở thư mục gốc dự án (hoặc notebooks/), chạy: python dataset.py
"""
from pathlib import Path
import numpy as np
import pandas as pd

# ---------- Tham số (ghi lại vào báo cáo) ----------
SEED = 2026
N_NAM1 = 300                              # số dòng mô phỏng năm 1
N_NAM2 = 300                              # số dòng mô phỏng năm 2
TY_LE_NAM = 0.40                          # tỉ lệ nam trong dòng mô phỏng (mã 1 = Nam)
PHAN_BO_TU_HOC = [0.10, 0.20, 0.30, 0.25, 0.15]   # mức 1..5 của Time_Studying

# ---------- Tự tìm thư mục gốc dự án và file dữ liệu ----------
try:
    day = Path(__file__).resolve().parent
except NameError:                      # chạy trong Jupyter
    day = Path.cwd().resolve()
GOC = next((p for p in [day, *day.parents] if (p / "data" / "raw").exists()), None)
if GOC is None:
    raise SystemExit("Khong tim thay thu muc data/raw. Hay dat script trong thu muc du an.")

RAW = GOC / "data" / "raw"
CLEAN = GOC / "data" / "clean"
CLEAN.mkdir(parents=True, exist_ok=True)

ds_file = sorted(RAW.glob("Database_paper*.xls*"))
if not ds_file:
    raise SystemExit(f"Khong thay file Database_paper*.xlsx trong {RAW}\n"
                     f"Cac file dang co: {[f.name for f in RAW.iterdir()]}")
INPUT = ds_file[0]
OUTPUT = CLEAN / "VNU_co_mo_phong_bo_sung.csv"
print("Doc file:", INPUT)
LIKERT = ["Adapt_Learning_Uni", "Study_Methods", "SupportOf_Uni", "SupportOf_Lec",
          "Facilitie_Uni", "Quality_Lecturer", "TrainingCurriculum",
          "Competitive_Class", "InfuenceF_Friends"]

rng = np.random.default_rng(SEED)
real = pd.read_excel(INPUT, sheet_name=0)   # sheet đầu tiên (Sheet1); bỏ qua Sheet17 thừa
real_goc = real.copy()
real["Nguon"] = "Khao sat that"


def tao_mo_phong(n, nam):
    """Lấy mẫu lại (bootstrap) các dòng thật để giữ nguyên quan hệ giữa các cột
    (kể cả quan hệ yếu với GPA), rồi chỉ thay Year, Gender, Time_Studying."""
    mau = real.drop(columns="Nguon").sample(
        n=n, replace=True, random_state=int(rng.integers(1_000_000_000))).copy()
    mau["Year"] = nam
    gioi = np.array([1] * round(n * TY_LE_NAM) + [2] * (n - round(n * TY_LE_NAM)))
    rng.shuffle(gioi)                      # đúng tỉ lệ nam đã đặt, thứ tự ngẫu nhiên
    mau["Gender"] = gioi
    mau["Time_Studying"] = rng.choice([1, 2, 3, 4, 5], size=n, p=PHAN_BO_TU_HOC)
    mau["Nguon"] = "Mo phong bo sung"
    return mau


df = pd.concat([real, tao_mo_phong(N_NAM1, 1), tao_mo_phong(N_NAM2, 2)],
               ignore_index=True)
df.insert(0, "STT", range(1, len(df) + 1))

# Kiểm tra: dòng thật không bị thay đổi
assert df[df["Nguon"] == "Khao sat that"].drop(columns=["STT", "Nguon"]) \
    .reset_index(drop=True).equals(real_goc), "Dòng thật bị thay đổi!"

df.to_csv(OUTPUT, index=False, encoding="utf-8-sig")

# ---------- Báo cáo nhanh ----------
thc = df[df["Nguon"] == "Khao sat that"]
print("Số dòng theo nguồn:\n", df["Nguon"].value_counts(), "\n")
print("Year (tất cả):\n", df["Year"].value_counts().sort_index(), "\n")
print("Ty le nam: that = %.1f%% | mô phỏng = %.1f%% | chung = %.1f%%" % (
    (thc.Gender == 1).mean() * 100,
    (df[df.Nguon != "Khao sat that"].Gender == 1).mean() * 100,
    (df.Gender == 1).mean() * 100))
print("\nTime_Studying (%), thật vs chung:")
print(pd.DataFrame({
    "that": thc["Time_Studying"].value_counts(normalize=True).sort_index() * 100,
    "chung": df["Time_Studying"].value_counts(normalize=True).sort_index() * 100}).round(1))
print("\nTương quan với GPA, thật vs chung (kiểm tra quan hệ không bị thổi phồng):")
print(pd.DataFrame({
    "that": thc.drop(columns=["STT", "Nguon"]).corr()["GPA"],
    "chung": df.drop(columns=["STT", "Nguon"]).corr()["GPA"]}).round(2).drop("GPA"))
print("\nDòng thật trả lời 1 mức duy nhất ở cả 9 câu Likert:",
      (thc[LIKERT].nunique(axis=1) == 1).sum())