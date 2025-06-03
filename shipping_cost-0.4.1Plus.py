import tkinter as tk
from tkinter import ttk, messagebox
import requests
from bs4 import BeautifulSoup
import time
import math
from collections import Counter

# ---------------------------- 原代码核心函数 ----------------------------
def get_quantity_of_goods(sell_id, gw, cbm, FCL20, FCL40, FCL40h, cold, FCL20_quantity, FCL40_quantity, FCL40h_quantity):
    # （此处完整保留原get_quantity_of_goods函数实现）
    FCL20G = FCL20_quantity * 25
    FCL20C = FCL20_quantity * 33
    FCL40G = FCL40_quantity * 29
    FCL40C = FCL40_quantity * 67
    FCL40hG = FCL40h_quantity * 29
    FCL40hC = FCL40h_quantity * 76

    g = gw / 1000 / sell_id
    c = cbm / sell_id

    FCL20_quantity1 = min(int(FCL20G / g),int(FCL20C / c))
    FCL40_quantity1 = min(int(FCL40G / g),int(FCL40C / c))
    FCL40h_quantity1 = min(int(FCL40hG / g),int(FCL40hC / c))
   
    keys = [FCL20_quantity1,FCL40_quantity1,FCL40h_quantity1]
    values = [FCL20,FCL40,FCL40h]

    for i in keys:
        for j in values:
            if i == max(keys) and j == min(values):
                Best = i
                break
    
    FCL = {FCL20_quantity1:['FCL20',FCL20_quantity1],FCL40_quantity1:['FCL40',FCL40_quantity1],FCL40h_quantity1:['FCL40h',FCL40h_quantity1]}
    FCL_c = {FCL20_quantity1:['FCL20_c',FCL20_quantity1],FCL40_quantity1:['FCL40_c',FCL40_quantity1],FCL40h_quantity1:['FCL40h_c',FCL40h_quantity1]}

    return FCL_c[Best] if cold == "是" else FCL[Best]

def get_quantity_of_FCL_2(order_num, sell_id, gw, cbm):
    # （此处完整保留原get_quantity_of_FCL_2函数实现）
    package_id = order_num / sell_id
    total_gw = package_id * gw / 1000
    total_cbm = package_id * cbm
    
    FCL20G = total_gw / 25
    FCL20C = total_cbm / 33
    FCL40G = total_gw / 29
    FCL40C = total_cbm / 67
    FCL40hG = total_gw / 29
    FCL40hC = total_cbm / 76

    return [
        math.ceil(max(FCL20G,FCL20C)),
        math.ceil(max(FCL40G,FCL40C)),
        math.ceil(max(FCL40hG,FCL40hC))
    ]

def get_quantity_of_FCL(order_num, sell_id, gw, cbm, cold, FCL20, FCL40, FCL40h, FCL20_c, FCL40_c, FCL40h_c):
    # （此处完整保留原get_quantity_of_FCL函数实现）
    package_id = order_num / sell_id
    total_gw = package_id * gw / 1000
    total_cbm = package_id * cbm
    
    FCL20G = total_gw / 25
    FCL20C = total_cbm / 33
    FCL40G = total_gw / 29
    FCL40C = total_cbm / 67
    FCL40hG = total_gw / 29
    FCL40hC = total_cbm / 76

    FCL20_quantity = math.ceil(max(FCL20G,FCL20C))
    FCL40_quantity = math.ceil(max(FCL40G,FCL40C))
    FCL40h_quantity = math.ceil(max(FCL40hG,FCL40hC))

    FCL = {FCL20_quantity*FCL20:['FCL20',FCL20_quantity],FCL40_quantity*FCL40:['FCL40',FCL40_quantity],FCL40h_quantity*FCL40h:['FCL40h',FCL40h_quantity]}
    FCL_c = {FCL20_quantity*FCL20_c:['FCL20_c',FCL20_quantity],FCL40_quantity*FCL40_c:['FCL40_c',FCL40_quantity],FCL40h_quantity*FCL40h_c:['FCL40h_c',FCL40h_quantity]}

    if cold == "否":

        result = min(FCL20_quantity*FCL20,FCL40_quantity*FCL40,FCL40h_quantity*FCL40h)
        return FCL[result]
    else:

        result = min(FCL20_quantity*FCL20_c,FCL40_quantity*FCL40_c,FCL40h_quantity*FCL40h_c)
        return FCL_c[result]

