# Báo Cáo Chất Lượng Dữ Liệu

**Nguồn dữ liệu kiểm tra:** 
- Dữ liệu khảo sát gốc: `data/raw/Database_paper.xlsx` (Sheet1 gồm 2.170 dòng, 22 cột)
- Từ điển dữ liệu: `data/raw/CODEBOOK.docx`

---

## 1. Bảng số liệu chất lượng dữ liệu

Kết quả kiểm tra thực tế trên tập dữ liệu thật (2.170 dòng):

| Tiêu chí | Số lượng | Tỉ lệ (ước tính) | Ghi chú & Đánh giá |
| :--- | :--- | :--- | :--- |
| **Dữ liệu thiếu (Missing)** | 0 | 0% | 100% các ô đều có dữ liệu đầy đủ. |
| **Dữ liệu trùng (Duplicates)** | 226 | ~10.4% | Xuất hiện 226 bản ghi trùng lặp hoàn toàn trên dữ liệu thật. Nhóm thống nhất **gắn cờ** để phân tích so sánh giữa tập có và không có các dòng này, không xóa trực tiếp do không có mã định danh cá nhân. |
| **Sai định dạng** | 0 | 0% | Định dạng các trường hoàn toàn đồng nhất ở dạng số nguyên (int64). |
| **Ngoài miền codebook** | 0 | 0% | Toàn bộ giá trị nằm đúng trong thang đo (1–5 hoặc 1–6) theo quy định của CODEBOOK.docx. |
| **Trả lời một mức (Straight-lining)** | 442 | ~20.4% | Có 442 dòng sinh viên chọn cùng 1 mức điểm cho toàn bộ 9 câu hỏi Likert nhóm B trên dữ liệu thật. Cần gắn cờ kiểm soát chất lượng phản hồi. |

---

## 2. Các vấn đề cấu trúc và chuẩn hóa cần xử lý

- **Lỗi chính tả tên cột:** Có 3 tên cột cần được chuẩn hóa lại theo đúng quy chuẩn:
  1. `Time_SocicalMedia` -> Chuẩn hóa: `Time_SocialMedia` (thừa chữ "c").
  2. `Facilitie_Uni` -> Chuẩn hóa: `Facilities_Uni` (thiếu chữ "s").
  3. `InfuenceF_Friends` -> Chuẩn hóa: `Influence_Friends` (thiếu chữ "l" và thừa ký tự "F_").
- **Dữ liệu thừa:** File Excel gốc tồn tại một sheet rác là `Sheet17`, cần loại bỏ khỏi luồng xử lý tự động.
- **Quyền riêng tư:** Dữ liệu khảo sát vốn không chứa các thông tin định danh cá nhân (Họ tên, Mã sinh viên, Email, SĐT), do đó không cần thực hiện thêm bước ẩn danh.