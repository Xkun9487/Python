import requests
from bs4 import BeautifulSoup
import time
import math

def defind_FCL(sell_id, gw, cbm, FCL20_quantity):
    
    FCL20G = FCL20_quantity * 25
    FCL20C = FCL20_quantity * 33


    one_FCL20 = min(FCL20G, FCL20C)

    FCL20_quantity1 = int(min(FCL20G / (gw / 1000 * sell_id),FCL20C / (cbm * sell_id)))

    if FCL20_quantity1 < one_FCL20:
        return 1
    else:
        return 0

def get_quantity_of_goods(sell_id, gw, cbm, FCL20, FCL40, FCL40h, cold, FCL20_quantity, FCL40_quantity, FCL40h_quantity):
    
    FCL20G = FCL20_quantity * 25
    FCL20C = FCL20_quantity * 33

    FCL40G = FCL40_quantity * 29
    FCL40C = FCL40_quantity * 67

    FCL40hG = FCL40h_quantity * 29
    FCL40hC = FCL40h_quantity * 76



    FCL20_quantity1 = int(min(FCL20G / (gw / 1000 * sell_id),FCL20C / (cbm * sell_id)))
    FCL40_quantity1 = int(min(FCL40G / (gw / 1000 * sell_id),FCL40C / (cbm * sell_id)))
    FCL40h_quantity1 = int(min(FCL40hG / (gw / 1000 * sell_id),FCL40hC / (cbm * sell_id)))

    FCL_COU = {FCL20_quantity1:FCL20,FCL40_quantity1:FCL40,FCL40h_quantity1:FCL40h}

    keys = []
    values = []

    for key,value in FCL_COU.items():
        keys.append(key)
        values.append(value)
        if key == max(keys) and value == min(values):

            Best = key * sell_id
    

    FCL = {FCL20_quantity1:['FCL20',FCL20_quantity1],FCL40_quantity1:['FCL40',FCL40_quantity1],FCL40h_quantity1:['FCL40h',FCL40h_quantity1]}
    FCL_c = {FCL20_quantity1:['FCL20_c',FCL20_quantity1],FCL40_quantity1:['FCL40_c',FCL40_quantity1],FCL40h_quantity1:['FCL40h_c',FCL40h_quantity1]}

    if cold == "否":
    
        return FCL[Best]
    else:
        
        return FCL_c[Best]
    
def get_quantity_of_FCL_2(order_num, sell_id, gw, cbm):
    package_id = order_num / sell_id
    total_gw = package_id * gw / 1000
    total_cbm = package_id * cbm
    
    FCL20G = total_gw / 25
    FCL20C = total_cbm / 33

    FCL40G = total_gw / 29
    FCL40C = total_cbm / 67

    FCL40hG = total_gw / 29
    FCL40hC = total_cbm / 76

    FCL20_quantity = int(max(FCL20G,FCL20C))
    if FCL20_quantity == 0:
        FCL20_quantity = 1
    FCL40_quantity = int(max(FCL40G,FCL40C))
    FCL40h_quantity = int(max(FCL40hG,FCL40hC))

    return [FCL20_quantity,FCL40_quantity,FCL40h_quantity]

def get_quantity_of_FCL(order_num, sell_id, gw, cbm, FCL20, FCL40, FCL40h, cold):
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

    FCL = {FCL20*FCL20_quantity:['FCL20',FCL20_quantity],FCL40*FCL40_quantity:['FCL40',FCL40_quantity],FCL40h*FCL40h_quantity:['FCL40h',FCL40h_quantity]}
    FCL_c = {FCL20*FCL20_quantity:['FCL20_c',FCL20_quantity],FCL40*FCL40_quantity:['FCL40_c',FCL40_quantity],FCL40h*FCL40h_quantity:['FCL40h_c',FCL40h_quantity]}

    if cold == "否":
        result = min(FCL20_quantity*FCL20,FCL40_quantity*FCL40,FCL40h_quantity*FCL40h)
        return FCL[result]
    else:
        result = min(FCL20_quantity*FCL20,FCL40_quantity*FCL40,FCL40h_quantity*FCL40h)
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