def get_FCL_price(FromTo):
    urlHome = 'http://172.16.11.127:5007/institutions/company/11/S0116/4_changyong/changyong2.html'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
    res = requests.get(urlHome,headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'lxml')

    tableUrl = soup.find('table').find('iframe',id = 'center')['src']
    tableUrl = 'http://172.16.11.127:5007/institutions/company/' + tableUrl.replace('../','')

    tableRes = requests.get(tableUrl,headers=headers)
    html = tableRes.text
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find('table')

    count = 1

    countryvalue = {'South Africa': 9, 'Germany': 3, 'UK': 4, 'Australia': 6, 'Japan': 1, 'America': 7, 'Brazil': 5, 'Cuba': 8, 'China': 0, 'Russia': 2}



    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 7 and cells[0].text.strip() != '航线':
            fromTo = cells[0].text.strip()
            if fromTo != FromTo:
                continue
            destination = cells[2].text.strip()
            for i in countryvalue:
                if destination in countryvalue.keys():
        
                    countrycode = countryvalue[destination]

            url = f"http://172.16.11.127:5007/institutions/company/14/vehiclelinedetail.aspx?id1={fromTo}&id2=S011{countrycode}"

            response = requests.get(url,headers=headers)

            html = response.text
            soup = BeautifulSoup(html, 'lxml')

            table = soup.find('table')

            for row in table.find_all('tr'):
                cells = row.find_all('td')
            
                if len(cells) == 6 and cells[0].text.strip() != '运费' and count % 2 != 0:
                    for i in range(1,4):
                        FCL20 = cells[1].text.strip()
                        time.sleep(1)
                        FCL40 = cells[2].text.strip()
                        time.sleep(1)
                        FCL40h = cells[3].text.strip()
                        time.sleep(1)
                        count += 1
                        break
                elif len(cells) == 6 and cells[0].text.strip() != '运费' and count % 2 == 0:
                    count += 1
                    continue

    return FCL20,FCL40,FCL40h

def get_LCL_price(FromTo):
    urlHome = 'http://172.16.11.127:5007/institutions/company/11/S0116/4_changyong/changyong2.html'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
    res = requests.get(urlHome,headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'lxml')

    tableUrl = soup.find('table').find('iframe',id = 'center')['src']
    tableUrl = 'http://172.16.11.127:5007/institutions/company/' + tableUrl.replace('../','')

    tableRes = requests.get(tableUrl,headers=headers)
    html = tableRes.text
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find('table')

    count = 1

    countryvalue = {'South Africa': 9, 'Germany': 3, 'UK': 4, 'Australia': 6, 'Japan': 1, 'America': 7, 'Brazil': 5, 'Cuba': 8, 'China': 0, 'Russia': 2}



    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 7 and cells[0].text.strip() != '航线':
            fromTo = cells[0].text.strip()
            if fromTo != FromTo:
                continue
            destination = cells[2].text.strip()
            for i in countryvalue:
                if destination in countryvalue.keys():
        
                    countrycode = countryvalue[destination]

            url = f"http://172.16.11.127:5007/institutions/company/14/vehiclelinedetail.aspx?id1={fromTo}&id2=S011{countrycode}"

            response = requests.get(url,headers=headers)

            html = response.text
            soup = BeautifulSoup(html, 'lxml')

            table = soup.find('table')

            for row in table.find_all('tr'):
                cells = row.find_all('td')
            
                if len(cells) == 6 and cells[0].text.strip() != '运费' and count % 2 != 0:
                    for i in range(4,6):
                        LCL_M = cells[4].text.strip()
                        time.sleep(1)
                        LCL_W = cells[5].text.strip()
                        time.sleep(1)
                        count += 1
                        break
                elif len(cells) == 6 and cells[0].text.strip() != '运费' and count % 2 == 0:
                    count += 1
                    continue


    return LCL_M,LCL_W

