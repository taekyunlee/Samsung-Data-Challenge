import pandas as pd 
import numpy as np 
from pandas import DataFrame , Series
import mglearn
from sklearn.ensemble import RandomForestRegressor 
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier  
from os import chdir

chdir('D:/samsung_data_challenge/')
    
ta = pd.read_csv('Train_교통사망사고정보(12.1~17.6).csv', engine='python')
test = pd.read_csv('test_kor.csv', engine='python')
result = pd.read_csv('result_kor.csv', engine='python')

ta1 = ta.drop(['발생년','발생년월일시','발생분','사고유형','법규위반_대분류','발생위치X_UTMK','발생위치Y_UTMK','위도','경도','당사자종별_1당','당사자종별_2당'] ,  axis=1) 
ta1 = ta1.drop(ta1[ta1['사망자수'] >=5].index)
ta1 = ta1.drop(ta1[ta1['사상자수'] >=15].index)
ta1 = ta1.drop(ta1[ta1['부상신고자수'] >=4].index)
ta1 = ta1.drop(ta1[ta1['경상자수'] >=10].index)
ta1 = ta1.drop(ta1[ta1['중상자수'] >=10].index)


lin = LinearRegression() 
forest = RandomForestClassifier(n_estimators = 100 , random_state =2) 
ranr = RandomForestRegressor()
                           
