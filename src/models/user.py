from dataclasses import dataclass

@dataclass
class User: 
    id: int
    ho_ten: str
    email: str
    so_dien_thoai: str
    mat_khau: str
    vai_tro: str
    trang_thai: str | None = "HOAT_DONG"