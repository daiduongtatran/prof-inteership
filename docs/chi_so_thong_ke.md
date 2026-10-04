# Chỉ Số Thống Kê & Trực Quan Hóa

**Dữ liệu sử dụng:** `data/clean/VNU_co_mo_phong_bo_sung.csv`[cite: 1]
**Cỡ mẫu tổng:** $n$ (Sẽ tính toán chính xác sau khi loại bỏ 226 dòng trùng và cân nhắc 442 dòng trả lời một mức)[cite: 2].

## 1. Các chỉ số thống kê phân tích

### 1.1. Tần suất và tỉ lệ từng mức GPA[cite: 2]
- **Công thức:** 
  - Tần suất ($f_i$): Số lượng sinh viên đạt mức GPA thứ $i$.
  - Tỉ lệ: $p_i = \frac{f_i}{n} \times 100\%$
- **Cột dùng:** Cột lưu giá trị phân loại GPA.
- **Lưu ý:** Cần chia GPA theo đúng các thang bậc quy định trong `CODEBOOK.docx`[cite: 1].

### 1.2. Tỉ lệ đạt mức 4–5 (từ 3.2 trở lên)[cite: 2]
- **Công thức:** $p = \frac{\text{Số SV có GPA } \ge 3.2}{n} \times 100\%$
- **Cột dùng:** Điểm GPA hệ 4.
- **Lưu ý:** Gộp nhóm sinh viên Khá - Giỏi - Xuất sắc để tính chung tỉ lệ này.

### 1.3. Mức GPA trung vị[cite: 2]
- **Công thức:** $Median = X_{(n+1)/2}$ (khi dữ liệu GPA được sắp xếp tăng dần).
- **Cột dùng:** Điểm GPA.
- **Lưu ý:** Phù hợp để đánh giá mặt bằng chung do trung vị ít bị ảnh hưởng bởi các điểm dị biệt (outliers).

### 1.4. Điểm trung bình các câu Likert[cite: 2]
- **Công thức:** $\bar{X} = \frac{\sum x_i}{n}$
- **Cột dùng:** Các cột câu hỏi đo lường bằng thang Likert (1-5).
- **Lưu ý:** Bóc tách các câu hỏi bị ảnh hưởng bởi hiện tượng "trả lời một mức" (442 mẫu)[cite: 2] để tránh làm lệch kết quả trung bình.

### 1.5. Tương quan hạng Spearman với GPA[cite: 2]
- **Công thức:** $\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$
- **Cột dùng:** Cột GPA và các cột biến định lượng/thứ bậc khác (ví dụ: thời gian tự học).
- **Lưu ý:** Sử dụng kiểm định Spearman vì GPA và thang đo Likert mang tính thứ bậc phân phối không chuẩn.

### 1.6. So sánh các nhóm[cite: 2]
- **Cột nhóm:** Năm học, Giới tính, Diện chính sách, Trình độ bố mẹ, Thời gian tự học[cite: 2].
- **Cột biến phụ thuộc:** GPA.
- **Công thức/Kiểm định:** 
  - 2 nhóm (Giới tính, Diện chính sách): Kiểm định Mann-Whitney U.
  - >2 nhóm (Năm học, Trình độ bố mẹ): Kiểm định Kruskal-Wallis H.

---

## 2. Danh sách 6–8 biểu đồ dự kiến (Trực quan hóa)[cite: 2]

1. **Biểu đồ tròn (Pie Chart):** Thể hiện *Tần suất và tỉ lệ từng mức GPA*[cite: 2].
2. **Biểu đồ cột (Bar Chart):** So sánh *Tỉ lệ đạt mức GPA 4–5 (từ 3.2)* với phần còn lại[cite: 2].
3. **Biểu đồ radar (Radar Chart):** Trực quan hóa *Điểm trung bình các câu Likert* để xem khía cạnh nào được đánh giá cao nhất[cite: 2].
4. **Biểu đồ phân tán (Scatter Plot):** Thể hiện mối *Tương quan hạng Spearman* giữa thời gian tự học và GPA thực tế[cite: 2].
5. **Biểu đồ hộp (Boxplot) 1:** So sánh phân phối điểm GPA theo *Giới tính* và *Năm học*[cite: 2].
6. **Biểu đồ hộp (Boxplot) 2:** Đánh giá độ phân tán và mức GPA trung vị giữa nhóm có và không thuộc *Diện chính sách*[cite: 2].
7. **Biểu đồ cột chồng (Stacked Bar Chart):** So sánh cấu trúc mức độ GPA theo *Trình độ học vấn của bố mẹ*[cite: 2].