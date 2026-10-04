# Báo cáo chất lượng dữ liệu

## 1. Phạm vi kiểm tra

- **Dữ liệu kiểm tra:** `data/raw/Database_paper.xlsx`, Sheet1: **2.170 phản hồi khảo sát thật, 22 cột**.
- **Từ điển và mã hóa:** `data/raw/CODEBOOK.docx`, `docs/tu_dien_du_lieu.md`.
- Các số liệu dưới đây tính trên dữ liệu thật, chưa tính 600 dòng mô phỏng bổ sung.

## 2. Kết quả kiểm tra

| Tiêu chí | Số lượng | Tỉ lệ | Ghi chú |
|---|---|---|---|
| Giá trị thiếu | 0 | 0% | Mọi ô đều có giá trị |
| Sai định dạng | 0 | 0% | Cả 22 cột đều là số nguyên |
| Ngoài miền codebook | 0 | 0% | Mọi giá trị nằm trong miền hợp lệ |
| Dòng trùng hệt nhau (22 cột) | 226 | ~10,4% | Không có mã định danh nên không phân biệt được nhập lặp với trùng ngẫu nhiên |
| Dòng chọn một mức ở cả 9 câu đánh giá | 442 | ~20,4% | Có thể là trả lời qua loa; chưa đủ cơ sở để kết luận |
| Tên cột sai chính tả | 3 | | `Time_SocicalMedia`, `Facilitie_Uni`, `InfuenceF_Friends` |
| Sheet thừa | 1 | | `Sheet17` chỉ lặp cột `Time_Friends`, hơn Sheet1 một dòng; bỏ qua |
| Thông tin cá nhân | 0 | | Không có tên, mã sinh viên: không cần ẩn danh |

## 3. Các vấn đề về nội dung dữ liệu

- **GPA tự khai, chỉ có 5 mức**, không có điểm số cụ thể.
- **Năm học:** dữ liệu thật chỉ có năm ba (135), năm tư (441) và đã tốt nghiệp (1.594); không có năm nhất, năm hai.
- **Mẫu lệch:** khoảng 89% là nữ; nhóm hộ nghèo chỉ 86 người, dân tộc thiểu số 129 người.
- **Thời gian tự học** dồn về mức cao nhất (khoảng 82%).

## 4. Cách xử lý

- Đổi tên 3 cột sai chính tả.
- Xóa dòng trùng (231 dòng gồm 226 dòng thật và 5 dòng mô phỏng) và ghi nhận hạn chế ở mục 2. Chi tiết trong `docs/nhat_ky_lam_sach.md`.
- Gắn cờ `Tra_loi_deu` thay vì xóa; dashboard có tùy chọn loại nhóm này.
- Bổ sung 600 dòng mô phỏng (năm nhất, năm hai) có gắn nhãn `Nguon`, chỉ để minh họa dashboard.

Sau xử lý: **1.944 dòng thật** (347 dòng được gắn cờ trả lời một mức) và 595 dòng mô phỏng, tổng 2.539 dòng trong `data/clean/vnu_that_sach.csv`.
