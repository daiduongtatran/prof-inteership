# Nhật ký làm sạch dữ liệu

Notebook thực hiện: `notebooks/01_lam_sach.ipynb`. Kết quả: `data/clean/vnu_that_sach.csv`.

## 1. Chuỗi xử lý

`data/raw/Database_paper.xlsx` (Sheet1) → `dataset.py` (bổ sung dòng mô phỏng) → `data/clean/VNU_co_mo_phong_bo_sung.csv` → `notebooks/01_lam_sach.ipynb` → `data/clean/vnu_that_sach.csv`

## 2. Các bước và số dòng

| Bước | Việc làm | Dòng trước | Dòng sau | Ghi chú |
|---|---|---|---|---|
| 0 | Chọn Sheet1 của file gốc, bỏ Sheet17 | | 2.170 (22 cột) | Sheet17 chỉ lặp lại cột `Time_Friends`, hơn Sheet1 một dòng |
| 1 | `dataset.py` thêm 600 dòng mô phỏng (300 năm 1, 300 năm 2), có cột `Nguon` | 2.170 | 2.770 | Dòng thật giữ nguyên; xem `docs/tu_dien_du_lieu.md` |
| 2 | Bỏ dòng trống theo cột `STT` | 2.770 | 2.770 | Không có dòng trống |
| 3 | Đổi 3 tên cột sai chính tả: `Time_SocicalMedia`, `Facilitie_Uni`, `InfuenceF_Friends` | 2.770 | 2.770 | |
| 4 | Xóa dòng trùng hệt nhau ở mọi cột (trừ `STT`), giữ dòng đầu tiên | 2.770 | 2.539 | Xóa 231 dòng: 226 dòng thật và 5 dòng mô phỏng |
| 5 | Gắn cờ `Tra_loi_deu` (chọn đúng một mức ở cả 9 câu đánh giá) | 2.539 | 2.539 | 461 dòng được gắn cờ: 347 dòng thật và 114 dòng mô phỏng |
| 6 | Giải mã 22 cột từ số sang nhãn chữ theo codebook | 2.539 | 2.539 | Không có giá trị nào ngoài miền, không phát sinh ô trống |
| 7 | Đổi tên cột sang tiếng Việt, xuất file | 2.539 | 2.539 | 25 cột (22 cột gốc, `STT`, `Nguon`, `Tra_loi_deu`) |

## 3. Cấu trúc file kết quả

- **2.539 dòng**: 1.944 dòng khảo sát thật (`Nguon = Khao sat that`) và 595 dòng mô phỏng (`Nguon = Mo phong bo sung`).
- Dòng thật: năm ba 135, năm tư 409, đã tốt nghiệp 1.400. Dòng mô phỏng: năm nhất 297, năm hai 298.
- Không có ô thiếu, không có giá trị ngoài miền codebook, không có dữ liệu cá nhân (không tên, không mã sinh viên) nên không cần ẩn danh.

## 4. Quyết định về dòng trùng

Nhóm **chọn xóa** các dòng trùng hệt nhau ở cả 22 cột. Lý do: tránh một tổ hợp câu trả lời bị tính nhiều lần.

Hạn chế đã biết:
- Dữ liệu không có mã định danh nên **không thể phân biệt** dòng nhập lặp với dòng trùng ngẫu nhiên (câu hỏi dạng chọn mức, nhiều người chọn cùng một tổ hợp).
- Trong 226 dòng trùng thật có 95 dòng là dòng chọn một mức ở cả 9 câu, nên số dòng thật bị gắn cờ `Tra_loi_deu` giảm từ 442 xuống 347.

Tác động lên số liệu chính (dữ liệu thật):

| Chỉ số | Trước khi xóa (2.170 dòng) | Sau khi xóa (1.944 dòng) |
|---|---|---|
| Tỉ lệ GPA từ 3.2 trở lên (mức 4–5) | 36,8% | 36,0% |
| Điểm trung bình chung 9 câu đánh giá (thang 1–5) | 3,961 | 3,949 |
| Tỉ lệ nam | 11,1% | 11,2% |

Thay đổi nhỏ, không đổi kết luận.

## 5. Lưu ý khi dùng file

- `Tra_loi_deu` chỉ có ý nghĩa với dòng thật. Dòng mô phỏng mang cờ này vì được lấy mẫu lại từ dòng thật.
- Nhãn thang điểm GPA: mức 1 ghi "Kém (Dưới 2.0)" theo cách dịch của nhóm; thực chất là nhóm dưới 2.0 (gồm cả Yếu).
- Dòng mô phỏng chỉ để minh họa dashboard, không dùng để kết luận về sinh viên thật. Dashboard mặc định chỉ hiển thị dòng thật.
- Tên file `vnu_that_sach.csv` có chứa dòng mô phỏng; cột `Nguon` là cách phân biệt.