while True:
    try:
        order_num = input('请输入订量：')
        sell_id = input('请输入销售单位：')
        gw = input('请输入GW：')
        cbm = input('请输入CBM：')
        FromTo = input('请输入航线：')
        parities = input('请输入汇率(本币->美元)：')
        cold_chain = input('是否是冻柜？(是/否)：')

        FCL_price = get_FCL_price(FromTo)
        LCL_price = get_LCL_price(FromTo)
        FCL_c_price = get_FCL_c_price(FromTo)
        LCL_c_price = get_LCL_c_price(FromTo)

        print('=========================运费信息==============================')
        print('==============================================================')
        print(f'FCL20:{FCL_price[0]}，FCL40:{FCL_price[1]}，FCL40h:{FCL_price[2]}')
        print(f'LCL_M:{LCL_price[0]}，LCL_W:{LCL_price[1]}')
        print(f'FCL20_c:{FCL_c_price[0]}，FCL40_c:{FCL_c_price[1]}，FCL40h_c:{FCL_c_price[2]}')
        print(f'LCL_M_c:{LCL_c_price[0]}，LCL_W_c:{LCL_c_price[1]}')
        print('===============================================================\n')

        FCL_price_1 = {'FCL20':float(FCL_price[0]),'FCL40':float(FCL_price[1]),'FCL40h':float(FCL_price[2])}
        FCL_c_price_1 = {'FCL20_c':float(FCL_c_price[0]),'FCL40_c':float(FCL_c_price[1]),'FCL40h_c':float(FCL_c_price[2])}
        LCL_price_1 = {'LCL_M':float(LCL_price[0]),'LCL_W':float(LCL_price[1])}
        LCL_c_price_1 = {'LCL_M_c':float(LCL_c_price[0]),'LCL_W_c':float(LCL_c_price[1])}

        bestlist = get_quantity_of_FCL_2(float(order_num), float(sell_id), float(gw), float(cbm))

        if cold_chain == '否':
            num = get_quantity_of_FCL(float(order_num), float(sell_id), float(gw), float(cbm),float(FCL_price[0]),float(FCL_price[1]),float(FCL_price[2]),cold_chain)
            infact = get_quantity_of_goods(float(sell_id), float(gw), float(cbm),float(FCL_price[0]),float(FCL_price[1]),float(FCL_price[2]),cold_chain,bestlist[0],bestlist[1],bestlist[2])
            print(f'使用{num[0]}最划算，数量：{num[1]}个。\n共计：{num[1]*FCL_price_1[num[0]]:.4f}美元, {(num[1]*FCL_price_1[num[0]])/float(parities):.4f}本币\n')
            if defind_FCL(float(sell_id), float(gw), float(cbm),bestlist[0]) != 1:
                print(f'最优箱型：{infact[0]}，最优订货数量：{infact[1]}\n')
            else:
                print('货物过少，无法确定最优箱型与最优订货数量')
        else:
            num = get_quantity_of_FCL(float(order_num), float(sell_id), float(gw), float(cbm),float(FCL_c_price[0]),float(FCL_c_price[1]),float(FCL_c_price[2]),cold_chain)
            infact = get_quantity_of_goods(float(sell_id), float(gw), float(cbm),float(FCL_price[0]),float(FCL_price[1]),float(FCL_price[2]),cold_chain,bestlist[0],bestlist[1],bestlist[2])
            print(f'使用{num[0]}最划算，数量：{num[1]}个。\n共计：{num[1]*FCL_c_price_1[num[0]]:.4f}美元, {(num[1]*FCL_c_price_1[num[0]])/float(parities):.4f}本币')
            if defind_FCL(float(sell_id), float(gw), float(cbm),bestlist[0]) != 1:
                print(f'最优箱型：{infact[0]}，最优订货数量：{infact[1]}\n')
            else:
                print('货物过少，无法确定最优箱型与最优订货数量')
        time.sleep(5)
    except:
        print('输入错误或未登录POCIB，请检查输入或重新登录POCIB')
        continue
        

#测试数据
#请输入订量：9500
#请输入销售单位：1
#请输入GW：13.5
#请输入CBM：0.0173
#请输入航线：Melbourne-Hamburg
#请输入汇率(本币->美元):1.0345
#是否是冻柜？(是/否): 是