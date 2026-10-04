# Chỉ Số Thống Kê & Trực Quan Hóa

**Nguồn dữ liệu:** `data/raw/Database_paper.xlsx` (Sheet1, 2.170 dòng thật, 22 cột)  
**Phương án xử lý dòng trùng:** Gắn cờ các bản ghi trùng lặp để phân tích song song hai trường hợp (có và không có các dòng trùng), không xóa cứng vì dữ liệu khuyết mã sinh viên.

---

## 1. Các chỉ số thống kê phân tích

### 1.1. Tần suất và tỉ lệ từng mức GPA
- **Công thức:** 
  - Tần suất ($f_i$): Đếm số lượng sinh viên theo từng mức GPA ($i \in [1, 5]$).
  - Tỉ lệ: $p_i = \frac{f_i}{n} \times 100\%$
- **Cột dùng:** `GPA` (mức 1–5 theo CODEBOOK).
- **Lưu ý:** Dữ liệu GPA không phải biến điểm số liên tục hệ 4 mà là biến thứ bậc được chia thành 5 mức:
  - Mức 1: Kém (< 2.0)
  - Mức 2: Trung bình (2.0 – < 2.5)
  - Mức 3: Khá (2.5 – < 3.2)
  - Mức 4: Giỏi (3.2 – < 3.6)
  - Mức 5: Xuất sắc ($\ge$ 3.6)

### 1.2. Tỉ lệ đạt mức 4–5 (từ 3.2 trở lên)
- **Công thức:** 
  $$p = \frac{\text{Số SV có } GPA \ge 4}{n} \times 100\%$$
- **Cột dùng:** `GPA` (mức 1–5), điều kiện lọc: `GPA >= 4`.
- **Lưu ý:** Chỉ tính gồm hai nhóm **Giỏi** (mức 4) và **Xuất sắc** (mức 5), không gộp nhóm Khá (mức 3). Tỉ lệ này đạt xấp xỉ 36.0% – 36.8% tùy thuộc vào việc xét tập mẫu có hoặc không có dòng trùng.

### 1.3. Mức GPA trung vị
- **Công thức:** 
  $$Median = \text{Mức nằm ở vị trí chính giữa dãy sắp thứ tự } (X_{(n+1)/2})$$
- **Cột dùng:** `GPA` (mức 1–5).
- **Lưu ý:** Trung vị ở đây là **một mức thứ bậc** (chẳng hạn mức 3 - Khá), không phải là một điểm số lẻ hệ 4.

### 1.4. Điểm trung bình các câu Likert (Nhóm B)
- **Công thức:** 
  $$\bar{X} = \frac{\sum x_i}{n}$$
- **Cột dùng:** 9 biến thang đo Likert 1–5: `Adapt_Learning_Uni`, `Study_Methods`, `SupportOf_Uni`, `SupportOf_Lec`, `Facilitie_Uni`, `Quality_Lecturer`, `TrainingCurriculum`, `Competitive_Class`, `InfuenceF_Friends`.
- **Lưu ý:** Cần đánh giá độ nhạy khi tính trên toàn bộ mẫu so với khi loại trừ nhóm 442 sinh viên trả lời một mức (straight-lining).

### 1.5. Tương quan hạng Spearman với GPA
- **Công thức:** 
  $$\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$$
- **Cột dùng:** `GPA` (mức 1–5) với các biến thời gian: `Time_Studying`, `Time_Friends`, `Time_SocicalMedia` (đều là biến thứ bậc 1–5).
- **Lưu ý:** Spearman là kiểm định phi tham số bắt buộc cho kiểu dữ liệu thứ bậc (Ordinal).

### 1.6. So sánh theo các nhóm nhân khẩu học
- **Biến phân nhóm:** Năm học (`Year`), Giới tính (`Gender`), Diện chính sách (`Policy_Stu`), Trình độ bố mẹ (`Father_Edu`, `Mother_Edu`), Thời gian tự học (`Time_Studying`).
- **Biến kiểm tra:** Mức `GPA` và điểm trung bình các tiêu chí Likert.
- **Kiểm định:** 
  - So sánh 2 nhóm (Giới tính, Diện chính sách): Mann-Whitney U.
  - So sánh trên 2 nhóm (Năm học, Trình độ phụ huynh): Kruskal-Wallis H.

---

## 2. Tiêu chí và trạng thái chất lượng dữ liệu

Đánh giá trên tập dữ liệu thật 2.170 dòng:

| Tiêu chí chất lượng | Chỉ số thực tế | Trạng thái | Đánh giá & Chi tiết kỹ thuật |
| :--- | :--- | :--- | :--- |
| **Tính đầy đủ (Completeness)** | **100%** | Tốt | Không có ô trống nào (0 missing values) trên toàn bộ 22 cột. |
| **Tính duy nhất (Uniqueness)** | **89.59%** | Cần theo dõi | 226 dòng trùng hoàn toàn. Xử lý bằng cách gắn cờ để phân tích so sánh, không xóa cứng. |
| **Tính hợp lệ (Validity)** | **100%** | Tốt | Giá trị của mọi biến đều nằm chính xác trong miền giá trị CODEBOOK quy định. |
| **Tính đồng nhất (Consistency)** | **100%** | Tốt | Toàn bộ 22 biến số đều thuộc kiểu số nguyên int64. |

---

## 3. Hệ thống chỉ số thống kê tham chiếu (Trên tập 1.944 dòng không trùng)

