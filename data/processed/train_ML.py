from data_cleaning import prep_raw_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score,mean_absolute_error,root_mean_squared_error
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor,GradientBoostingRegressor
import pandas as pd
import numpy as np
from sklearn.model_selection import GridSearchCV
import joblib
if __name__=='__main__':
    df=prep_raw_data(path='../raw/apartments_pl_2024_06.csv',path_shp='../raw/dzielnice_Warszawy/dzielnice_Warszawy.shp')
    y=df['price']
    X=df.drop(columns=['price','district'])
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)

    #We are going to compare diffetent attitudes to this problem:
    #1 Linear Regression
    print("======================================Linear Regression=====================================")
    model=LinearRegression()
    reg=model.fit(X_train, y_train)
    y_pred=reg.predict(X_test)
    r2=r2_score(y_test,y_pred)
    MAE=mean_absolute_error(y_test,y_pred)
    RMSE=root_mean_squared_error(y_test,y_pred)
    print(f'Metrics: R2={r2}, MAE: {MAE}, RMSE: {RMSE}')
    #First model is Linear Regression Model from Scikit-learn. Model achieved R^2 score of 0.813 what is very decent score, it explained 81.3% of variance in estate prices. MAE(Mean absolute error) is 146628PLN, it says that prediction differ from actual price by about 147k PLN, what is significant value when range of prices is 500k PLN and 3000k PLN. RMSE(Root mean square error) is 205838 PLN, it is greater value that MAE, so it suggests that model occasionally makes larger prediction errors, as RMSE punishes larger faults more heavily than MAE
    plt.scatter(y_test, y_pred, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()],[y_test.min(), y_test.max()],color="red",linestyle="--")
    plt.xlabel("Actual price")
    plt.ylabel("Predicted price")
    plt.title("Actual vs Predicted(Linear Regression)")
    plt.show()

    #2 Random Forest Regressor
    print("====================================Random Forest Regressor===================================")
    model2=RandomForestRegressor(random_state=42)
    reg2=model2.fit(X_train, y_train)
    y_pred2=reg2.predict(X_test)
    r2_2 = r2_score(y_test, y_pred2)
    MAE_2 = mean_absolute_error(y_test, y_pred2)
    RMSE_2 = root_mean_squared_error(y_test, y_pred2)
    print(f'Metrics: R2={r2_2}, MAE: {MAE_2}, RMSE: {RMSE_2}')
    # Second model is Random Forest Regressor Model from Scikit-learn. Model achieved R^2 score of 0.862 what is better score than Linear regression had, it explained 86% of variance in estate prices. MAE(Mean absolute error) is 118108PLN, it says that prediction differ from actual price by about 118k PLN, what is significant value when range of prices is 500k PLN and 3000k PLN, but it's better score compared to first one. RMSE(Root mean square error) is 171832 PLN, it is greater value that MAE, so it suggests that model occasionally makes larger prediction errors, as RMSE punishes larger faults more heavily than MAE. This model is better solution than Linear Regression Model.
    plt.scatter(y_test, y_pred2, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()],[y_test.min(), y_test.max()],color="red",linestyle="--")
    plt.xlabel("Actual price")
    plt.ylabel("Predicted price")
    plt.title("Actual vs Predicted(Random Forest Regressor)")
    plt.show()

    #3 Gradient Boosting regression
    print("==============================Gradient Boosting regression==================================")
    model3=GradientBoostingRegressor(random_state=42)
    reg3=model3.fit(X_train, y_train)
    y_pred3=reg3.predict(X_test)
    r2_3 = r2_score(y_test, y_pred3)
    MAE_3 = mean_absolute_error(y_test, y_pred3)
    RMSE_3 = root_mean_squared_error(y_test, y_pred3)
    print(f'Metrics: R2={r2_3}, MAE: {MAE_3}, RMSE: {RMSE_3}')
    # Third model is Gradient Boosting regression Model from Scikit-learn. Model achieved R^2 score of 0.880 what is better score than all models we have checked before , it explained 88% of variance in estate prices. MAE(Mean absolute error) is 112143PLN, it says that prediction differ from actual price by about 112k PLN, what is significant value when range of prices is 500k PLN and 3000k PLN, but it's better score compared to first and second model. RMSE(Root mean square error) is 164864 PLN, it is greater value that MAE, so it suggests that model occasionally makes larger prediction errors, as RMSE punishes larger faults more heavily than MAE. This model is the best solution among all models that we have performed so far.

    plt.scatter(y_test, y_pred3, alpha=0.5)
    plt.plot([y_test.min(), y_test.max()],[y_test.min(), y_test.max()],color="red",linestyle="--")
    plt.xlabel("Actual price")
    plt.ylabel("Predicted price")
    plt.title("Actual vs Predicted(Gradient Boosting)")
    plt.show()

    #We have also made 3 plots for 3 different models. As we see the better the model is, the closer to the 'ideal predicted line' the points are. Plots show us that the biggest cummulation near prediction line of points  are in range 0 - 1000k PLN, but it can be caused because of amount of data given in this range.


    #We will try to boost this model and to perform better results
    print("=========================importances======================")
    importance = model3.feature_importances_
    imp=pd.DataFrame({"Feature":X.columns,"Importance":importance})
    print(imp.sort_values(by='Importance',ascending=False))


    #n_estimators
   ## n=np.linspace(100,1000,10)
   ## for i in n:
   ##     model3 = GradientBoostingRegressor(random_state=42,n_estimators=int(i))
   ##     reg3 = model3.fit(X_train, y_train)
   ##     y_pred3 = reg3.predict(X_test)
   ##     r2_3 = r2_score(y_test, y_pred3)
   ##     MAE_3 = mean_absolute_error(y_test, y_pred3)
   ##     RMSE_3 = root_mean_squared_error(y_test, y_pred3)
   ##     print(f'est{i},Metrics: R2={r2_3}, MAE: {MAE_3}, RMSE: {RMSE_3}')

    #after performing this loop we noticed that n_estimators =200 gave best results:
    #est200.0,Metrics: R2=0.8866829073750055, MAE: 108527.79982524244, RMSE: 160071.41964837356
   ## lr=np.linspace(0.01,0.2,10)
   ## for i in lr:
   ##     model3 = GradientBoostingRegressor(random_state=42,n_estimators=200,learning_rate=i)
   ##     reg3 = model3.fit(X_train, y_train)
   ##     y_pred3 = reg3.predict(X_test)
   ##     r2_3 = r2_score(y_test, y_pred3)
   ##     MAE_3 = mean_absolute_error(y_test, y_pred3)
   ##     RMSE_3 = root_mean_squared_error(y_test, y_pred3)
   ##     print(f'lr={i},Metrics: R2={r2_3}, MAE: {MAE_3}, RMSE: {RMSE_3}')
