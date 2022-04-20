from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse.linalg import svds

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings

from sklearn.metrics import confusion_matrix
warnings.filterwarnings("ignore")



#0407

# 데이터준비
ratings = "C:\\Users\\kkbo5\\Documents\GitHub\Coordinating\\ratings\\ratings.xlsx"
users = "C:\\Users\\kkbo5\\Desktop\\AIIP_Lab\\smart_coordinating\\user-item.xlsx"

# 0: Pt-PRS, 1: DPt-PRS, 2: PRS
df_ratings = pd.read_excel(ratings, sheet_name=2)
df_users = pd.read_excel(users, sheet_name=0)


df_ratings.drop('propertyId', axis=1, inplace=True)
print(df_ratings)

user_item_rating = pd.merge(df_ratings, df_users, on="itemId")
print(user_item_rating.head(2))


# item_user_rating = user_item_rating.pivot_table('Pt_PRS', index="username", columns='userId')   
user_item_rating = user_item_rating.pivot_table('PRS', index="userId", columns="username")  # 아이템 기반 협업필터링


# null값 채우기
user_item_rating.fillna(0, inplace=True)
print(user_item_rating.head())



# 코사인 유사도 측정
based_collabor = cosine_similarity(user_item_rating)
print(based_collabor)

# 유사도 값을 가진 데이터프레임 출력 
based_collabor = pd.DataFrame(data = based_collabor, 
                              index =user_item_rating.index, 
                              columns=user_item_rating.index)


print('=====based_collabor====')
print(based_collabor.head())


# 유사도가 가까울수록 1에 가까운 값 출력, 자기자신 = 1
def get_based_collabor(userId, head):
    # 유사도 Top5
    #return based_collabor[userId].sort_values(ascending=False)[:6]
    # 자기자신 제외
    predict = based_collabor[userId].sort_values(ascending=False)[1:head+1]
    prediction = predict.index.to_list()
    return prediction


# 결과값 출력
# print(get_based_collabor(22))

for i in range(23,58):
    print("==========")
    print(i)
    print(get_based_collabor(i, 3))