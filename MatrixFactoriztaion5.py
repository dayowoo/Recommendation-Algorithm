from sklearn.decomposition import TruncatedSVD
from scipy.sparse.linalg import svds

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings("ignore")



#0215

# 데이터준비
ratings = "C:\\Users\\kkbo5\\Documents\GitHub\Coordinating\\ratings\\ratings.xlsx"
users = "C:\\Users\\kkbo5\\Desktop\\AIIP_Lab\\smart_coordinating\\user-item.xlsx"


df_ratings = pd.read_excel(ratings, sheet_name=2)
df_users = pd.read_excel(users, sheet_name=0)


# values : Pt_PRS, DPt_PRS, PRS
def matrixFactorization(values):
    
    # 사용자-item 평점 데이터
    df_user_item_ratings = df_ratings.pivot_table(
        index='userId',      # row
        columns='itemId',     
        values=values        # 바꿔줘야함
    ).fillna(0)
    print(df_user_item_ratings.head())

    # pivot_table 값을 numpy matrix(행렬)로 만듦
    matrix = df_user_item_ratings.to_numpy()


    # 사용자의 평균 평점
    user_ratings_mean = np.mean(matrix, axis=1)
    matrix_user_mean = matrix - user_ratings_mean.reshape(-1,1)
    print(matrix)

    print(pd.DataFrame(matrix_user_mean, columns = df_user_item_ratings.columns).head())


    # scipy에서 제공해주는 svd.  
    # U 행렬, sigma 행렬, V 전치 행렬을 반환.
    U, sigma, Vt = svds(matrix_user_mean, k = 12)
    print(U.shape)
    print(sigma.shape)
    print(Vt.shape)

    # 0이 포함된 대칭행렬로 변환
    sigma = np.diag(sigma)

    # U, Sigma, Vt의 내적을 수행하면, 다시 원본 행렬로 복원이 된다. 
    # 거기에 + 사용자 평균 rating을 적용한다. 
    svd_user_predicted_ratings = np.dot(np.dot(U, sigma), Vt) + user_ratings_mean.reshape(-1, 1)

    df_svd_preds = pd.DataFrame(svd_user_predicted_ratings, columns = df_user_item_ratings.columns)
    print(df_svd_preds.head())
    return df_svd_preds




'''
1. userId에 SVD로 나온 결과의 item 평점이 가장 높은 데이터 순으로 정렬
2. 이미 평가한 item(=user)도 포함. (재거래 가능하기 때문에) 
'''
def recommend_item(df_svd_preds, user_id, users_df, ratings_df, num_recommendations=5):
    
    #현재는 index로 적용이 되어있으므로 user_id - 1을 해야함.
    user_row_number = user_id - 1 
    
    # 최종적으로 만든 predict_df에서 사용자 index에 따라 데이터 정렬 -> PRS 높은 순으로 정렬 됌
    sorted_user_predictions = df_svd_preds.iloc[user_row_number].sort_values(ascending=False)
    
    # 원본 평점 데이터에서 user id에 해당하는 데이터를 뽑아낸다. 
    user_data = ratings_df[ratings_df.userId == user_id]
    
    # 위에서 뽑은 user_data와 원본 itemlist(=userList) 데이터를 합친다. 
    user_history = user_data.merge(users_df, on = 'itemId').sort_values(['PRS'], ascending=False)
    
    # 원본 영화 데이터에서 사용자가 본 영화 데이터를 제외한 데이터를 추출
    # recommendations = users_df[~users_df['itemId'].isin(user_history['itemId'])]
    recommendations = user_history
    # 사용자의 영화 평점이 높은 순으로 정렬된 데이터와 위 recommendations을 합친다. 
    recommendations = recommendations.merge( pd.DataFrame(sorted_user_predictions).reset_index(), on ='itemId')
    
    # 컬럼 이름 바꾸고 정렬해서 return
    recommendations = recommendations.rename(columns = {user_row_number: 'Predictions'}).sort_values('Predictions', ascending = False).iloc[:num_recommendations, :]

    # 자기 자신 제외
    # df5 = df.loc[~df['name'].isin(targets)]
    user = [user_id]
    recommendation = recommendations.loc[~recommendations['itemId'].isin(user)]   
    user_history = user_history.loc[~user_history['itemId'].isin(user)] 

    # 중복 값 제거
    user_history = user_history.drop_duplicates(['itemId'], keep='first')
    recommendation = recommendation.drop_duplicates(['itemId'], keep='first')

    user_history = user_history.head(5)
    recommendation = recommendation.head(5)

    # 리스트 변환
    user_history = user_history['itemId'].to_list()
    # recommendation = recommendation['userId'].to_list              
    return user_history




# 이미 이루어진 데이터 , 예측
# df_svd_preds, user_id, users_df, ratings_df, num_recommendations=5
'''
already_rated, predictions = recommend_item(df_svd_preds, 1, df_users, df_ratings, 10)
print(already_rated.head(10))
print(predictions)
'''


df_svd_preds = matrixFactorization('PRS')

# i = userId
for i in range(1,58):
    # prediction
    already_rated = recommend_item(df_svd_preds, i, df_users, df_ratings, 10)

    print("===================")
    print(i)
    print(already_rated)
    # print(predictions.head(5))