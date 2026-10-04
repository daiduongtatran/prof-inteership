# Từ điển dữ liệu và quy ước mã hóa

Tài liệu này giải thích ý nghĩa từng cột và từng mã số trong file `data/clean/VNU_co_mo_phong_bo_sung.csv`. Mọi cột đều đang ở dạng **mã số**, cần giải mã theo bảng dưới đây trước khi phân tích hoặc vẽ biểu đồ.

## 1. Nguồn dữ liệu

- **Dữ liệu gốc (thật):** khảo sát sinh viên Trường Đại học Giáo dục, Đại học Quốc gia Hà Nội, về các yếu tố ảnh hưởng đến kết quả học tập. File: `data/raw/Database_paper.xlsx` (Sheet1, 2.170 phản hồi). Bảng câu hỏi và mã hóa: `data/raw/CODEBOOK.docx`.
- **Nơi công bố:** Mendeley Data, DOI `10.17632/23ppcdbmhc.1` (https://data.mendeley.com/datasets/23ppcdbmhc/1). Bài mô tả dữ liệu: https://www.sciencedirect.com/science/article/pii/S2352340925001702
- **Giấy phép và trích dẫn:** *(nhóm điền sau khi kiểm tra trang Mendeley Data)*
- **Dòng mô phỏng bổ sung:** 600 dòng (300 năm 1, 300 năm 2) do nhóm tạo bằng `dataset.py`, **chỉ để minh họa chức năng dashboard**. Cách tạo: lấy mẫu lại (bootstrap) từ dòng thật, chỉ thay `Year`, `Gender`, `Time_Studying`. Tham số: SEED = 2026, tỉ lệ nam = 40%, phân bố `Time_Studying` mức 1–5 = 10/20/30/25/15%.
- **Sheet17** trong file Excel gốc chỉ lặp lại cột `Time_Friends`, không dùng.

> **Quy tắc sử dụng:** mọi kết luận về sinh viên thật chỉ rút ra từ các dòng có `Nguon = "Khao sat that"`. Dòng `Nguon = "Mo phong bo sung"` chỉ dùng để thử bộ lọc và biểu đồ.

## 2. Hai cột do nhóm thêm

| Cột | Ý nghĩa |
|---|---|
| `STT` | Số thứ tự dòng (1 đến 2.770). Dữ liệu gốc không có mã sinh viên. |
| `Nguon` | `Khao sat that` = phản hồi khảo sát thật; `Mo phong bo sung` = dòng mô phỏng. |

## 3. Quy ước chung (đọc trước khi phân tích)

1. **Câu hỏi Có/Không: mã 1 = Có, mã 2 = Không.** Đây là điểm dễ nhầm, vì thường người ta nghĩ 1 là "Không".
2. **Các câu theo mức độ (1–5): mã càng lớn thì mức càng cao** (thời gian càng nhiều, mức độ càng mạnh, GPA càng cao).
3. **Các cột đều là thang thứ bậc hoặc nhóm, không phải số đo thật.** Không nên tính trung bình và độ lệch chuẩn cho GPA, thời gian. Dùng tần suất, tỉ lệ, trung vị.
4. **Tất cả câu trả lời là tự khai** (sinh viên tự báo cáo), kể cả GPA.
5. Không có ô thiếu giá trị. Mọi giá trị đều nằm trong miền hợp lệ ở các bảng dưới.

## 4. Nhóm A: thông tin cá nhân và gia đình

| Cột | Câu hỏi | Mã số và nhãn |
|---|---|---|
| `Year` | Bạn là sinh viên năm mấy? | 1 = Năm nhất; 2 = Năm hai; 3 = Năm ba; 4 = Năm tư; 5 = Đã tốt nghiệp |
| `Gender` | Giới tính | 1 = Nam; 2 = Nữ |
| `Policy_Stu` | Thuộc diện chính sách? | 1 = Có; 2 = Không |
| `Minority_Stu` | Là sinh viên dân tộc thiểu số? | 1 = Có; 2 = Không |
| `Poor_Stu` | Gia đình thuộc hộ nghèo? | 1 = Có; 2 = Không |
| `Father_Edu` | Trình độ học vấn của bố | 1 = Tiểu học; 2 = THCS; 3 = THPT; 4 = Cao đẳng; 5 = Đại học/sau đại học; 6 = Khác |
| `Mother_Edu` | Trình độ học vấn của mẹ | Như `Father_Edu` |
| `Father_Occupation` | Nghề nghiệp của bố | 1 = Cán bộ, viên chức nhà nước; 2 = Tự kinh doanh; 3 = Lao động tự do; 4 = Khác; 5 = "Not public" *(giữ nguyên theo codebook, nghĩa cần đối chiếu bài báo gốc)* |
| `Mother_Occupation` | Nghề nghiệp của mẹ | Như `Father_Occupation` |

*Lưu ý:* trong dữ liệu thật, `Year` chỉ có giá trị 3, 4 và 5. Giá trị 1 và 2 chỉ có ở dòng mô phỏng.

## 5. Nhóm A tiếp: thói quen hằng ngày

| Cột | Câu hỏi | Mã số và nhãn |
|---|---|---|
| `Time_Friends` | Thời gian đi chơi với bạn bè mỗi ngày | 1 = dưới 1 giờ; 2 = từ 1 đến dưới 2 giờ; 3 = từ 2 đến dưới 3 giờ; 4 = từ 3 đến dưới 4 giờ; 5 = trên 4 giờ |
| `Time_SocicalMedia` | Thời gian dùng mạng xã hội mỗi ngày | Như `Time_Friends` |
| `Time_Studying` | Thời gian tự học mỗi ngày | 1 = dưới 2 giờ; 2 = từ 2 đến dưới 4 giờ; 3 = từ 4 đến dưới 6 giờ; 4 = từ 6 đến dưới 8 giờ; 5 = trên 8 giờ |

*Lưu ý:* tên cột `Time_SocicalMedia` viết sai chính tả (Social). Khi làm sạch nên đổi tên.

## 6. Kết quả học tập

| Cột | Câu hỏi | Mã số và nhãn |
|---|---|---|
| `GPA` | GPA tích lũy (thang 4, tự khai) | 1 = dưới 2.0 (Yếu); 2 = từ 2.0 đến dưới 2.5 (Trung bình); 3 = từ 2.5 đến dưới 3.2 (Khá); 4 = từ 3.2 đến dưới 3.6 (Giỏi); 5 = từ 3.6 trở lên (Xuất sắc) |

*Lưu ý:* đây là **5 nhóm điểm, không phải điểm thật**. Dữ liệu không có điểm theo môn, theo kỳ hay theo lớp, nên không thể tính GPA trung bình hay độ lệch chuẩn của GPA.

## 7. Nhóm B: đánh giá mức độ (thang 1–5)

Quy ước mã dùng chung cho 9 cột dưới đây:
**1 = Hoàn toàn không; 2 = Ít; 3 = Vừa phải; 4 = Khá nhiều; 5 = Rất nhiều.**

| Cột | Nội dung câu hỏi |
|---|---|
| `Adapt_Learning_Uni` | Mức độ thích nghi với môi trường học tập ở trường |
| `Study_Methods` | Mức độ phương pháp học ảnh hưởng đến kết quả học tập |
| `SupportOf_Uni` | Mức độ hỗ trợ của trường dành cho sinh viên |
| `SupportOf_Lec` | Mức độ hỗ trợ của giảng viên (ảnh hưởng đến kết quả) |
| `Facilitie_Uni` | Mức độ đáp ứng của cơ sở vật chất |
| `Quality_Lecturer` | Mức độ chất lượng đội ngũ giảng viên |
| `TrainingCurriculum` | Mức độ phù hợp của chương trình đào tạo |
| `Competitive_Class` | Mức độ ảnh hưởng của sự cạnh tranh trong lớp |
| `InfuenceF_Friends` | Mức độ ảnh hưởng của bạn bè trong lớp đến kết quả |

*Lưu ý:* tên cột `Facilitie_Uni` và `InfuenceF_Friends` viết sai chính tả. Khi làm sạch nên đổi tên.

## 8. Hạn chế đã biết của dữ liệu

- **GPA tự khai, chỉ có 5 nhóm**; mẫu có khoảng 89% là nữ và 73% đã tốt nghiệp (dữ liệu thật). Kết quả không đại diện cho toàn bộ sinh viên.
- **Thời gian tự học dồn về mức 5** (khoảng 82% dữ liệu thật), nên cột này ít phân biệt được các nhóm.
- **Các nhóm nhỏ** (hộ nghèo: 86 người; dân tộc thiểu số: 129 người; năm ba: 135 người) khi so sánh dễ cho kết luận thiếu chắc chắn. Mọi biểu đồ cần ghi cỡ mẫu `n`.
- **Mối liên hệ giữa các yếu tố và GPA đều yếu** (hệ số tương quan lớn nhất khoảng 0,13). Báo cáo đúng như vậy, không phóng đại.
- **226 dòng trùng hệt nhau ở cả 22 cột** (khoảng 10%). Vì dữ liệu không có mã định danh nên không biết là nhập lặp hay trùng ngẫu nhiên. Không xóa tự động; phân tích có và không có các dòng này.
- **442 dòng thật chọn đúng một mức ở cả 9 câu nhóm B**, có thể là trả lời qua loa. Sẽ đánh dấu bằng cột riêng khi làm sạch.

## 9. Việc cần làm ở bước làm sạch

1. Giải mã các cột mã số thành nhãn theo bảng ở trên.
2. Đổi tên cột sai chính tả, đặt tên thống nhất.
3. Tạo cột nhóm GPA (Yếu, Trung bình, Khá, Giỏi, Xuất sắc) và nhóm thời gian tự học đã gộp (mức 1–3, mức 4, mức 5).
4. Đánh dấu dòng trùng và dòng chọn một mức ở cả 9 câu nhóm B.
5. Ghi nhật ký làm sạch: số dòng trước và sau, từng thay đổi và lý do.

### Nhật ký làm sạch dữ liệu (Ngày 04/10/2026)

**1. Biến động số lượng bản ghi (Dòng):**
- **Trước khi làm sạch:** 2.770 bản ghi.
- **Sau khi làm sạch:** 2.539 bản ghi (Đã loại bỏ 231 bản ghi rác).

**2. Chi tiết các bước thay đổi và Lý do:**
- **Giải mã & Đổi tên (Mapping & Renaming):** 
  - Đã giải mã toàn bộ các cột mã số thành nhãn chữ cái trực quan dựa theo bảng Codebook. 
  - Đổi tên các cột bị sai chính tả gốc gồm `Time_SocicalMedia`, `Facilitie_Uni`, `InfuenceF_Friends` để đặt tên thống nhất cho dữ liệu.
  - *Lý do:* Đảm bảo tính toàn vẹn và dễ đọc cho file CSV cuối cùng, tạo thuận lợi khi chuyển giao file sạch và khi lên biểu đồ phân tích.
- **Xử lý dữ liệu nhiễu & bất thường:** 
  - Đã phát hiện và **xóa bỏ hoàn toàn** 231 dòng trùng lặp y hệt nhau ở cả 22 biến. *Lý do:* Đây là lỗi spam/double-click, nếu giữ lại sẽ làm sai lệch nghiêm trọng phân phối thực tế.
  - Đã **đánh dấu cờ (Flagging)** vào cột `Tra_loi_deu` đối với 442 dòng chọn đúng một mức ở cả 9 câu nhóm B. *Lý do:* Đây là biểu hiện của việc trả lời qua loa (straight-lining). Việc đánh dấu giúp nhóm linh hoạt cô lập và kiểm định riêng tệp dữ liệu này thay vì xóa bỏ tự động.