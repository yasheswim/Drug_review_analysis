# -*- coding: utf-8 -*-
"""
Created on Thu Dec 17 16:19:22 2020

@author: YASHESWI MISHRA
"""

from bs4 import BeautifulSoup as bs
import requests
##Source-Drugs.com
link='https://www.drugs.com/comments/tretinoin-topical/'
page = requests.get(link)
page
page.content
soup = bs(page.content,'html.parser')
print(soup.prettify())
names = soup.find_all('span',class_='user-name')
names

##Extracting customers name
cust_name = []
for i in range(0,len(names)):
    cust_name.append(names[i].get_text())
cust_name

##Extracting conditions
condition = soup.find_all('p',class_='ddc-comment-content')
type(condition)

cond = []
for i in range(0,len(condition)):
    cond.append(condition[i].get_text())
cond

condition_new=[i.split('\t', 1)[0] for i in cond]
condition_new[:] = [titles.lstrip('\n') for titles in condition_new]
condition_new[:] = [titles.rstrip(':') for titles in condition_new]
condition_new

##Extracting ratings
rating = soup.find_all('div',class_='ddc-rating-summary ddc-mgb-2')
rating

rate = []
for i in range(0,len(rating)):
    rate.append(rating[i].get_text())
rate
rate[:]=[rat.rstrip('\n\n\n\n\n') for rat in rate ]
rate[:]=[rat.lstrip('\n') for rat in rate ]
rate[:]=[rat.split('/',1)[0] for rat in rate]

##Extracting reviews
review = soup.find_all("p",class_='ddc-comment-content')
reviews = []
for i in range(0,len(review)):
    reviews.append(review[i].get_text())
reviews_new=[i.split('\t', 1)[1] for i in cond]
reviews_new[:]=[rev.lstrip('\t\t') for rev in reviews_new]
reviews_new[:]=[rev.rstrip('\n\t\t') for rev in reviews_new]
reviews_new

##Extracting dates
date=soup.find_all('span',class_='comment-date ddc-text-color-secondary')
post_date=[]
for d in range (0,len(date)):
    post_date.append(date[d].get_text())


##Extracting likes/upcounts
upcount=soup.find_all('div',class_='ddc-comment-actions')
upcount
upcounts=[]
for i in range (0,len(upcount)):
    upcounts.append(upcount[i].get_text())

upcounts[:]=[up.lstrip('\n\t\t\t') for up in upcounts]
upcounts[:]=[up.rstrip('\n') for up in upcounts]
upcounts_new=[]
for y in range(len(upcounts)):
    if y%2!=0:
        upcounts_new.append(upcounts[y])
upcounts_new=[i.split('\n')[0] for i in upcounts_new]
upcounts_new


import pandas as pd
df = pd.DataFrame()
df['Name']=cust_name
df['Condition']=condition_new
df['reviews']=reviews_new
df['Ratings']=rate
df['Date']=post_date
df['Upvotes']=upcounts_new
df["Reviews"] = df['reviews'].str.replace('“',' ')
df=df.drop(["reviews"],axis=1)
df['Medicine']=pd.DataFrame(['Tretenion-tropical']*25)
df=df.replace(to_replace=['Retin-A (tretinoin) for Acne','Stieva-A (tretinoin) for Acne'],value='Acne')
df['Condition']= df['Condition'].str.replace('For',' ')

df=df.iloc[:,[0,6,1,5,2,3,4]]

df.to_csv('ws1.csv')

###Source-Drugs.com

rev=[]
cust=[]
date=[]
rate=[]
likes=[]
for i in range (1,7):
    link1='https://www.drugs.com/comments/minoxidil-topical/for-alopecia.html?page='+str(i)
    response1 = requests.get(link1)
    soup1 = bs(response1.content,"html.parser")# creating soup object to iterate over the extracted content 
    reviews1 = soup1.find_all("p",class_='ddc-comment-content')
    cust_name1=soup1.find_all('span',class_='user-name') 
    date1=soup1.find_all('span',class_='comment-date') 
    rating1=soup1.find_all('div',class_='ddc-comment')
    like1=soup1.find_all('div',class_='ddc-comment-actions')
    for i in range(len(reviews1)):
        rev.append(reviews1[i].get_text()) 
        cust.append(cust_name1[i].get_text())
        date.append(date1[i].get_text())
        rate.append(rating1[i].get_text())
        likes.append(like1[i].get_text())
        likes
        
