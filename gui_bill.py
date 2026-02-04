import customtkinter as ctk
import requests
from datetime import datetime
from tkinter import messagebox

# === 設定外觀主題 ===
ctk.set_appearance_mode("System")  # 跟隨系統 (深色/淺色)
ctk.set_default_color_theme("blue")  # 主題顏色

class CurrencyConverterApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. 視窗基礎設定
        self.title("極簡匯率換算 (Live Rates)")
        self.geometry("400x550")
        self.resizable(False, False)

        # 定義常用的貨幣列表
        self.currencies = ["TWD", "USD", "JPY", "EUR", "KRW", "CNY", "GBP", "AUD", "HKD", "SGD"]
        self.rates = {} 
        
        # 2. 介面佈局 (UI Layout)
        self.create_widgets()
        
        # 3. 程式啟動時，自動上網抓匯率
        self.fetch_rates()

    def create_widgets(self):
        # --- 標題區 ---
        self.label_title = ctk.CTkLabel(self, text="Currency Converter", font=("Roboto Medium", 24))
        self.label_title.pack(pady=(30, 20))

        # --- 金額輸入區 ---
        self.entry_amount = ctk.CTkEntry(self, placeholder_text="請輸入金額", 
                                         width=200, height=40, font=("Arial", 16), justify="center")
        self.entry_amount.pack(pady=10)

        # --- 貨幣選擇區 (使用 Frame 包起來比較整齊) ---
        self.frame_selection = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_selection.pack(pady=20)

        # 左邊：持有貨幣
        self.combo_from = ctk.CTkOptionMenu(self.frame_selection, values=self.currencies, width=100)
        self.combo_from.set("USD") # 預設
        self.combo_from.grid(row=0, column=0, padx=10)

        # 中間：交換按鈕 (Swap)
        self.btn_swap = ctk.CTkButton(self.frame_selection, text="⇄", width=40, 
                                      fg_color="gray", hover_color="#555", command=self.swap_currencies)
        self.btn_swap.grid(row=0, column=1, padx=5)

        # 右邊：目標貨幣
        self.combo_to = ctk.CTkOptionMenu(self.frame_selection, values=self.currencies, width=100)
        self.combo_to.set("TWD") # 預設
        self.combo_to.grid(row=0, column=2, padx=10)

        # --- 轉換按鈕 ---
        self.btn_convert = ctk.CTkButton(self, text="立即換算", width=200, height=50, 
                                         font=("Arial", 18, "bold"), corner_radius=30,
                                         command=self.convert_currency)
        self.btn_convert.pack(pady=20)

        # --- 結果顯示區 (卡片式設計) ---
        self.frame_result = ctk.CTkFrame(self, width=300, height=100, corner_radius=15)
        self.frame_result.pack(pady=10, padx=20, fill="x")

        self.label_result_text = ctk.CTkLabel(self.frame_result, text="0.00", font=("Arial", 36, "bold"), text_color="#2CC985")
        self.label_result_text.pack(pady=(15, 0))

        self.label_rate_info = ctk.CTkLabel(self.frame_result, text="1 USD = ? TWD", font=("Arial", 12), text_color="gray")
        self.label_rate_info.pack(pady=(0, 15))

        # --- 底部狀態列 ---
        self.label_status = ctk.CTkLabel(self, text="正在更新匯率...", font=("Arial", 10), text_color="gray")
        self.label_status.pack(side="bottom", pady=10)

    def fetch_rates(self):
        """ 從網路 API 抓取即時匯率 """
        try:
            # 使用免費公開的 API (以 USD 為基準)
            url = "https://api.exchangerate-api.com/v4/latest/USD"
            response = requests.get(url)
            data = response.json()
            
            self.rates = data["rates"]
            self.last_update = datetime.now().strftime("%Y-%m-%d %H:%M")
            
            self.label_status.configure(text=f"匯率最後更新：{self.last_update}", text_color="#666")
            # 更新一下當前的顯示匯率
            self.update_rate_display()
            
        except Exception as e:
            self.label_status.configure(text="網路連線失敗，無法更新匯率", text_color="red")
            messagebox.showerror("錯誤", "無法連線至匯率伺服器！")

    def convert_currency(self):
        """ 計算匯率 """
        try:
            amount_str = self.entry_amount.get()
            if not amount_str:
                return
            
            amount = float(amount_str)
            from_curr = self.combo_from.get()
            to_curr = self.combo_to.get()

            # 匯率換算邏輯 (因為 API 是以 USD 為基準)
            # 公式： (金額 / 原幣匯率) * 目標幣匯率
            if from_curr in self.rates and to_curr in self.rates:
                rate_from = self.rates[from_curr]
                rate_to = self.rates[to_curr]
                
                result = (amount / rate_from) * rate_to
                
                # 顯示結果 (加上貨幣符號)
                self.label_result_text.configure(text=f"{result:,.2f}")
                self.update_rate_display()
            else:
                self.label_result_text.configure(text="Error")

        except ValueError:
            messagebox.showwarning("輸入錯誤", "請輸入正確的數字！")

    def update_rate_display(self):
        """ 顯示 1 A = ? B 的參考匯率 """
        from_curr = self.combo_from.get()
        to_curr = self.combo_to.get()
        
        if from_curr in self.rates and to_curr in self.rates:
            rate = (1 / self.rates[from_curr]) * self.rates[to_curr]
            self.label_rate_info.configure(text=f"1 {from_curr} ≈ {rate:.4f} {to_curr}")

    def swap_currencies(self):
        """ 交換兩個貨幣的選擇 """
        current_from = self.combo_from.get()
        current_to = self.combo_to.get()
        
        self.combo_from.set(current_to)
        self.combo_to.set(current_from)
        
        # 交換後自動重新計算
        self.convert_currency()

if __name__ == "__main__":
    app = CurrencyConverterApp()
    app.mainloop()