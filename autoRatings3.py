from re import I
from xml.sax.handler import property_interning_dict
import pandas as pd
from openpyxl import load_workbook
import openpyxl as xl
import numpy as np
from sigmoid import noneSigmoid
import os


'''
< 데이터 전처리 ratings1 ~ ratings10 파일 정리하기 >

1. UserPRS 폴더 안에 있는 outputUser1~57 파일을 읽어온다.
2. outputUser1 파일의 prop_n 시트를 읽어온다.
3. userId	itemId(user)	Pt-PRS+DPt-PRS(score)	propertyId(prop_2) 	칼럼에 맞게 생성한다.
Se(Pt-PRS)    Sd(DPt-PRS)

def readOutput(), def writeRatings()
'''


userId, itemId, Pt_PRS, propertyId  = [], [], [], []


# ratings2에 대한 Pt_PRS 구하기
for user in range(1,58):
    excel_path = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\UserPRS\\outputUser{user}.xlsx"

    # sheet_name : propId
    # propId=2인 시트를 57개 불러와서 저장한다.
    globals()[f'dfUser{user}'] = pd.read_excel(excel_path, sheet_name=0)
    
    item = globals()[f'dfUser{user}']['user']
    globals()[f'Pt_PRS_{user}'] = globals()[f'dfUser{user}']['Se']
    
    nums = len(globals()[f'Pt_PRS_{user}'])
    # print(nums)
    # userID, propertyID : 한 파일에 대한 값 리스트
    userID, propertyID = [], []
    for num in range(0,nums):
        userID.append(user)
        propertyID.append(1)

    # 리스트 제거
    userID_str = str(userID)[1:-1]
    propertyID_str = str(propertyID)[1:-1]
    
    # 전체 파일에 대한 값 리스트
    Pt_PRS.append(globals()[f'Pt_PRS_{user}'])  # dataframe
    itemId.append(item)     # dataframe
    userId.append(userID_str)
    propertyId.append(propertyID_str)
    
    # print(Pt_PRS, itemId, userId, propertyId)
    # print(len(userId), len(itemId), len(Pt_PRS), len(propertyId))

    globals()[f'ratings_{user}_Pt_PRS'] = pd.DataFrame({'userId': userID, 'itemId': item, 
                                                'Pt_PRS': globals()[f'Pt_PRS_{user}'], 
                                                'propertyId': propertyID })

    # print(globals()[f'ratings_{user}'])
    if user == 1:
        ratings_1_Pt_PRS = ratings_1_Pt_PRS
    else:
        globals()[f'ratings_{user}_Pt_PRS'] = globals()[f'ratings_{user-1}_Pt_PRS'].append(globals()[f'ratings_{user}_Pt_PRS'])


# ratings2에 대한 DPt_PRS 구하기
for user in range(1,58):
    excel_path = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\UserPRS\\outputUser{user}.xlsx"

    # sheet_name : propId
    # propId=2인 시트를 57개 불러와서 저장한다.
    globals()[f'dfUser{user}'] = pd.read_excel(excel_path, sheet_name=0)
    
    item = globals()[f'dfUser{user}']['user']
    globals()[f'Pt_PRS_{user}'] = globals()[f'dfUser{user}']['Sd']
    
    nums = len(globals()[f'Pt_PRS_{user}'])
    # print(nums)
    # userID, propertyID : 한 파일에 대한 값 리스트
    userID, propertyID = [], []
    for num in range(0,nums):
        userID.append(user)
        propertyID.append(1)

    # 리스트 제거
    userID_str = str(userID)[1:-1]
    propertyID_str = str(propertyID)[1:-1]
    
    # 전체 파일에 대한 값 리스트
    Pt_PRS.append(globals()[f'Pt_PRS_{user}'])  # dataframe
    itemId.append(item)     # dataframe
    userId.append(userID_str)
    propertyId.append(propertyID_str)
    
    # print(Pt_PRS, itemId, userId, propertyId)
    # print(len(userId), len(itemId), len(Pt_PRS), len(propertyId))

    globals()[f'ratings_{user}_DPt_PRS'] = pd.DataFrame({'userId': userID, 'itemId': item, 
                                                'DPt_PRS': globals()[f'Pt_PRS_{user}'], 
                                                'propertyId': propertyID })

    # print(globals()[f'ratings_{user}'])
    if user == 1:
        ratings_1_DPt_PRS = ratings_1_DPt_PRS
    else:
        globals()[f'ratings_{user}_DPt_PRS'] = globals()[f'ratings_{user-1}_DPt_PRS'].append(globals()[f'ratings_{user}_DPt_PRS'])



# ratings2에 대한 Pt_PRS + DPt_PRS 구하기
for user in range(1,58):
    excel_path = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\UserPRS\\outputUser{user}.xlsx"

    # sheet_name : propId
    # propId=2인 시트를 57개 불러와서 저장한다.
    globals()[f'dfUser{user}'] = pd.read_excel(excel_path, sheet_name=0)
    
    item = globals()[f'dfUser{user}']['user']
    globals()[f'Pt_PRS_{user}'] = globals()[f'dfUser{user}']['score']
    
    nums = len(globals()[f'Pt_PRS_{user}'])
    # print(nums)
    # userID, propertyID : 한 파일에 대한 값 리스트
    userID, propertyID = [], []
    for num in range(0,nums):
        userID.append(user)
        propertyID.append(1)

    # 리스트 제거
    userID_str = str(userID)[1:-1]
    propertyID_str = str(propertyID)[1:-1]
    
    # 전체 파일에 대한 값 리스트
    Pt_PRS.append(globals()[f'Pt_PRS_{user}'])  # dataframe
    itemId.append(item)     # dataframe
    userId.append(userID_str)
    propertyId.append(propertyID_str)
    
    # print(Pt_PRS, itemId, userId, propertyId)
    # print(len(userId), len(itemId), len(Pt_PRS), len(propertyId))

    globals()[f'ratings_{user}_PRS'] = pd.DataFrame({'userId': userID, 'itemId': item, 
                                                'PRS': globals()[f'Pt_PRS_{user}'], 
                                                'propertyId': propertyID })

    # print(globals()[f'ratings_{user}'])
    if user == 1:
        ratings_1_PRS = ratings_1_PRS
    else:
        globals()[f'ratings_{user}_PRS'] = globals()[f'ratings_{user-1}_PRS'].append(globals()[f'ratings_{user}_PRS'])

    
ratings_1 = pd.ExcelWriter('ratings_1.xlsx', engine='openpyxl')
ratings_57_Pt_PRS.to_excel(ratings_1, sheet_name="Pt-PRS")
ratings_57_DPt_PRS.to_excel(ratings_1, sheet_name="DPt-PRS")
ratings_57_PRS.to_excel(ratings_1, sheet_name="Pt-PRS+DPt-PRS")
ratings_1.save()