from requests import get, post, delete
from time import localtime

class EntradeClient:
    def __init__(self):
        self.token = None
        self.trading_token = None
        # https://services-staging.entrade.com.vn/papertrade-entrade-api/derivative/orders
        self.base_url = f"https://services.entrade.com.vn/"

    def Authenticate(self, username, password):
        url = f"{self.base_url}entrade-api/v2/auth"

        _headers = {
            "Content-Type": "application/json"
        }
        _json = {
            "username": username,
            "password": password
        }
        response = post(url, headers=_headers, json=_json)
        response.raise_for_status()
        self.token = response.json().get("token")
        print("Đăng nhập thành công! (Entrade)")

    def GetOTP(self):
        url = f"{self.base_url}entrade-api/email-otp"

        _headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        response = get(url, headers=_headers)
        response.raise_for_status()
        print("Gửi OTP thành công! (Entrade)")

    def GetTradingToken(self, otp):
        url = f"{self.base_url}entrade-api/otp/trading-token"

        _headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}",
            "otp": otp
        }
        response = get(url, headers=_headers)
        response.raise_for_status()
        self.trading_token = response.json().get("tradingToken")
        print("Lấy Trading Token thành công! (Entrade)")

    def DatLenh(self, symbol, account, side, price, loan, volume, order_type, demo : bool):
        _headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        _json = {
            "symbol": symbol,
            "side": side,
            "orderType": order_type,
            "price": price,
            "quantity": volume,
            "bankMarginPortfolioId": loan or (32 if demo else 37),
            "investorId": account
        }

        url = "https://services.entrade.com.vn/papertrade-entrade-api/derivative/orders"
        if not demo:
            url = f"{self.base_url}entrade-api/derivative/orders"
            _headers["trading-token"] = self.trading_token

        response = post(url, headers=_headers, json=_json)
        response.raise_for_status()
        print("Gửi yêu cầu đặt lệnh thành công! (Entrade)")
        return response.json()

    def DatLenhDieuKien(self, symbol, account : int, sub_account_id : int, side, price : float, loan, volume, condition, demo : bool):
        _headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }

        current_time = localtime()
        _json = {
            "bankMarginPortfolioId": loan or (32 if demo else 37),
            "condition": condition,
            "expiredTime": f"{current_time.tm_year}-{current_time.tm_mon:02d}-{current_time.tm_mday:02d}T07:30:00.000Z",
            "investorAccountId": sub_account_id,
            "investorId": account,
            "symbol": symbol,
            "targetPrice": price,
            "targetQuantity": volume,
            "targetSide": side,
            "type": "STOP"
        }

        url = "https://services.entrade.com.vn/papertrade-smart-order/orders"
        if not demo: # Whether to make a real or demo order
            url = f"{self.base_url}smart-order/orders"
            _headers["trading-token"] = self.trading_token

        response = post(url, headers=_headers, json=_json)
        response.raise_for_status()
        print("Gửi yêu cầu đặt lệnh điều kiện thành công! (Entrade)")
        return response.json()

    def HuyLenhDieuKien(self, account, sub_account_id, order_id, delete_all : bool, demo : bool):
        _headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}"
        }
        _params = {}

        # Default to only delete 1 order
        url = f"https://services.entrade.com.vn/papertrade-smart-order/orders/{order_id}"
        if not delete_all:
            if not demo:
                url = f"{self.base_url}smart-order/orders/{order_id}"
                _headers["trading-token"] = self.trading_token

        else: # Overwrite by delete all order if user chose to
            _params = {
                "investorId": account,
                "investorAccountId": sub_account_id
            }

            url = "https://services.entrade.com.vn/papertrade-smart-order/orders"
            if not demo:
                url = f"{self.base_url}smart-order/orders"
                _headers["trading-token"] = self.trading_token

        # Make request after processing all data
        response = delete(url, headers=_headers, params=_params)
        response.raise_for_status()
        return response.json()