cust    
##Condition       
condition1=[i.split('\t',1)[0] for i in rev]
condition1
condition1=[cond1.rstrip(':\n') for cond1 in condition1 ]
condition1=[cond1.lstrip('\n') for cond1 in condition1 ]

##Reviews
rev1=[i.split('\t',1)[1] for i in rev]
rev1=[i.rstrip('\n\t\t') for i in rev1]
rev1=[i.lstrip('\t\t\t\t\t') for i in rev1]       
rate
##Ratings
rate1=[i.split('Was this helpful?\n\t\t\t\t\xa0\n\t\t\t\tYes\n\t\t\t\t\xa0\n\t\t\t\tNo\n\n\n\n',1)[0] for i in rate]
rate1=[i.split('\n\t\t\n\n',1)[1]for i in rate1]  
rate1=[i.rstrip('\n\n\n\n\n\n\n\n\t\t\t\t') for i in rate1]


##likes
like1=[i.split('\tNo\n\n\n\n',1)[1] for i in rate]
like1=[i.rstrip('\n\n·\nReport\n\n\n') for i in like1]

import pandas as pd
import numpy as np
df = pd.DataFrame()
df['Name']=cust
df['Condition']=pd.DataFrame(['Hairline thinning']*134)
df['reviews']=rev1
rate1=[i.split('/',1)[0] for i in rate1 ]
df['Ratings']=rate1
df['Date']=date
df['Upvotes']=like1
df["Reviews"] = df['reviews'].str.replace('“',' ')
df=df.drop(["reviews"],axis=1)
df['Medicine']=pd.DataFrame(['Minoxidil Topical']*134)
df=df.iloc[:,[0,6,1,5,2,3,4]]
df = df.replace(r'^\s*$', np.nan, regex=True)
df_new=df
df_new.to_csv('ws2.csv')
df_old=pd.read_csv('ws1.csv')
final_dataset=pd.concat([df_old,df_new])
final_dataset.to_csv('new1.csv',index=False)


##Skin cancer
rev=[]
cust=[]
date=[]
rate=[]
likes=[]
for i in range (1,10):
    link1='https://www.drugs.com/comments/fluorouracil-topical/efudex.html?page='+str(i)
    response1 = requests.get(link1)
    soup1 = bs(response1.content,"html.parser")# creating soup object to iterate over the extracted content 
    reviews1 = soup1.find_all("p",class_='ddc-comment-content')
    cust_name1=soup1.find_all('span',class_='user-name') 
    date1=soup1.find_all('span',class_='comment-date') 
    rating1=soup1.find_all('div',class_='ddc-comment')
    like1=soup1.find_all('div',class_='ddc-comment-actions')
    for i in range(len(reviews1)):
        rev.append(reviews1[i].get_text()) 
        cust.append(cust_name1[i].get_text())
        date.append(date1[i].get_text())
        rate.append(rating1[i].get_text())
        likes.append(like1[i].get_text())
        likes
        
##Extracting condition
condition=[i.split('\t\t\t',1)[0] for i in rev]
condition=[i.lstrip('\n') for i in condition]       
condition=[i.rstrip(':') for i in condition]  

##Extracting reviews
review=[i.split('\t\t\t',1)[1] for i in rev]
review=[i.rstrip('\n\t\t') for i in review]

##Extracting rate
rate1=[i.split('Was this helpful?\n\t\t\t\t\xa0\n\t\t\t\tYes\n\t\t\t\t\xa0\n\t\t\t\tNo\n\n\n\n',1)[0] for i in rate]
rate1=[i.split('\n\t\t\n\n',1)[1]for i in rate1]  
rate1=[i.rstrip('\n\n\n\n\n\n\n\n\t\t\t\t') for i in rate1]

