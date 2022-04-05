# import tensorflow as tf
from re import I
import pandas as pd
from openpyxl import load_workbook
import openpyxl as xl
import numpy as np
from sigmoid import noneSigmoid


# Sd, Se값만 추출

# 데이터준비
df = "C:\\Users\\kkbo5\\Desktop\\AIIP_Lab\\smart_coordinating\\testData4.xlsx"



class Recommend:
    
    def __init__(self, inputUser, inputService, inputProperty):
        self.inputUser = inputUser
        self.inputService = inputService
        self.inputProperty = inputProperty



    # Sd값 구하기
    def resultSd(self):
        inputUser = self.inputUser
        
        targetGiveTB = pd.read_excel(df, sheet_name=3)
        # userID -> userID 추출하기
        targetUser = targetGiveTB.loc[targetGiveTB['userID'] == inputUser]
        colUserID = targetUser['userID'].values.tolist()
        userID = list(set(colUserID))
        print(userID, type(userID))     #[1] <class 'list'>
        userID = int(userID[0])

        # inputUser 가 포함된 거래 출력
        dealTB = pd.read_excel(df, sheet_name=2)
        partnerTB = dealTB.loc[(dealTB['giver'] == userID) | (dealTB['taker'] == userID)]
        # print(partnerTB)

        colGiver = partnerTB['giver'].values.tolist()
        colTaker = partnerTB['taker'].values.tolist()

        result = colGiver + colTaker
        # print(result)

        # userID가 거래한 횟수 카운트
        count={}
        lists = result
        for i in lists:
            try: count[i] += 1
            except: count[i]=1
        # del count[1]
        # print(count)

        userSd = list(count)
        frequency = list(count.values())
        # print('userID : ', userSd, 'frequency : ', frequency)


        valueSd = []
        # userID 리스트 요소만큼 반복
        for i in frequency:
            result = noneSigmoid(i)
            valueSd.append(result)

        scoreSdTB = pd.DataFrame({'user': userSd, 
                          'frequency': frequency,
                          'Sd': valueSd
                        })

        return scoreSdTB

    
    # Se값 구하기
    def resultSe(self):
        inputProperty = self.inputProperty
        
        dealTB = pd.read_excel(df, sheet_name=2)
        
        # inputProperty와 같은 property 거래만 출력
        propertyTB = dealTB.loc[dealTB['propertyID'] == inputProperty]
        colPropertyUserG = propertyTB['giver'].values.tolist()
        coltPropertyUserT = propertyTB['taker'].values.tolist()
        colPropertyUser = colPropertyUserG + coltPropertyUserT

        # print(colPropertyUser)

        # userID가 거래한 횟수 카운트 (frequency)
        recentCount = {}
        for col in colPropertyUser:
            try: recentCount[col] += 1
            except: recentCount[col] = 1

        recentF = list(recentCount.values())
        recentUser = list(recentCount.keys())

        
        valueSe = []
        # userID 리스트 요소만큼 반복
        for r in recentF:
            result = noneSigmoid(r)
            valueSe.append(result)

        scoreSeTB = pd.DataFrame({'user': recentUser,
                            'recent': recentF,
                            'Se': valueSe
                            })
        
        return scoreSeTB
        
    
    # 최종 Score Excel 변환
    def writeExcel(self):
        scoreSdTB = Recommend.resultSd(self)
        scoreSeTB = Recommend.resultSe(self)

        scoreTB = pd.merge(scoreSeTB, scoreSdTB, how='outer', on='user')
        # NaN -> 0으로 변경
        scoreTB = scoreTB.fillna(0)


        # 점수 합산
        sumTB = scoreTB[['Sd', 'Se']]
        print(sumTB)
        result1 = sumTB.sum(axis=1)
        sum_list = result1.to_list()

        scoreTB['score'] = sum_list
        # 내림차순 정렬, 상위 3개 출력 .head(3)
        scoreTB = scoreTB.sort_values(by=['score'], ascending=False)
        print('최종 scoreTB입니다')
        print(scoreTB)

        # dataframe excel 변환
        with pd.ExcelWriter('output.xlsx') as writer:
            # scoreSdTB.to_excel(writer, sheet_name='SdTB')
            # scoreSeTB.to_excel(writer, sheet_name='SeTB')
            scoreTB.to_excel(writer, sheet_name='scoreTB')
        
        return scoreTB

    

'''
# 추천받을 user, service, property 입력 (로그인유저)
inputUser = int(input())
inputService = input()
inputProperty = int(input())

input = Recommend(inputUser, inputService, inputProperty)
resultSd = input.resultSd()
resultSe = input.resultSe()
result = Recommend.writeExcel(input)
'''

'''
while i < 58:
    while prop < 11:
        inputUser = i
        inputService = "give"
        inputProperty = prop

        input = Recommend(inputUser, inputService, inputProperty)
        resultSd = input.resultSd()
        resultSe = input.resultSe()
        resultScore = input.writeExcel()
        
        prop += 1

    i += 1
'''

# user에 대한 property 별 scoredf
def userProperty(userId):

    output = ['']
    for i in range(1,11):
        inputUser = userId
        # inputService = input()
        inputService = "give"
        inputProperty = i

        input = Recommend(inputUser, inputService, inputProperty)
        resultSd = input.resultSd()
        resultSe = input.resultSe()
        result = Recommend.writeExcel(input)    #score 데이터프레임 반환
        output.append(result)

    print(type(output[1]))      #DataFrame

    globals()[f'outputUser{userId}'] = pd.ExcelWriter(f'outputUser{userId}.xlsx', engine='openpyxl')
    
    # sheet 변수 생성
    i = 1
    while i<11:
        globals()['prop_{}'.format(i)] = output[i]
        i += 1

    prop_1.to_excel(globals()[f'outputUser{userId}'],sheet_name="prop_1") 
    prop_2.to_excel(globals()[f'outputUser{userId}'],sheet_name="prop_2") 
    prop_3.to_excel(globals()[f'outputUser{userId}'],sheet_name="prop_3") 
    prop_4.to_excel(globals()[f'outputUser{userId}'],sheet_name="prop_4") 
    prop_5.to_excel(globals()[f'outputUser{userId}'],sheet_name="prop_5") 
    prop_6.to_excel(globals()[f'outputUser{userId}'],sheet_name="prop_6") 
    prop_7.to_excel(globals()[f'outputUser{userId}'],sheet_name="prop_7") 
    prop_8.to_excel(globals()[f'outputUser{userId}'],sheet_name="prop_8") 
    prop_9.to_excel(globals()[f'outputUser{userId}'],sheet_name="prop_9") 
    prop_10.to_excel(globals()[f'outputUser{userId}'],sheet_name="prop_10")

    globals()[f'outputUser{userId}'].save()


# userId 입력 > 해당 user의 데이터시트 생성
result = userProperty(1)