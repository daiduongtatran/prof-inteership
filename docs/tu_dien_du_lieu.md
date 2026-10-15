# Từ điển dữ liệu (Codebook)

Bảng dưới đây giải thích ý nghĩa và quy ước mã hóa của **25 cột** dữ liệu trong file `vnu_that_sach.csv` sau bước làm sạch.

| Cột gốc (Tiếng Anh) | Tên tiếng Việt trên biểu đồ | Giải thích và Quy ước mã hóa |
| :--- | :--- | :--- |
| `STT` | STT | Số thứ tự dòng (1 đến 2.770). Dữ liệu gốc không có mã sinh viên. |
| `Nguon` | Nguồn | `Khao sat that` = phản hồi khảo sát thật; `Mo phong bo sung` = dòng mô phỏng thêm vào. |
| `Year` | Năm học | 1 = Năm nhất; 2 = Năm hai; 3 = Năm ba; 4 = Năm tư; 5 = Đã tốt nghiệp. |
| `Gender` | Giới tính | 1 = Nam; 2 = Nữ. |
| `Policy_Stu` | Diện chính sách | 1 = Có; 2 = Không. |
| `Minority_Stu` | Dân tộc thiểu số | 1 = Có; 2 = Không. |
| `Poor_Stu` | Hộ nghèo | 1 = Có; 2 = Không. |
| `Father_Edu` | Học vấn của Bố | 1 = Tiểu học; 2 = THCS; 3 = THPT; 4 = Cao đẳng; 5 = Đại học/Sau đại học; 6 = Khác. |
| `Mother_Edu` | Học vấn của Mẹ | Như `Father_Edu`. |
| `Father_Occupation` | Nghề nghiệp của Bố | 1 = Cán bộ, viên chức nhà nước; 2 = Tự kinh doanh; 3 = Lao động tự do; 4 = Khác; 5 = Không tiết lộ. |
| `Mother_Occupation` | Nghề nghiệp của Mẹ | Như `Father_Occupation`. |
| `Time_Friends` | TG dành cho bạn bè | 1 = Dưới 1 giờ; 2 = Từ 1 đến dưới 2 giờ; 3 = Từ 2 đến dưới 3 giờ; 4 = Từ 3 đến dưới 4 giờ; 5 = Trên 4 giờ. |
| `Time_SocialMedia` | TG dùng mạng xã hội | Như `Time_Friends`. *(Cột gốc đã được sửa lỗi chính tả từ Time_SocicalMedia).* |
| `Time_Studying` | TG tự học | 1 = Dưới 2 giờ; 2 = Từ 2 đến dưới 4 giờ; 3 = Từ 4 đến dưới 6 giờ; 4 = Từ 6 đến dưới 8 giờ; 5 = Trên 8 giờ. |
| `GPA` | Điểm GPA | 1 = Dưới 2.0 (Dưới 2.0 / Yếu / Kém); 2 = Từ 2.0 đến dưới 2.5 (Trung bình); 3 = Từ 2.5 đến dưới 3.2 (Khá); 4 = Từ 3.2 đến dưới 3.6 (Giỏi); 5 = Từ 3.6 trở lên (Xuất sắc). |
| `Adapt_Learning_Uni`| Mức độ thích nghi ĐH | Quy ước nhóm B: 1 = Hoàn toàn không; 2 = Ít; 3 = Bình thường; 4 = Nhiều; 5 = Rất nhiều. |
| `Study_Methods` | Phương pháp học tập | Như quy ước nhóm B. |
| `SupportOf_Uni` | Sự hỗ trợ từ Trường | Như quy ước nhóm B. |
| `SupportOf_Lec` | Sự hỗ trợ từ Giảng viên | Như quy ước nhóm B. |
| `Facilities_Uni` | Cơ sở vật chất | Như quy ước nhóm B. *(Cột gốc đã được sửa lỗi chính tả từ Facilitie_Uni).* |
| `Quality_Lecturer` | Chất lượng Giảng viên | Như quy ước nhóm B. |
| `TrainingCurriculum`| Chương trình đào tạo | Như quy ước nhóm B. |
| `Competitive_Class` | Sự cạnh tranh trong lớp | Như quy ước nhóm B. |
| `Influence_Friends` | Ảnh hưởng từ bạn bè | Như quy ước nhóm B. *(Cột gốc đã được sửa lỗi chính tả từ InfuenceF_Friends).* |
| `Tra_loi_deu` | Trả lời đều | Cờ (True/False) đánh dấu các dòng chọn đúng một mức ở cả 9 câu nhóm B. |