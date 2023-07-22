import numpy as np
import sklearn as sk
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Input
from sklearn.datasets import load_diabetes
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler, StandardScaler

#1. 데이터
datasets = load_diabetes()
x = datasets.data
y = datasets.target

# print(x)
print(x.shape)  # (442, 10)
# print(y)
print(y.shape)  # (442,)

print(datasets.feature_names)

print(datasets.DESCR)

x_train, x_test, y_train, y_test = train_test_split(x, y,
    train_size=0.7, shuffle=True, random_state=123)


# 데이터 전처리
scaler = MinMaxScaler()                     # minmaxscaler 정의
# scaler = StandardScaler()
scaler.fit(x_train)                         # x값의 범위만큼 가중치 생성
x_train = scaler.transform(x_train)
# x_train = scaler.fit_transform(x_test)
x_test = scaler.transform(x_test)           # x_train fit한 가중치 값 범위에 맞춰서 x_test 데이터 변환


""" #2. 모델 구성 (순차형)
model = Sequential()
model.add(Dense(16, input_dim=10))
model.add(Dense(25))
model.add(Dense(32))
model.add(Dense(72))
model.add(Dense(18))
model.add(Dense(64))
model.add(Dense(1)) """

#2. 모델 구성 (함수형)                                  # 순차형과 반대로 레이어 구성
input1 = Input(shape=(10,))                             # 입력 데이터의 크기(shape)를 Input() 함수의 인자로 입력층 정의
dense1 = Dense(25, activation='linear')(input1)         # 이전층을 다음층 함수의 입력으로 사용하고, 변수에 할당
dense2 = Dense(32, activation='sigmoid')(dense1)
dense3 = Dense(72, activation='relu')(dense2)
dense4 = Dense(18, activation='linear')(dense3)
dense5 = Dense(64, activation='linear')(dense4)
output1 = Dense(1, activation='linear')(dense5)
model = Model(inputs=input1, outputs=output1)           # 순차형과 달리 model 형태를 마지막에 정의.     Model() 함수에 입력과 출력 정의
model.summary()

#3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam')

from tensorflow.keras.callbacks import EarlyStopping
EarlyStopping = EarlyStopping(monitor='val_loss', 
                              mode='min',
                              patience=10, 
                              restore_best_weights=True,
                              verbose=1)
hist = model.fit(x_train, y_train, epochs=200, batch_size=25, 
          validation_split=0.2, callbacks=[EarlyStopping], 
          verbose=1)

#4. 평가, 예측
loss = model.evaluate(x_test, y_test)
print('loss : ', loss)


print("==================================================")
print(hist) # <keras.callbacks.History object at 0x0000017442ACECA0>
print("==================================================")
print(hist.history)
print("==================================================")
print(hist.history['loss'])


y_predict = model.predict(x_test)

from sklearn.metrics import mean_squared_error, r2_score
def RMSE(y_test, y_predict):
    return np.sqrt(mean_squared_error(y_test, y_predict))
print("RMSE : ", RMSE(y_test, y_predict))

r2 = r2_score(y_test, y_predict)
print("R2 : ", r2)


# 시각화
import matplotlib.pyplot as plt

plt.figure(figsize=(9,6))
plt.plot(hist.history['loss'], c='red', 
         marker='.', label='loss') 
plt.plot(hist.history['val_loss'], c='blue', 
         marker='.', label='val_loss')
plt.grid()
plt.xlabel('epochs')
plt.ylabel('loss')
plt.title('boston loss')
plt.legend()
# plt.legeng(loc='upper right')
plt.show()

""" 
Epoch 00076: early stopping
loss :  3087.035888671875
RMSE :  55.56110283034244
R2 :  0.4808833090193445 """