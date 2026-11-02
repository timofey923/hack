import customtkinter as ctk
import requests
import whereismyip
import threading

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

# ЗАМЕНИТЕ на ваш URL после деплоя на Render
SERVER_URL = "https://your-app-name.onrender.com"

class SwillApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("SWILL // Hacker Tool")
        self.geometry("650x550")
        
        # Заголовок
        self.label_title = ctk.CTkLabel(
            self, text="[ SWILL ]", 
            font=("Courier New", 36, "bold"),
            text_color="#00FF41"
        )
        self.label_title.pack(pady=15)
        
        # Вкладки
        self.tabview = ctk.CTkTabview(self, width=600, height=450)
        self.tabview.pack(pady=5, padx=20, fill="both", expand=True)
        
        self.tab_ip = self.tabview.add("IP Lookup")
        self.tab_gen = self.tabview.add("Link Generator")
        self.tab_logs = self.tabview.add("Server Logs")
        
        self.setup_ip_tab()
        self.setup_gen_tab()
        self.setup_logs_tab()
    
    def setup_ip_tab(self):
        ctk.CTkLabel(self.tab_ip, text="Target IP:", font=("Courier", 14)).pack(pady=5)
        self.ip_entry = ctk.CTkEntry(self.tab_ip, width=250, placeholder_text="8.8.8.8")
        self.ip_entry.pack(pady=5)
        ctk.CTkButton(
            self.tab_ip, text="ANALYZE", command=self.lookup_ip,
            fg_color="#003300", hover_color="#005500", font=("Courier", 13, "bold")
        ).pack(pady=10)
        self.ip_result = ctk.CTkTextbox(self.tab_ip, width=550, height=250, font=("Courier", 12))
        self.ip_result.pack(pady=10, padx=20, fill="both", expand=True)
    
    def lookup_ip(self):
        ip = self.ip_entry.get().strip()
        if not ip:
            self.ip_result.delete("1.0", "end")
            self.ip_result.insert("1.0", "[-] Enter an IP.")
            return
        self.ip_result.delete("1.0", "end")
        self.ip_result.insert("1.0", "[*] Scanning...")
        threading.Thread(target=self._do_lookup, args=(ip,), daemon=True).start()
    
    def _do_lookup(self, ip):
        try:
            data = whereismyip.whereismyip_dict(ip)
            text = f"""[+] IP: {data.get('ip')}
[+] Country: {data.get('country')}
[+] City: {data.get('city')}
[+] Region: {data.get('region')}
[+] ISP: {data.get('isp', 'N/A')}

[!] This is approximate. Not a person."""
        except Exception as e:
            text = f"[-] Error: {e}"
        self.ip_result.delete("1.0", "end")
        self.ip_result.insert("1.0", text)
    
    def setup_gen_tab(self):
        ctk.CTkLabel(self.tab_gen, text="Target URL (where victim lands):", font=("Courier", 14)).pack(pady=5)
        self.url_entry = ctk.CTkEntry(self.tab_gen, width=450, placeholder_text="https://pappinpub.ru")
        self.url_entry.pack(pady=5)
        ctk.CTkButton(
            self.tab_gen, text="GENERATE LINK", command=self.generate_link,
            fg_color="#003300", hover_color="#005500", font=("Courier", 13, "bold")
        ).pack(pady=10)
        self.link_result = ctk.CTkTextbox(self.tab_gen, width=550, height=200, font=("Courier", 12))
        self.link_result.pack(pady=10, padx=20, fill="both", expand=True)
    
    def generate_link(self):
        target = self.url_entry.get().strip() or "https://pappinpub.ru"
        # Ссылка ведёт на ваш сервер, который логирует и редиректит
        link = f"{SERVER_URL}/track?to={target}"
        self.link_result.delete("1.0", "end")
        self.link_result.insert("1.0", f"[+] Tracking link:\n\n{link}\n\n[!] Send this. Server logs will show IP.")
    
    def setup_logs_tab(self):
        ctk.CTkLabel(self.tab_logs, text="Server Logs", font=("Courier", 14)).pack(pady=5)
        ctk.CTkButton(
            self.tab_logs, text="REFRESH LOGS", command=self.fetch_logs,
            fg_color="#003300", hover_color="#005500", font=("Courier", 13, "bold")
        ).pack(pady=10)
        self.logs_text = ctk.CTkTextbox(self.tab_logs, width=550, height=300, font=("Courier", 11))
        self.logs_text.pack(pady=10, padx=20, fill="both", expand=True)
    
    def fetch_logs(self):
        try:
            r = requests.get(f"{SERVER_URL}/logs", timeout=10)
            data = r.json()
            visits = data.get('visits', [])
            if not visits:
                text = "[*] No visits yet."
            else:
                text = "\n".join([
                    f"[{v['time']}] IP: {v['ip']} | {v['city']}, {v['country']}"
                    for v in visits
                ])
        except Exception as e:
            text = f"[-] Error: {e}\n(Is the server running?)"
        self.logs_text.delete("1.0", "end")
        self.logs_text.insert("1.0", text)

if __name__ == "__main__":
    app = SwillApp()
    app.mainloop()