def get_FCL_c_price(FromTo):
    urlHome = 'http://172.16.11.127:5007/institutions/company/11/S0116/4_changyong/changyong2.html'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
    res = requests.get(urlHome,headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'lxml')

    tableUrl = soup.find('table').find('iframe',id = 'center')['src']
    tableUrl = 'http://172.16.11.127:5007/institutions/company/' + tableUrl.replace('../','')

    tableRes = requests.get(tableUrl,headers=headers)
    html = tableRes.text
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find('table')

    countryvalue = {'South Africa': 9, 'Germany': 3, 'UK': 4, 'Australia': 6, 'Japan': 1, 'America': 7, 'Brazil': 5, 'Cuba': 8, 'China': 0, 'Russia': 2}



    count = 1
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 7 and cells[0].text.strip() != '航线':
            fromTo = cells[0].text.strip()
            if fromTo != FromTo:
                continue
            destination = cells[2].text.strip()
            for i in countryvalue:
                if destination in countryvalue.keys():
        
                    countrycode = countryvalue[destination]

            url = f"http://172.16.11.127:5007/institutions/company/14/vehiclelinedetail.aspx?id1={fromTo}&id2=S011{countrycode}"

            response = requests.get(url,headers=headers)

            html = response.text
            soup = BeautifulSoup(html, 'lxml')

            table = soup.find('table')
            
            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) == 6 and cells[0].text.strip() != '运费' and count % 2 == 0:
                    for i in range(1,4):
                        FCL20_c = cells[1].text.strip()
                        time.sleep(1)
                        FCL40_c = cells[2].text.strip()
                        time.sleep(1)
                        FCL40h_c = cells[3].text.strip()
                        time.sleep(1)
                        count += 1
                        break
                elif len(cells) == 6 and cells[0].text.strip() != '运费' and count % 2 != 0:
                    count += 1
                    continue

    return FCL20_c,FCL40_c,FCL40h_c

def get_LCL_c_price(FromTo):
    urlHome = 'http://172.16.11.127:5007/institutions/company/11/S0116/4_changyong/changyong2.html'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
    res = requests.get(urlHome,headers=headers)
    html = res.text
    soup = BeautifulSoup(html, 'lxml')

    tableUrl = soup.find('table').find('iframe',id = 'center')['src']
    tableUrl = 'http://172.16.11.127:5007/institutions/company/' + tableUrl.replace('../','')

    tableRes = requests.get(tableUrl,headers=headers)
    html = tableRes.text
    soup = BeautifulSoup(html, 'lxml')

    table = soup.find('table')

    countryvalue = {'South Africa': 9, 'Germany': 3, 'UK': 4, 'Australia': 6, 'Japan': 1, 'America': 7, 'Brazil': 5, 'Cuba': 8, 'China': 0, 'Russia': 2}



    count = 1
    for row in table.find_all('tr'):
        cells = row.find_all('td')
        if len(cells) == 7 and cells[0].text.strip() != '航线':
            fromTo = cells[0].text.strip()
            if fromTo != FromTo:
                continue
            destination = cells[2].text.strip()
            for i in countryvalue:
                if destination in countryvalue.keys():
        
                    countrycode = countryvalue[destination]

            url = f"http://172.16.11.127:5007/institutions/company/14/vehiclelinedetail.aspx?id1={fromTo}&id2=S011{countrycode}"

            response = requests.get(url,headers=headers)

            html = response.text
            soup = BeautifulSoup(html, 'lxml')

            table = soup.find('table')

            for row in table.find_all('tr'):
                cells = row.find_all('td')
            
                if len(cells) == 6 and cells[0].text.strip() != '运费' and count % 2 == 0:
                    for i in range(4,6):
                        LCL_M_c = cells[4].text.strip()
                        time.sleep(1)
                        LCL_W_c = cells[5].text.strip()
                        time.sleep(1)
                        count += 1
                        break
                elif len(cells) == 6 and cells[0].text.strip() != '运费' and count % 2 != 0:
                    count += 1
                    continue

    return LCL_M_c,LCL_W_c

# （此处完整保留所有get_*_price函数，包括get_FCL_price、get_LCL_price等）

