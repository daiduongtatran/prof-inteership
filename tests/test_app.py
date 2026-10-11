"""
Kiểm thử tự động cho dashboard/app.py bằng streamlit.testing.v1.AppTest.
Chạy kiểm thử:  pytest
"""
from pathlib import Path
from streamlit.testing.v1 import AppTest

APP_PATH = str(Path(__file__).resolve().parents[1] / "dashboard" / "app.py")


def test_khoi_dong_mac_dinh():
    """Chạy app với bộ lọc mặc định, kiểm tra không có exception."""
    at = AppTest.from_file(APP_PATH, default_timeout=30).run()
    assert not at.exception


def test_moi_lua_chon_nhom_so_sanh_va_goi_y():
    """Chạy qua mọi lựa chọn nhóm so sánh (Tab 2) và yếu tố gợi ý (Tab 5)."""
    at = AppTest.from_file(APP_PATH, default_timeout=30).run()
    assert not at.exception

    # Duyệt qua tất cả các selectbox trên trang (gồm nhóm so sánh và yếu tố gợi ý)
    for sb in at.selectbox:
        for opt in sb.options:
            sb.select(opt).run()
            assert not at.exception


def test_bat_mo_phong_bo_sung_va_co_tra_loi_mot_muc():
    """Bật nguồn 'Mô phỏng bổ sung' và bật checkbox loại dòng trả lời một mức."""
    at = AppTest.from_file(APP_PATH, default_timeout=30).run()
    assert not at.exception

    # Bật cả Khảo sát thật + Mô phỏng bổ sung ở multiselect đầu tiên (Nguồn dữ liệu)
    ms_nguon = at.sidebar.multiselect[0]
    ms_nguon.set_value(list(ms_nguon.options)).run()
    assert not at.exception

    # Bật cờ loại dòng trả lời một mức
    at.sidebar.checkbox[0].check().run()
    assert not at.exception


def test_loc_rong_khong_loi():
    """Khi người dùng bỏ chọn hết khiến bộ lọc rỗng, app cảnh báo và không văng exception."""
    at = AppTest.from_file(APP_PATH, default_timeout=30).run()
    assert not at.exception

    # Bỏ chọn toàn bộ Năm học để tạo bộ lọc rỗng
    at.sidebar.multiselect[1].set_value([]).run()
    assert not at.exception
    assert len(at.warning) > 0