##
    #after performing this loop we noticed that lr=0.15777 combined with n_est=200 gave best results
    #lr = 0.1577777777777778, Metrics: R2 = 0.8883559096149151, MAE: 109455.76163817394, RMSE: 158885.38652400463

    ##depth=np.linspace(1,10,10)
    ##for i in depth:
    ##    model3 = GradientBoostingRegressor(random_state=42,n_estimators=200,learning_rate=0.1577777777777778,max_depth=int(i))
    ##    reg3 = model3.fit(X_train, y_train)
    ##    y_pred3 = reg3.predict(X_test)
    ##    r2_3 = r2_score(y_test, y_pred3)
    ##    MAE_3 = mean_absolute_error(y_test, y_pred3)
    ##    RMSE_3 = root_mean_squared_error(y_test, y_pred3)
    ##    print(f'max_depth={i},Metrics: R2={r2_3}, MAE: {MAE_3}, RMSE: {RMSE_3}')

# after performing this loop we noticed that lr=0.15777 combined with n_est=200 and max_depth=3 gave best results
#max_depth=3.0,Metrics: R2=0.8883559096149151, MAE: 109455.76163817394, RMSE: 158885.38652400463

#conclusions:
#best combination is  n_estimators=200,learning_rate=0.1577777777777778,max_depth=3

#another attitude using GridSearchCV
    ##gb_model=GradientBoostingRegressor(random_state=42)
    ##n=[100, 200, 300]
    ##lr= [0.05, 0.1, 0.15, 0.2]
    ##depth=[2, 3, 4]
    ##params={"n_estimators": n,"learning_rate": lr,"max_depth": depth}
    ##grid_search=GridSearchCV(estimator=gb_model,param_grid=params,scoring="neg_root_mean_squared_error",cv=5,  n_jobs=-1,verbose=2)
    ##grid_search.fit(X_train, y_train)
    ##print(f"Best parameters={grid_search.best_params_}")
    ##best_model = grid_search.best_estimator_
    ##y_pred_best = best_model.predict(X_test)
    ##r2_best = r2_score(y_test, y_pred_best)
    ##mae_best = mean_absolute_error(y_test, y_pred_best)
    ##rmse_best = root_mean_squared_error(y_test, y_pred_best)
    ##
    ##print(f'Metrics: R2={r2_best}, MAE: {mae_best}, RMSE: {rmse_best}')

    #total conclusion:
    #After tuning I decide to use this parameters
    #n_estimators = 200, learning_rate = 0.1577777777777778, max_depth = 3
    final_model=GradientBoostingRegressor(random_state=42,n_estimators = 200, learning_rate = 0.1577777777777778, max_depth = 3)
    reg_final=final_model.fit(X_train,y_train)
    joblib.dump(final_model,'../../model/final_model.pkl')