# ---------------------------- GUI界面 ----------------------------
class ShippingCalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("海运成本计算器 v0.4.1")
        self.create_widgets()
        
    def create_widgets(self):
        style = ttk.Style()
        style.configure('TEntry', padding=5)
        style.configure('TButton', padding=5, font=('微软雅黑', 10))
        style.configure('Header.TLabel', font=('微软雅黑', 10, 'bold'))

        input_frame = ttk.LabelFrame(self.root, text="输入参数", style='Header.TLabel')
        input_frame.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        fields = [
            ("销售单位", "sell_id"),
            ("GW（毛重）", "gw"),
            ("CBM（体积）", "cbm"),
            ("总金额", "amount"),
            ("单价", "unit_price"),
            ("航线（如Melbourne-Hamburg）", "FromTo"),
            ("汇率（本币->美元）", "parities"),
        ]
        
        self.entries = {}
        for i, (label, name) in enumerate(fields):
            ttk.Label(input_frame, text=label).grid(row=i, column=0, sticky="e", padx=5, pady=5)
            entry = ttk.Entry(input_frame, width=25)
            entry.grid(row=i, column=1, padx=5, pady=5)
            self.entries[name] = entry

        self.cold_var = tk.StringVar(value="否")
        ttk.Label(input_frame, text="是否是冻柜").grid(row=7, column=0, sticky="e", padx=5, pady=5)
        cold_combobox = ttk.Combobox(input_frame, textvariable=self.cold_var, values=["是", "否"], width=22)
        cold_combobox.grid(row=7, column=1, padx=5, pady=5)

        btn_frame = ttk.Frame(self.root)
        btn_frame.grid(row=1, column=0, pady=10)
        ttk.Button(btn_frame, text="开始计算", command=self.calculate, style='TButton').pack(side=tk.LEFT, padx=10)
        ttk.Button(btn_frame, text="清空输入", command=self.clear, style='TButton').pack(side=tk.LEFT, padx=10)

        self.result_text = tk.Text(self.root, height=18, width=80, font=('Consolas', 10))
        self.result_text.grid(row=2, column=0, padx=15, pady=10)

    def calculate(self):
        try:
            params = {k: entry.get() for k, entry in self.entries.items()}
            params["cold_chain"] = self.cold_var.get()

            # 获取价格数据
            FCL_price = get_FCL_price(params["FromTo"])
            LCL_price = get_LCL_price(params["FromTo"])
            FCL_c_price = get_FCL_c_price(params["FromTo"])
            LCL_c_price = get_LCL_c_price(params["FromTo"])

            maxment = []
            max_order = int((float(params["amount"])/float(params["unit_price"])))
            
            for order_num in range(1, max_order+1):
                bestlist = get_quantity_of_FCL_2(
                    order_num,
                    float(params["sell_id"]),
                    float(params["gw"]),
                    float(params["cbm"])
                )
                
                infact = get_quantity_of_goods(
                    float(params["sell_id"]),
                    float(params["gw"]),
                    float(params["cbm"]),
                    float(FCL_price[0]),
                    float(FCL_price[1]),
                    float(FCL_price[2]),
                    params["cold_chain"],
                    bestlist[0],
                    bestlist[1],
                    bestlist[2]
                )
                maxment.append(infact[1])

            counter = Counter(maxment)
            duplicates = {item: count for item, count in counter.items() if count > 1}
            keyy = [int(k) for k in duplicates.keys() if int(k) <= max_order]
            
            if not keyy:
                keyy.append(min(int(k) for k in duplicates.keys()) if duplicates else [])

            # 构建结果输出
            output = []
            output.append("="*78)
            output.append(f"最多可报{max_order+1}件，推荐订货方案：")
            output.append("="*78)
            
            for item in sorted(keyy):
                if item > max_order:
                    continue
                quantity = get_quantity_of_FCL(
                    item,
                    float(params["sell_id"]),
                    float(params["gw"]),
                    float(params["cbm"]),
                    params["cold_chain"],
                    float(FCL_price[0]),
                    float(FCL_price[1]),
                    float(FCL_price[2]),
                    float(FCL_c_price[0]),
                    float(FCL_c_price[1]),
                    float(FCL_c_price[2])
                )
                output.append(f"► 使用{quantity[1]}个{quantity[0]}集装箱订货{item}件")
            
            output.append("="*78)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "\n".join(output))
            
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：{str(e)}")

    def clear(self):
        for entry in self.entries.values():
            entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)
        self.cold_var.set("否")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("800x700")
    ShippingCalculator(root)
    root.mainloop()