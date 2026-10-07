from dataclasses import dataclass

@dataclass
class Report:
    id: int
    nguoi_bao_cao_id: int
    tin_dang_id: int
    ly_do: str
    mo_ta: str
    trang_thai: str
    nguoi_xu_ly_id: int
    ngay_bao_cao: str
    ngay_xu_ly: str
    ghi_chu_xu_ly: str