for i in range(len(test.index)) :                                                   
    if (np.isnan(test.at[ i , '사망자수' ]) == True) : 
        if (np.isnan(test.loc[ i , '사상자수' ]) == False) : 
            lin.fit(ta1[['사상자수']].values , ta1[['사망자수']].values)
            test.loc[i,'사망자수'] = float(lin.predict(test.loc[i,'사상자수']))

        elif (str(test.loc[ i , '발생지시군구' ]) != 'nan') & (str(test.loc[ i , '사고유형_대분류' ]) != 'nan')  :
            lin.fit(pd.get_dummies(ta1[['발생지시군구','사고유형_대분류']]).values , ta1[['사망자수']].values)
            test.loc[i,'사망자수'] = float(lin.predict(pd.get_dummies(pd.concat([ta1[['발생지시군구','사고유형_대분류']],test[['발생지시군구','사고유형_대분류']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1)))                                  

        elif (str(test.loc[ i , '도로형태' ]) != 'nan') & (str(test.loc[ i , '사고유형_중분류' ]) != 'nan')  :
            lin.fit(pd.get_dummies(ta1[['도로형태','사고유형_중분류']]).values , ta1[['사망자수']].values)
            test.loc[i,'사망자수'] = float(lin.predict(pd.get_dummies(pd.concat([ta1[['도로형태','사고유형_중분류']],test[['도로형태','사고유형_중분류']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1)))

        elif (np.isnan(test.loc[ i , '중상자수' ]) == False) & (np.isnan(test.loc[ i , '경상자수' ]) == False) & (np.isnan(test.loc[ i , '부상신고자수' ]) == False)  :
            lin.fit(ta1[['중상자수','경상자수','부상신고자수']].values , ta1[['사망자수']].values)
            test.loc[i,'사망자수'] = float(lin.predict(test.loc[i,['중상자수','경상자수','부상신고자수']].values.reshape(1,-1)))

    if (np.isnan(test.loc[ i , '부상신고자수' ]) == True) : 
        if (np.isnan(test.loc[ i , '사상자수' ]) == False) : 
            if (np.isnan(test.loc[ i , '중상자수' ]) == False) & (np.isnan(test.loc[ i , '경상자수' ]) == False)  : 
                lin.fit(ta1[['사상자수','사망자수','중상자수','경상자수']].values , ta1[['부상신고자수']].values)
                test.loc[i,'부상신고자수'] = float(lin.predict(test.loc[i,['사상자수','사망자수','중상자수','경상자수']].values.reshape(1,-1)))

            elif (np.isnan(test.loc[ i , '경상자수' ]) == False) :    
                lin.fit(ta1[['사상자수','사망자수','경상자수']].values , ta1[['부상신고자수']].values)
                test.loc[i,'부상신고자수'] = float(lin.predict(test.loc[i,['사상자수','사망자수','경상자수']].values.reshape(1,-1)))

            elif (np.isnan(test.loc[ i , '중상자수' ]) == False): 
                lin.fit(ta1[['사상자수','사망자수','중상자수']].values , ta1[['부상신고자수']].values)
                test.loc[i,'부상신고자수'] = float(lin.predict(test.loc[i,['사상자수','사망자수','중상자수']].values.reshape(1,-1))) 
            else : 
                lin.fit(ta1[['사상자수','사망자수']].values , ta1[['부상신고자수']].values)
                test.loc[i,'부상신고자수'] = float(lin.predict(test.loc[i,['사상자수','사망자수']].values.reshape(1,-1))) 
           

        elif (np.isnan(test.loc[ i , '중상자수' ]) == False) & (np.isnan(test.loc[ i , '경상자수' ]) == False) :                                    
            lin.fit(ta1[['사망자수','중상자수','경상자수']].values , ta1[['부상신고자수']].values)
            test.loc[i,'부상신고자수'] = float(lin.predict(test.loc[i,['사망자수','중상자수','경상자수']].values.reshape(1,-1))) 

        elif (np.isnan(test.loc[ i , '중상자수' ]) == False) :                                    
            lin.fit(ta1[['사망자수','중상자수']].values , ta1[['부상신고자수']].values)
            test.loc[i,'부상신고자수'] = float(lin.predict(test.loc[i,['사망자수','중상자수']].values.reshape(1,-1)))   

        elif (np.isnan(test.loc[ i , '경상자수' ]) == False) :                                   
            lin.fit(ta1[['사망자수','경상자수']].values , ta1[['부상신고자수']].values)
            test.loc[i,'부상신고자수'] = float(lin.predict(test.loc[i,['사망자수','경상자수']].values.reshape(1,-1)))        
        else : 
            lin.fit(ta1[['사망자수']].values , ta1[['부상신고자수']].values)
            test.loc[i,'부상신고자수'] = float(lin.predict(test.loc[i,['사망자수']].values.reshape(1,-1)))                   

    if (np.isnan(test.loc[ i , '경상자수' ]) == True) : 
        if (np.isnan(test.loc[ i , '사상자수' ]) == False) :
            if (np.isnan(test.loc[ i , '중상자수' ]) == False) & (np.isnan(test.loc[ i , '부상신고자수' ]) == False) :
                lin.fit(ta1[['사상자수','사망자수','부상신고자수','중상자수']].values , ta1[['경상자수']].values)
                test.loc[i,'경상자수'] = float(lin.predict(test.loc[i,['사상자수','사망자수','부상신고자수','중상자수']].values.reshape(1,-1)))  

            elif (np.isnan(test.loc[ i , '중상자수' ]) == False) :
                lin.fit(ta1[['사상자수','사망자수','중상자수']].values , ta1[['경상자수']].values)
                test.loc[i,'경상자수'] = float(lin.predict(test.loc[i,['사상자수','사망자수','중상자수']].values.reshape(1,-1))) 

            elif (np.isnan(test.loc[ i , '부상신고자수' ]) == False) :
                ranr.fit(ta1[['사상자수','사망자수','부상신고자수']].values , ta1[['경상자수']].values.ravel())
                test.loc[i,'경상자수'] = float(ranr.predict(test.loc[i,['사상자수','사망자수','부상신고자수']].values.reshape(1,-1)))  
            
             
        elif (np.isnan(test.loc[ i , '중상자수' ]) == False) :
            lin.fit(ta1[['사망자수','부상신고자수','중상자수']].values , ta1[['경상자수']].values)
            test.loc[i,'경상자수'] = float(lin.predict(test.loc[i,['사망자수','부상신고자수','중상자수']].values.reshape(1,-1)))
        else :
            ranr.fit(ta1[['사망자수','부상신고자수']].values , ta1[['경상자수']].values.ravel())
            test.loc[i,'경상자수'] = float(ranr.predict(test.loc[i,['사망자수','부상신고자수']].values.reshape(1,-1)))
    
    if (np.isnan(test.loc[ i , '중상자수' ]) == True) :               
        if (np.isnan(test.loc[ i , '사상자수' ]) == False) :  
            if (np.isnan(test.loc[ i , '경상자수' ]) == False) & (np.isnan(test.loc[ i , '부상신고자수' ]) == False) :
                lin.fit(ta1[['사상자수','사망자수','부상신고자수','경상자수']].values , ta1[['중상자수']].values)
                test.loc[i,'중상자수'] = float(lin.predict(test.loc[i,['사상자수','사망자수','부상신고자수','경상자수']].values.reshape(1,-1)))  
              
        else :                                                                                                                                                                                       
            ranr.fit(ta1[['사망자수','부상신고자수','경상자수']].values , ta1[['중상자수']].values.ravel())
            test.loc[i,'중상자수'] = float(ranr.predict(test.loc[i,['사망자수','부상신고자수','경상자수']].values.reshape(1,-1)))
                   
    if (np.isnan(test.loc[ i , '사상자수' ]) == True) :
        lin.fit(ta1[['사망자수','부상신고자수','경상자수','중상자수']].values , ta1[['사상자수']].values)                           
        test.loc[i,'사상자수'] = float(lin.predict(test.loc[i,['사망자수','부상신고자수','경상자수','중상자수']].values.reshape(1,-1)))   
    
    if (str(test.loc[ i , '법규위반' ]) == 'nan') :
        forest.fit( ta1[['사상자수']].values , ta1[['법규위반']].values.ravel() )
        test.loc[i,'법규위반'] = forest.predict(pd.get_dummies(pd.concat([ta1[['사상자수']],test[['사상자수']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
    
    if (str(test.loc[ i , '도로형태_대분류' ]) == 'nan') :
        if (str(test.loc[ i , '도로형태' ]) != 'nan') :
            forest.fit( pd.get_dummies(ta1[['도로형태']]).values , ta1[['도로형태_대분류']].values.ravel() )
            test.loc[i,'도로형태_대분류'] = forest.predict(pd.get_dummies(pd.concat([ta1[['도로형태']],test[['도로형태']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
        else : 
            forest.fit( pd.get_dummies(ta1[['사상자수','법규위반']]).values , ta1[['도로형태_대분류']].values.ravel() )
            test.loc[i,'도로형태_대분류'] = forest.predict(pd.get_dummies(pd.concat([ta1[['사상자수','법규위반']],test[['사상자수','법규위반']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
     
    if (str(test.loc[ i , '도로형태' ]) == 'nan') :
        forest.fit( pd.get_dummies(ta1[['사상자수','법규위반','도로형태_대분류']]).values , ta1[['도로형태']].values.ravel() )
        test.loc[i,'도로형태'] = forest.predict(pd.get_dummies(pd.concat([ta1[['사상자수','법규위반','도로형태_대분류']],test[['사상자수','법규위반','도로형태_대분류']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
         
    if (str(test.loc[ i , '당사자종별_2당_대분류' ]) == 'nan') :
        if (str(test.loc[ i , '사고유형_대분류' ]) != 'nan') :
            forest.fit( pd.get_dummies(ta1[['중상자수','법규위반','도로형태','사고유형_대분류']]).values , ta1[['당사자종별_2당_대분류']].values.ravel() )
            test.loc[i,'당사자종별_2당_대분류'] = forest.predict(pd.get_dummies(pd.concat([ta1[['중상자수','법규위반','도로형태','사고유형_대분류']],test[['중상자수','법규위반','도로형태','사고유형_대분류']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
    
        elif (str(test.loc[ i , '사고유형_중분류' ]) != 'nan') :  
            forest.fit( pd.get_dummies(ta1[['중상자수','법규위반','도로형태','사고유형_중분류']]).values , ta1[['당사자종별_2당_대분류']].values.ravel() )
            test.loc[i,'당사자종별_2당_대분류'] = forest.predict(pd.get_dummies(pd.concat([ta1[['중상자수','법규위반','도로형태','사고유형_중분류']],test[['중상자수','법규위반','도로형태','사고유형_중분류']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))

        elif (str(test.loc[ i , '당사자종별_1당_대분류' ]) != 'nan') :
            forest.fit( pd.get_dummies(ta1[['중상자수','법규위반','도로형태','당사자종별_1당_대분류']]).values , ta1[['당사자종별_2당_대분류']].values.ravel() )
            test.loc[i,'당사자종별_2당_대분류'] = forest.predict(pd.get_dummies(pd.concat([ta1[['중상자수','법규위반','도로형태','당사자종별_1당_대분류']],test[['중상자수','법규위반','도로형태','당사자종별_1당_대분류']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
        else : 
            forest.fit( pd.get_dummies(ta1[['중상자수','법규위반','도로형태']]).values , ta1[['당사자종별_2당_대분류']].values.ravel() )
            test.loc[i,'당사자종별_2당_대분류'] = forest.predict(pd.get_dummies(pd.concat([ta1[['중상자수','법규위반','도로형태']],test[['중상자수','법규위반','도로형태']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
    
    if (str(test.loc[ i , '사고유형_대분류' ]) == 'nan') :
        forest.fit( pd.get_dummies(ta1[['당사자종별_2당_대분류']]).values , ta1[['사고유형_대분류']].values.ravel() )
        test.loc[i,'사고유형_대분류'] = forest.predict(pd.get_dummies(pd.concat([ta1[['당사자종별_2당_대분류']],test[['당사자종별_2당_대분류']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
    
    if (str(test.loc[ i , '사고유형_중분류' ]) == 'nan') :
        forest.fit( pd.get_dummies(ta1[['사고유형_대분류','당사자종별_2당_대분류','법규위반']]).values , ta1[['사고유형_중분류']].values.ravel() )
        test.loc[i,'사고유형_중분류'] = forest.predict(pd.get_dummies(pd.concat([ta1[['사고유형_대분류','당사자종별_2당_대분류','법규위반']],test[['사고유형_대분류','당사자종별_2당_대분류','법규위반']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
    
    if (str(test.loc[ i , '발생지시도' ]) == 'nan') :
        if (str(test.loc[ i , '발생지시군구' ]) != 'nan') :       
            forest.fit( pd.get_dummies(ta1[['발생지시군구']]).values , ta1[['발생지시도']].values.ravel() )
            test.loc[i,'발생지시도'] = forest.predict(pd.get_dummies(pd.concat([ta1[['발생지시군구']],test[['발생지시군구']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
        else : 
            forest.fit( pd.get_dummies(ta1[['법규위반','사고유형_중분류','당사자종별_1당_대분류','당사자종별_2당_대분류']]).values , ta1[['발생지시도']].values.ravel() )
            test.loc[i,'발생지시도'] = forest.predict(pd.get_dummies(pd.concat([ta1[['법규위반','사고유형_중분류','당사자종별_1당_대분류','당사자종별_2당_대분류']],test[['법규위반','사고유형_중분류','당사자종별_1당_대분류','당사자종별_2당_대분류']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
    
    if (str(test.loc[ i , '발생지시군구' ]) == 'nan') :
        forest.fit( pd.get_dummies(ta1[['발생지시도']]).values , ta1[['발생지시군구']].values.ravel() )
        test.loc[i,'발생지시군구' ] = forest.predict(pd.get_dummies(pd.concat([ta1[['발생지시도']],test[['발생지시도']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))

    if (str(test.loc[ i , '당사자종별_1당_대분류' ]) == 'nan') :
        forest.fit( pd.get_dummies(ta1[['당사자종별_2당_대분류','법규위반','사상자수','발생지시도']]).values , ta1[['당사자종별_1당_대분류']].values.ravel() )
        test.loc[i,'당사자종별_1당_대분류'] = forest.predict(pd.get_dummies(pd.concat([ta1[['당사자종별_2당_대분류','법규위반','사상자수','발생지시도']],test[['당사자종별_2당_대분류','법규위반','사상자수','발생지시도']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
    
    if (str(test.loc[ i , '주야' ]) == 'nan') :
        forest.fit( pd.get_dummies(ta1[['법규위반','당사자종별_1당_대분류']]).values , ta1[['주야']].values.ravel() )
        test.loc[i,'주야'] = forest.predict(pd.get_dummies(pd.concat([ta1[['법규위반','당사자종별_1당_대분류']],test[['법규위반','당사자종별_1당_대분류']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
        
    if (str(test.loc[ i , '요일' ]) == 'nan') :
        forest.fit( pd.get_dummies(ta1[['주야', '사망자수', '사상자수', '중상자수', '경상자수', '부상신고자수', '발생지시도', '발생지시군구','사고유형_대분류', '사고유형_중분류', '법규위반', '도로형태_대분류', '도로형태', '당사자종별_1당_대분류','당사자종별_2당_대분류']]).values , ta1[['요일']].values.ravel() )
        test.loc[i,'요일'] = forest.predict(pd.get_dummies(pd.concat([ta1[['주야', '사망자수', '사상자수', '중상자수', '경상자수', '부상신고자수', '발생지시도', '발생지시군구','사고유형_대분류', '사고유형_중분류', '법규위반', '도로형태_대분류', '도로형태', '당사자종별_1당_대분류','당사자종별_2당_대분류']],test[['주야', '사망자수', '사상자수', '중상자수', '경상자수', '부상신고자수', '발생지시도', '발생지시군구','사고유형_대분류', '사고유형_중분류', '법규위반', '도로형태_대분류', '도로형태', '당사자종별_1당_대분류','당사자종별_2당_대분류']]] , axis =0).reset_index().drop(['index'] , axis = 1)).loc[i + 24922, ].values.reshape(1,-1))
    print(str(int(i/len(test)*100)) + '% 진행') 



                
for i in range(len(result.index)) :
    if   result.loc[i, '열'] == 'A' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '주야' ]
    elif result.loc[i, '열'] == 'B' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '요일' ]
    elif result.loc[i, '열'] == 'C' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '사망자수' ]
    elif result.loc[i, '열'] == 'D' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '사상자수' ]
    elif result.loc[i, '열'] == 'E' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '중상자수' ]
    elif result.loc[i, '열'] == 'F' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '경상자수' ]
    elif result.loc[i, '열'] == 'G' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '부상신고자수' ]
    elif result.loc[i, '열'] == 'H' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '발생지시도' ]
    elif result.loc[i, '열'] == 'I' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '발생지시군구' ]
    elif result.loc[i, '열'] == 'J' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '사고유형_대분류' ]
    elif result.loc[i, '열'] == 'K' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '사고유형_중분류' ]
    elif result.loc[i, '열'] == 'L' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '법규위반' ]
    elif result.loc[i, '열'] == 'M' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '도로형태_대분류' ]
    elif result.loc[i, '열'] == 'N' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '도로형태' ]
    elif result.loc[i, '열'] == 'O' :
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '당사자종별_1당_대분류' ]
    else :  
        result.loc[i, '값'] = test.loc[ result.loc[i,'행'] - 2 ,  '당사자종별_2당_대분류' ]
    
result.to_csv('result.csv' , index =False, encoding = 'euc_kr')

print('완료')

