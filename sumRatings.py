from re import I
from xml.sax.handler import property_interning_dict
import pandas as pd
from openpyxl import load_workbook
import openpyxl as xl
import numpy as np
from sigmoid import noneSigmoid
import os


ratings_1 = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_1.xlsx"
ratings_2 = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_2.xlsx"
ratings_3 = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_3.xlsx"
ratings_4 = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_4.xlsx"
ratings_5 = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_5.xlsx"
ratings_6 = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_6.xlsx"
ratings_7 = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_7.xlsx"
ratings_8 = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_8.xlsx"
ratings_9 = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_9.xlsx"
ratings_10 = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_10.xlsx"


'''
for i in range(1,11):
    f'ratings_{i}_Pt_PRS' = 
    f'ratings_{i}_DPt_PRS' = 
    f'ratings_{i}_PRS' =
'''

for i in range(1,11):
    excel_path = f"C:\\Users\\kkbo5\\Documents\\GitHub\\Coordinating\\ratings\\ratings_{i}.xlsx"

    globals()[f'ratings_{i}_Pt_PRS'] = pd.read_excel(excel_path, sheet_name=0)
    globals()[f'ratings_{i}_DPt_PRS'] = pd.read_excel(excel_path, sheet_name=1)
    globals()[f'ratings_{i}_PRS'] = pd.read_excel(excel_path, sheet_name=2)


ratings_Pt_PRS = pd.concat([
    ratings_1_Pt_PRS,
    ratings_2_Pt_PRS,
    ratings_3_Pt_PRS,
    ratings_4_Pt_PRS,
    ratings_5_Pt_PRS,
    ratings_6_Pt_PRS,
    ratings_7_Pt_PRS,
    ratings_8_Pt_PRS,
    ratings_9_Pt_PRS,
    ratings_10_Pt_PRS
])


ratings_DPt_PRS = pd.concat([
    ratings_1_DPt_PRS,
    ratings_2_DPt_PRS,
    ratings_3_DPt_PRS,
    ratings_4_DPt_PRS,
    ratings_5_DPt_PRS,
    ratings_6_DPt_PRS,
    ratings_7_DPt_PRS,
    ratings_8_DPt_PRS,
    ratings_9_DPt_PRS,
    ratings_10_DPt_PRS
])

ratings_PRS = pd.concat([
    ratings_1_PRS,
    ratings_2_PRS,
    ratings_3_PRS,
    ratings_4_PRS,
    ratings_5_PRS,
    ratings_6_PRS,
    ratings_7_PRS,
    ratings_8_PRS,
    ratings_9_PRS,
    ratings_10_PRS
])

ratings = pd.ExcelWriter('ratings.xlsx', engine='openpyxl')
ratings_Pt_PRS.to_excel(ratings, sheet_name="Pt-PRS")
ratings_DPt_PRS.to_excel(ratings, sheet_name="DPt-PRS")
ratings_PRS.to_excel(ratings, sheet_name="Pt-PRS+DPt-PRS")
ratings.save()