Dưới đây là các giá trị thống kê cụ thể khi xét tập dữ liệu đã lọc các bản ghi trùng lặp (n = 1.944):

### 3.1. Đặc điểm đối tượng khảo sát
- **Giới tính:** Nữ chiếm 88.84% (1.727 sv); Nam chiếm 11.16% (217 sv).
- **Khóa học:** Đã tốt nghiệp: 72.02%; Sinh viên năm tư: 21.04% (409 sv); Sinh viên năm ba: 6.94% (135 sv).
- **Đối tượng ưu tiên:** Diện chính sách: 36.57% (711 sv); Dân tộc thiểu số: 6.53% (127 sv); Hộ nghèo: 4.32% (84 sv).

### 3.2. Phân bố Kết quả Học tập (GPA)
- **Điểm GPA trung bình (Mã hóa mức 1–5):** 3.29 / 5.0 (Độ lệch chuẩn Std = 0.77).
- **Cơ cấu xếp loại học lực:**
  - Loại Khá (mức 3 - GPA 2.5 đến < 3.2): 55.50% (1.079 sv).
  - Loại Giỏi (mức 4 - GPA 3.2 đến < 3.6): 31.22% (607 sv).
  - Loại Xuất sắc (mức 5 - GPA $\ge$ 3.6): 4.78% (93 sv).
  - Loại Trung bình (mức 2 - GPA 2.0 đến < 2.5): 5.45% (106 sv).
  - Loại Yếu (mức 1 - GPA < 2.0): 3.03% (59 sv).
- **Tổng tỉ lệ đạt loại Giỏi và Xuất sắc (mức 4–5):** 36.00% (700 sv).

### 3.3. Đánh giá các Yếu tố Ảnh hưởng (Likert 1–5)
- Chất lượng giảng viên (`Quality_Lecturer`): 4.33 / 5.0 (Cao nhất).
- Sự hỗ trợ từ giảng viên (`SupportOf_Lec`): 4.18 / 5.0.
- Chương trình đào tạo (`TrainingCurriculum`): 4.11 / 5.0.
- Cơ sở vật chất nhà trường (`Facilitie_Uni`): 4.07 / 5.0.
- Mức độ hỗ trợ của trường (`SupportOf_Uni`): 3.99 / 5.0.
- Mức độ cạnh tranh trong lớp (`Competitive_Class`): 3.94 / 5.0.
- Ảnh hưởng từ bạn bè (`InfuenceF_Friends`): 3.83 / 5.0.
- Phương pháp học tập cá nhân (`Study_Methods`): 3.62 / 5.0.
- Khả năng thích ứng môi trường ĐH (`Adapt_Learning_Uni`): 3.46 / 5.0 (Thấp nhất).

---

## 4. Danh sách biểu đồ dự kiến (Trực quan hóa)

1. **Biểu đồ tròn (Pie Chart):** Phân bổ cơ cấu tỉ lệ 5 mức GPA (Yếu, Trung bình, Khá, Giỏi, Xuất sắc).
2. **Biểu đồ cột (Bar Chart):** So sánh tỉ lệ đạt GPA mức 4–5 (Giỏi & Xuất sắc) với các mức còn lại.
3. **Biểu đồ thanh chồng 100% (100% Stacked Bar Chart):** Cơ cấu lựa chọn từ mức 1 (Not at all) đến mức 5 (Very) cho 9 câu Likert nhóm B.
4. **Bản đồ nhiệt ma trận tương quan (Spearman Correlation Heatmap):** Mối tương quan hạng giữa GPA và các biến thời gian tự học, mạng xã hội, bạn bè.
5. **Biểu đồ hộp (Boxplot) 1:** Phân bố mức GPA theo Giới tính (Nam vs Nữ).
6. **Biểu đồ hộp (Boxplot) 2:** So sánh mức GPA giữa nhóm sinh viên diện chính sách và sinh viên thông thường.
7. **Biểu đồ cột nhóm (Grouped Bar Chart):** So sánh phân bố xếp loại GPA theo Năm học / Tình trạng khóa học.
8. **Biểu đồ cột chồng (Stacked Bar Chart):** Tỉ lệ các mức GPA theo từng bậc Trình độ học vấn của bố/mẹ.

---

## 5. Tác dụng và ý nghĩa trong dự án Bảng điều khiển (Dashboard)

1. **Hệ thống thẻ chỉ số tổng quan (KPI Cards):** Đặt các chỉ số chính ngay đầu trang dashboard (Tổng số khảo sát, Tỉ lệ sinh viên Giỏi & Xuất sắc, Điểm đánh giá Giảng viên) giúp nắm bắt bức tranh học tập nhanh chóng.
2. **Bộ lọc tương tác đa chiều (Cross-Filtering):** Cho phép người dùng bấm chọn các đối tượng đặc thù (Hộ nghèo, Diện chính sách, Nhóm có cờ dữ liệu trùng) để quan sát sự thay đổi tức thì của phổ điểm GPA.
3. **Phát hiện hiểu biết cốt lõi (Key Insights):** Phản ánh điểm nghẽn lớn nhất của sinh viên nằm ở phương pháp và khả năng tự thích ứng (chỉ đạt 3.46/5), từ đó hỗ trợ nhà trường đưa ra quyết định tổ chức các buổi hội thảo định hướng đầu khóa thay vì chỉ tập trung vào nâng cấp cơ sở vật chất.