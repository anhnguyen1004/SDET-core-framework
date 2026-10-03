# Python SDET Core Framework

Automation testing framework được thiết kế chuyên biệt cho hệ thống Backend/Microservices, tích hợp kiểm thử API, Database và UI.

## 🛠 Tech Stack
* **Ngôn ngữ:** Python 3.1x
* **Core Framework:** Pytest
* **API Automation:** `requests`
* **Database Automation:** `psycopg2` (PostgreSQL)
* **UI Automation:** Playwright
* **Configuration:** `python-dotenv`
* **Reporting:** Allure Report
* **Infrastructure:** Docker

## 📁 Cấu trúc thư mục
```text
sdet-core-framework/
├── config/          # Quản lý biến môi trường và settings trung tâm
├── data/            # Chứa file test data mầm (JSON, CSV)
├── models/          # Data Models (dataclasses) và các Client (DB, Kafka, API)
├── tests/           # Kịch bản kiểm thử (chia theo api, ui, backend)
├── .env.example     # Template định dạng các biến môi trường cần thiết
├── conftest.py      # Chứa các Pytest fixtures (setup/teardown, DB connections)
├── pytest.ini       # Cấu hình Pytest (markers, log cli)
└── requirements.txt # Danh sách thư viện phụ thuộc