##Extracting likes
like1=[i.split('\tNo\n\n\n\n',1)[1] for i in rate]
like1=[i.rstrip('\n\n·\nReport\n\n\n') for i in like1]

import pandas as pd
import numpy as np
df = pd.DataFrame()
df['Name']=cust
df['condition']=condition
df['Condition']=df['condition'].str.replace('For',' ')
df['Condition'].fillna('Keratosis',inplace=True)
df['reviews']=review
rate1=[i.split('/',1)[0] for i in rate1 ]
df['Ratings']=rate1
df['Date']=date
df['Upvotes']=like1
df["Reviews"] = df['reviews'].str.replace('“',' ')
df=df.drop(["reviews"],axis=1)
df=df.drop(["condition"],axis=1)
df['Medicine']=pd.DataFrame(['Efudex']*177)
df=df.iloc[:,[0,6,1,5,2,3,4]]
df = df.replace(r'^\s*$', np.nan, regex=True)
df_old=pd.read_csv('new1.csv')
df_latest=pd.concat([df,df_old])
df_latest.to_csv('nicegoing.csv',index=False)


##Acne treatment
rev=[]
cust=[]
date=[]
rate=[]
likes=[]
for i in range (1,10):
    link1='https://www.drugs.com/comments/spironolactone/?page='+str(i)
    response1 = requests.get(link1)
    soup1 = bs(response1.content,"html.parser")# creating soup object to iterate over the extracted content 
    reviews1 = soup1.find_all("p",class_='ddc-comment-content')
    cust_name1=soup1.find_all('span',class_='user-name') 
    date1=soup1.find_all('span',class_='comment-date') 
    rating1=soup1.find_all('div',class_='ddc-comment')
    like1=soup1.find_all('div',class_='ddc-comment-actions')
    for i in range(len(reviews1)):
        rev.append(reviews1[i].get_text()) 
        cust.append(cust_name1[i].get_text())
        date.append(date1[i].get_text())
        rate.append(rating1[i].get_text())
        likes.append(like1[i].get_text())
        likes
        
##Extracting condition
condition=[i.split('\t\t\t',1)[0] for i in rev]
condition=[i.lstrip('\n') for i in condition]       
condition=[i.rstrip(':') for i in condition]  

##Extracting reviews
review=[i.split('\t\t\t',1)[1] for i in rev]
review=[i.rstrip('\n\t\t') for i in review]

##Extracting rate
rate1=[i.split('Was this helpful?\n\t\t\t\t\xa0\n\t\t\t\tYes\n\t\t\t\t\xa0\n\t\t\t\tNo\n\n\n\n',1)[0] for i in rate]
rate1=[i.split('\n\t\t\n\n',1)[1]for i in rate1]  
rate1=[i.rstrip('\n\n\n\n\n\n\n\n\t\t\t\t') for i in rate1]

##Extracting likes
like1=[i.split('\tNo\n\n\n\n',1)[1] for i in rate]
like1=[i.rstrip('\n\n·\nReport\n\n\n') for i in like1]

import pandas as pd
import numpy as np
df = pd.DataFrame()
df['Name']=cust
df['condition']=condition
df=df.replace(to_replace='Aldactone (spironolactone) for Alopecia',value='Alopecia')
df['Condition']=df['condition'].str.replace('For',' ')
df['Condition'].fillna('Acne',inplace=True)
df['reviews']=review
rate1=[i.split('/',1)[0] for i in rate1 ]
df['Ratings']=rate1
df['Date']=date
df['Upvotes']=like1
df["Reviews"] = df['reviews'].str.replace('“',' ')
df=df.drop(["reviews"],axis=1)
df=df.drop(["condition"],axis=1)
df['Medicine']=pd.DataFrame(['Spironolactone']*225)
df=df.iloc[:,[0,6,1,5,2,3,4]]
df = df.replace(r'^\s*$', np.nan, regex=True)
df_old=pd.read_csv('nicegoing.csv')
df_latest=pd.concat([df,df_old])
df_latest.to_csv('brandnew.csv',index=False)














