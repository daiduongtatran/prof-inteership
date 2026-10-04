# Báo Cáo Chất Lượng Dữ Liệu

**Nguồn dữ liệu đánh giá:** 
- Dữ liệu thô: `data/raw/Database_paper.xlsx`
- Dữ liệu đã làm sạch: `data/clean/VNU_co_mo_phong_bo_sung.csv`[cite: 1]
- Từ điển dữ liệu: `data/raw/CODEBOOK.docx`[cite: 1]

## 1. Bảng số liệu chất lượng dữ liệu

Dưới đây là các vấn đề được phát hiện trong quá trình kiểm tra dữ liệu[cite: 2]:

| Tiêu chí | Số lượng | Tỉ lệ (ước tính) | Ghi chú |
| :--- | :--- | :--- | :--- |
| **Dữ liệu thiếu (Missing)** | 0 | 0% | Toàn bộ các dòng đều được điền đầy đủ[cite: 2]. |
| **Dữ liệu trùng (Duplicates)** | 226 | ~10% | Cần loại bỏ hoặc xem xét lại các bản ghi trùng lặp này[cite: 2]. |
| **Sai định dạng** | 0 | 0% | Dữ liệu tuân thủ đúng định dạng các trường[cite: 2]. |
| **Ngoài miền codebook** | 0 | 0% | 100% dữ liệu nằm trong giới hạn của `CODEBOOK.docx`[cite: 1, 2]. |
| **Trả lời một mức** | 442 | ~20% | Hiện tượng đánh lụi (straight-lining), cần cẩn trọng khi phân tích[cite: 2]. |

## 2. Các vấn đề khác cần xử lý
- **Lỗi cột:** Phát hiện 3 tên cột bị sai chính tả, cần chuẩn hóa lại[cite: 2].
- **Dữ liệu thừa:** Tồn tại `Sheet17` bị thừa trong file dữ liệu gốc, cần được loại bỏ khỏi pipeline[cite: 2].
- **Quyền riêng tư:** Dữ liệu không yêu cầu và không cần thực hiện ẩn danh[cite: 2].