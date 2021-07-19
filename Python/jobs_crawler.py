# import
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import os
from IPython.display import clear_output
from tqdm import tqdm
from os import makedirs
from os.path import join
import warnings
warnings.filterwarnings("ignore")

if __name__ == '__main__':
    # parameters
    headers = {'User-Agent': 'GoogleBot'}
    areas = ['台北市', '新北市', '宜蘭縣', '基隆市', '桃園市', '新竹縣市', '苗栗縣', '台中市', '彰化縣',
             '南投縣', '雲林縣', '嘉義縣市', '台南市', '高雄市', '屏東縣', '台東縣', '花蓮縣', '澎湖縣', '金門縣', '連江縣']
    jobs = ['經營╱幕僚類人員', '人力資源類人員', '行政╱總務類人員', '法務╱智財類人員', '財務╱會計╱稅務類', '金融專業相關類人員', '行銷類人員', '產品企劃類人員', '專案╱產品管理類人員', '客戶服務類人員', '門市營業類人員', '業務銷售類人員', '貿易類人員', '餐飲類人員', '旅遊休閒類人員', '美容╱美髮類人員', '軟體╱工程類人員', 'MIS╱網管類人員', '工程研發類人員', '化工材料研發類人員', '生技╱醫療研發類人員', '生產管理類人員',
            '製程規劃類人員', '品保╱品管類人員', '環境安全衛生類人員', '操作╱技術類人員', '維修╱技術服務類人員', '採購╱資材╱倉管類人員', '運輸物流類人員', '營建規劃類人員', '營建施作類人員', '製圖╱測量類人員', '設計類人員', '傳播藝術類人員', '文字編譯類人員', '記者及採訪類人員', '醫療專業類人員', '醫療╱保健服務人員', '學術研究類人員', '教育輔導類人員', '軍警消防類人員', '保全類人員', '農林漁牧相關類人員', '其他類人員']
    area_of_intrest = ['雲林縣']
    job_of_intrest = ['軟體╱工程類人員']
    patience = 20
    data_path = './data'
    makedirs(name=data_path, exist_ok=True)

    # area code
    url = 'https://static.104.com.tw/category-tool/json/Area.json'
    resp = requests.get(url)
    df1 = []
    for i in resp.json()[0]['n']:
        if i['des'] in area_of_intrest:
            ndf = pd.DataFrame(i['n'])
            ndf['city'] = i['des']
            df1.append(ndf)
    df1 = pd.concat(df1, ignore_index=True)
    df1 = df1.loc[:, ['city', 'des', 'no']]
    df1 = df1.sort_values('no')

    # job code
    url = 'https://static.104.com.tw/category-tool/json/JobCat.json'
    resp = requests.get(url)
    df2 = []
    for i in resp.json():
        for j in i['n']:
            if j['des'] in job_of_intrest:
                ndf = pd.DataFrame(j['n'])
                ndf['des1'] = i['des']  # 職務大分類
                ndf['des2'] = j['des']  # 職務小分類
                df2.append(ndf)
    df2 = pd.concat(df2, ignore_index=True)
    df2 = df2.loc[:, ['des1', 'des2', 'des', 'no']]
    df2 = df2.sort_values('no')

    #
    tmp = pd.DataFrame([re.sub('\.pkl', '', file)
                        for file in os.listdir('./data')], columns=['no'])
    df1 = pd.merge(df1, tmp, how='left', on='no', indicator=True)
    df1 = df1.loc[df1['_merge'] != 'both', :]

    # get jobs
    columns = ['公司名稱', '公司編號', '公司類別', '公司類別描述', '公司連結', '職缺名稱', '職務性質', '職缺大分類',
               '職缺中分類', '職缺小分類', '職缺編號', '職務內容', '更新日期', '職缺連結', '薪資', '標籤', '公司地址', '地區', '經歷', '學歷']

    for areades, areacode in tqdm(zip(df1['des'], df1['no']), total=len(df1['des'])):
        values = []
        for jobdes1, jobdes2, jobdes, jobcode in zip(df2['des1'], df2['des2'], df2['des'], df2['no']):
            print(areades, ' | ', jobdes1, ' - ', jobdes2, ' - ', jobdes)
            page = 1
            number_of_attempts = 0
            while page < 150:
                try:
                    url = 'https://www.104.com.tw/jobs/search/?ro=0&jobcat={}&jobcatExpansionType=1&area={}&order=11&asc=0&page={}&mode=s&jobsource=2018indexpoc'.format(
                        jobcode, areacode, page)
                    # print(url)
                    resp = requests.get(url, headers=headers)
                    soup = BeautifulSoup(resp.text)
                    soup2 = soup.find('div', {'id': 'js-job-content'}).findAll(
                        'article', {'class': 'b-block--top-bord job-list-item b-clearfix js-job-item'})
                    # print(len(soup2))

                    for job in soup2:

                        update_date = job.find(
                            'span', {'class': 'b-tit__date'}).text
                        update_date = re.sub('\r|\n| ', '', update_date)

                        try:
                            address = job.select('ul > li > a')[0]['title']
                            address = re.findall('公司住址：(.*?)$', address)[0]
                        except:
                            address = ''

                        loc = job.find('ul', {
                                       'class': 'b-list-inline b-clearfix job-list-intro b-content'}).findAll('li')[0].text
                        exp = job.find('ul', {
                                       'class': 'b-list-inline b-clearfix job-list-intro b-content'}).findAll('li')[1].text
                        try:
                            edu = job.find('ul', {
                                           'class': 'b-list-inline b-clearfix job-list-intro b-content'}).findAll('li')[2].text
                        except:
                            edu = ''

                        try:
                            content = job.find('p').text
                        except:
                            content = ''
                        try:
                            tags = [tag.text for tag in soup2[0].find(
                                'div', {'class': 'job-list-tag b-content'}).findAll('span')]
                        except:
                            tags = []

                        value = [job['data-cust-name'],  # 公司名稱
                                 job['data-cust-no'],  # 公司編號
                                 job['data-indcat'],  # 公司類別
                                 job['data-indcat-desc'],  # 公司類別描述
                                 job.select('ul > li > a')[0]['href'],  # 公司連結
                                 job['data-job-name'],  # 職缺名稱
                                 # 職務性質 _判斷全職兼職 1全職/2兼職/3高階/4派遣/5接案/6家教
                                 job['data-job-ro'],
                                 jobdes1,  # 職缺大分類
                                 jobdes2,  # 職缺中分類
                                 jobdes,  # 職缺小分類
                                 job['data-job-no'],  # 職缺編號
                                 content,  # 職務內容
                                 update_date,  # 更新日期
                                 # 職缺連結
                                 job.find(
                                     'a', {'class': 'js-job-link'})['href'],
                                 tags[0],   #薪資
                                 tags[1:],  # 標籤
                                 address,  # 公司地址
                                 loc,  # 地區
                                 exp,  # 經歷
                                 edu  # 學歷
                                 ]
                        values.append(value)

                    page += 1
                    # print(len(values))
                    if len(soup2) < 20:
                        break
                except:
                    if number_of_attempts >= patience:
                        break
                    else:
                        number_of_attempts += 1
                        print('Retry')

        df = pd.DataFrame()
        df = pd.DataFrame(values, columns=columns)
        df.to_pickle(join(data_path, '{}.pkl'.format(areacode)))
        clear_output()
        print('===================================  Save Data  ===================================')

    # combine the data
    df = []
    for i in os.listdir(data_path):
        if '.pkl' in i:
            ndf = pd.read_pickle(join(data_path, i))
            df.append(ndf)
    df = pd.concat(df, ignore_index=True)
    df.to_csv(join(data_path, 'result.csv'))
