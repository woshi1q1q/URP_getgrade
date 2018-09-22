import requests,json,re,xlwt

#获取商户信息
def get_ele(page):
    url = 'https://h5.ele.me/restapi/shopping/v3/restaurants?latitude=坐标&longitude=坐标&offset=8&limit=%s&extras[]=activities&extras[]=tags&extra_filters=home&rank_id=5a63b2f2eb424f828c6a6dacb45296b5&terminal=h5'%page #需要提取饿了么坐标信息
    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36'}
    s = requests.get(url,headers=headers).text    
    return json.loads(s)


#生成excel文件
workbook = xlwt.Workbook(encoding = 'utf-8')
worksheet = workbook.add_sheet('ELM_info')
worksheet.write(0,0,'商户')
worksheet.write(0,1,'新用户优惠')
worksheet.write(0,2,'满减优惠')
worksheet.write(0,3,'配送费')

row = 0
for page in range(0,2000,8):
    obj = get_ele(page)
    for restaurant in obj.get('items'):
        row = row+1
        shop_name = restaurant['restaurant']['name']
        ps_price= restaurant['restaurant']['piecewise_agent_fee']['description']
        try:
            new_favorable = restaurant['restaurant']['activities'][0]['tips']
        except:
            new_favorable = '无新用户优惠'
        try:
            mj_favorable = restaurant['restaurant']['activities'][1]['description']
        except:
            mj_favorable = '无满减优惠'        
        worksheet.write(row,0,shop_name)
        worksheet.write(row,1,new_favorable)
        worksheet.write(row,2,mj_favorable)
        worksheet.write(row,3,ps_price)
workbook.save('ele.xls')

