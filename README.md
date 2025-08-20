# 🚀 DNSE Local API Server

Hiện tại **DNSE/Entrade** có cung cấp dịch vụ API cho toàn bộ khách hàng có tài khoản chứng khoán.  
Khách hàng có thể lấy dữ liệu giá chứng khoán (**Market Data**) từ DNSE và đặt lệnh giao dịch chứng khoán qua cổng **API (Trading API)** do DNSE cung cấp.  

👉 Hướng dẫn đăng ký: [Hướng dẫn đăng ký API Lightspeed](https://hdsd2.entrade.com.vn/api-lightspeed/i.-huong-dan-dang-ky)

---

## 🌟 Giới thiệu

Dự án này cung cấp **một server chạy cục bộ (local server)** trên máy người dùng, giúp đơn giản hóa việc gọi API tới DNSE/Entrade.  
Thay vì phải thao tác trực tiếp với API (vốn có thể phức tạp), bạn chỉ cần gọi API qua server cục bộ này để:  

- 🛒 Đặt lệnh mua/bán thông qua API đơn giản hơn  
- ⚡ Giảm thiểu độ phức tạp trong quá trình phát triển  

---

## ⚙️ Cài đặt

Clone repo và cài đặt các dependencies:

```bash
git clone https://github.com/ChungkhoanPhaisinh/PyTrade.git
cd PyTrade
pip install -r requirements.txt
```

Thêm thông tin đăng nhập và App Password vào file .env.
👉 Hướng dẫn tạo App Password: [Hướng dẫn tạo App Password](https://support.google.com/accounts/answer/185833?hl=vi)

## ▶️ Chạy server

Khởi động server cục bộ:

```bash
python server.py
```

Mặc định server sẽ chạy tại:
👉 http://127.0.0.1:8000

Nếu bạn thấy log đăng nhập thành công trên console thì server đã hoạt động.

---

## 📚 Example Usage

🛠️ API Hỗ trợ

Server local bao gồm API cho việc đặt lệnh cơ sở/phái sinh cho cả DNSE và Entrade.

🔑 Tham số chung của lệnh

symbol: mã chứng khoán

account: investorId

side: NB (BUY) hoặc NS (SELL) – mặc định là NB

price: giá đặt

loan: mã gói vay – mặc định đã cài đặt, chỉ cần thêm nếu gặp lỗi

volume: khối lượng đặt – mặc định là 1

type: kiểu lệnh (LO / MTL / ATO / ATC / MOK / MAK) – mặc định là LO

platform: Entrade hoặc DNSE – mặc định là Entrade

demo: chỉ dùng nếu platform = Entrade – mặc định dùng tài khoản thật

---
🔑 Tham số lệnh điều kiện

sub_acc: investorAccountId

condition: >= hoặc <= – mặc định là <=

stop: giá điều kiện

---
🔑 Tham số hủy lệnh điều kiện

id: order_id của lệnh muốn hủy – mặc định hủy hết nếu không truyền vào

---
🌟 Các mẫu API

- Đặt lệnh SHORT tại giá 1820 tại tài khoản Entrade thật

http://localhost:8000/trade?symbol=41I1F8000&account=1000064040&side=NS&price=1820

- Đặt lệnh điều kiện LONG tại giá 1775 khi giá xuống dưới 1780 cho tài khoản DNSE

http://localhost:8000/conditional_order?symbol=41I1F8000&account=1000064040&sub_acc=1000070905&price=1775&stop=1780

- Đặt lệnh mua DSE tại giá 30000 khi giá đạt 30000

http://localhost:8000/conditional_order?symbol=DSE&account=1000064040&sub_acc=1000070905&price=30000&condition=>=&stop=30000

- Hủy lệnh điều kiện (hiện chỉ áp dụng cho Entrade)

http://localhost:7979/cancel_conditional_order?account=1000064040&sub_acc=1000070905&id=12121

- Hủy tất cả lệnh điều kiện (hiện chỉ áp dụng cho Entrade)

http://localhost:7979/cancel_conditional_order?account=1000064040&sub_acc=1000070905
