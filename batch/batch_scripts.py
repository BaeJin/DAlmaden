import pandas as pd
import xlsxwriter
batch_name='U&A_sample'
keyword_list = ["카페",
"드라이기",
"카페 내돈내산",
"드라이기 내돈내산"
]

year_list = ['2016','2017','2018','2019','2020']
month_list = ['01','02','03','04','05','06','07','08','09','10','11','12']
date = ['31','28','31','30','31','30', '31', '31', '30', '31', '30', '31']
start_date_list = []
end_date_list = []
script_list = []
script = "python C:\\Users\\User\\Documents\\pycharm\\DAlmaden\\engine\\crawler\\dc1_Crawler_naverblog_batch.py"

for keyword in keyword_list:
    for year in year_list:
        for index, month in enumerate(month_list):
            start_date = '{}-{}-01'.format(year,month)
            end_date = '{}-{}-{}'.format(year,month,date[index])
            script_dict = {'script': script+' '+'\"'+keyword+'\"'+' '+start_date+' '+end_date+' '+' '+str(300)}
            script_list.append(script_dict)

df_sc = pd.DataFrame(script_list)

df_sc.to_excel(batch_name+"_"+"batch_scripts.xlsx")