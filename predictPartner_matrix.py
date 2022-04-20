# import tensorflow as tf
import pandas as pd
from openpyxl import Workbook
import openpyxl as xl
import numpy as np
from sigmoid import noneSigmoid
from collaborating4 import get_based_collabor
from MatrixFactoriztaion5 import matrixFactorization, recommend_item



'''
[ Matrix Factorization - giver 기준 ]

1. while문으로 한 행씩 읽기
2. Collaborative 함수 호출 / 각 행의 userId, top input 
3. return 값을 Top5, Top3, Top5로 각각 시트에 넣기

'''


# 데이터준비
df = "C:\\Users\\kkbo5\\Desktop\\AIIP_Lab\\smart_coordinating\\testData4.xlsx"
dealTB = pd.read_excel(df, sheet_name=2)
dfDealTop1 = pd.read_excel(df, sheet_name=2)
dfDealTop3 = pd.read_excel(df, sheet_name=2)
dfDealTop5 = pd.read_excel(df, sheet_name=2)


# 데이터준비
ratings = "C:\\Users\\kkbo5\\Documents\GitHub\Coordinating\\ratings\\ratings.xlsx"
users = "C:\\Users\\kkbo5\\Desktop\\AIIP_Lab\\smart_coordinating\\user-item.xlsx"

df_ratings = pd.read_excel(ratings, sheet_name=2)
df_users = pd.read_excel(users, sheet_name=0)
df_svd_preds = matrixFactorization('PRS')



def predictMatrixbased():
    
    i = 0
    recommendUserTop1, recommendUserTop3, recommendUserTop5 = [], [], []

   
    while i < 365:
        rowUser = dealTB['giver'].loc[i]
        predictTop1 = recommend_item(df_svd_preds, rowUser, df_users, df_ratings, 10)    # 리스트 반환
        predictTop3 = recommend_item(df_svd_preds, rowUser, df_users, df_ratings, 10)    # 리스트 반환
        predictTop5 = recommend_item(df_svd_preds, rowUser, df_users, df_ratings, 10)    # 리스트 반환
        
        recommendUserTop1.append(predictTop1)
        recommendUserTop3.append(predictTop3)
        recommendUserTop5.append(predictTop5)
        i += 1

    dfDealTop1['prediction'] = recommendUserTop1
    dfDealTop3['prediction'] = recommendUserTop3
    dfDealTop5['prediction'] = recommendUserTop5


    accuracy = 0
    # accuracy 비교
    while accuracy < 365:
        # 현재 행
        rowTakerTop1 = dfDealTop1['taker'].loc[accuracy]
        rowTakerTop3 = dfDealTop3['taker'].loc[accuracy]
        rowTakerTop5 = dfDealTop5['taker'].loc[accuracy]

        rowPredictionTop1 = dfDealTop1['prediction'].loc[accuracy]
        rowPredictionTop3 = dfDealTop3['prediction'].loc[accuracy]
        rowPredictionTop5 = dfDealTop5['prediction'].loc[accuracy]
        
        if rowTakerTop1 in rowPredictionTop1:
            dfDealTop1['accuracy'].loc[accuracy] = 1
        else:
            dfDealTop1['accuracy'].loc[accuracy] = 0

        if rowTakerTop3 in rowPredictionTop3:
            dfDealTop3['accuracy'].loc[accuracy] = 1
        else:
            dfDealTop3['accuracy'].loc[accuracy] = 0

        if rowTakerTop5 in rowPredictionTop5:
            dfDealTop5['accuracy'].loc[accuracy] = 1
        else:
            dfDealTop5['accuracy'].loc[accuracy] = 0

        accuracy += 1

    # 결과값 데이터프레임 만들기

    # accuracy 평균
    percentTop1 = dfDealTop1['accuracy'].mean()
    percentTop3 = dfDealTop3['accuracy'].mean()
    percentTop5 = dfDealTop5['accuracy'].mean()

    dfOutput = pd.DataFrame({
        'accuracyTop1': percentTop1,
        'accuarcyTop3': percentTop3,
        'accuracyTop5': percentTop5
        }, index=[0])
    

    # dataframe -> excel 변환
    with pd.ExcelWriter('matrixbased_PRS.xlsx') as writer:
        dfDealTop1.to_excel(writer, sheet_name='Top1')
        dfDealTop3.to_excel(writer, sheet_name='Top3')
        dfDealTop5.to_excel(writer, sheet_name='Top5')
        dfOutput.to_excel(writer, sheet_name='accuracy')





predictMatrixbased()
