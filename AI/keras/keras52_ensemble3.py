import numpy as np

#1. 데이터
x1_datasets = np.array([range(100), range(301, 401)]).transpose()
print(x1_datasets.shape)    # (100, 2)
x2_datasets = np.array([range(101, 201), range(411, 511), range(150, 250)]).T
print(x2_datasets.shape)    # (100, 3)
x3_datasets = np.array([range(100, 200), range(1301, 1401)]).T
print(x3_datasets.shape)    # (100, 2)

y1 = np.array(range(2001, 2101))     # (100, )       # 삼성전자의 하루 뒤 종가 예측
y2 = np.array(range(201, 301))      # (100,)        # 아모레의 하루 뒤 종가
y3 = np.array(range(201, 301))

from sklearn.model_selection import train_test_split
x1_train, x1_test, x2_train, x2_test, x3_train, x3_test, y1_train, y1_test, y2_train, y2_test, y3_train, y3_test = train_test_split(
    x1_datasets, x2_datasets, x3_datasets, y1, y2, y3, train_size=0.7, random_state=1234
)

print(x1_train.shape, x2_train.shape, x3_train.shape, y1_train.shape, y2_train.shape, y3_train.shape)
print(x1_test.shape, x2_test.shape, x3_test.shape, y1_test.shape, y2_test.shape, y3_test.shape)


#2-1. 모델 1
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, Input

input1 = Input(shape=(2,))
dense1 = Dense(10, activation='relu', name='ds11')(input1)
dense2 = Dense(10, activation='relu', name='ds12')(dense1)
dense3 = Dense(10, activation='relu', name='ds13')(dense2)
output1 = Dense(10, activation='relu', name='ds14')(dense3)

#2-2. 모델 2
input2 = Input(shape=(3,))
dense1 = Dense(20, activation='linear', name='ds21')(input1)
dense2 = Dense(20, activation='linear', name='ds22')(dense1)
output2 = Dense(20, activation='linear', name='ds23')(dense2)

#2-3. 모델 3
input3 = Input(shape=(2,))
dense1 = Dense(30, activation='relu', name='ds31')(input1)
dense2 = Dense(30, activation='relu', name='ds32')(dense1)
output3 = Dense(30, activation='relu', name='ds33')(dense2)

#2-4. 모델 병합
from tensorflow.keras.layers import concatenate, Concatenate            # Concatenate 함수로 변경
# merge1 = concatenate([output1, output2, output3], name='mg1')
merge1 = Concatenate()([output1, output2, output3])
merge2 = Dense(10, activation='relu', name='mg2')(merge1)
merge3 = Dense(10, name='mg3')(merge2)
last_output = Dense(1, name='last')(merge3)

#2-5. 모델 5 = 분기 1 (모델 병합한 것 다시 둘로 쪼개기)
dense5 = Dense(20, activation='relu', name='ds51')(last_output)
dense5 = Dense(20, activation='relu', name='ds52')(dense5)
output5 = Dense(20, activation='relu', name='ds54')(dense5)

#2-6. 모델 6 = 분기 2 (모델 병합한 것 다시 둘로 쪼개기)
dense6 = Dense(10, activation='linear', name='ds61')(last_output)
dense6 = Dense(10, activation='linear', name='ds62')(dense6)
output6 = Dense(10, activation='linear', name='ds63')(dense6)

#2-6. 모델 7 = 분기 3 (모델 병합한 것 다시 둘로 쪼개기)
dense7 = Dense(10, activation='linear', name='ds71')(last_output)
dense7 = Dense(10, activation='linear', name='ds72')(dense7)
output7 = Dense(10, activation='linear', name='ds73')(dense7)

model = Model(inputs=[input1, input2, input3], outputs=[output5, output6, output7])

model.summary()


#3. 컴파일, 훈련
model.compile(loss='mse', optimizer='adam', metrics=['mae'])
model.fit([x1_train, x2_train, x3_train], [y1_train, y2_train, y3_train], epochs=500, batch_size=5)


#4. 평가, 예측
loss = model.evaluate([x1_test, x2_test, x3_test], [y1_test, y2_test, y3_test])
print('loss : ', loss)


# loss :  [2337447.5, 2336583.5, 429.5423583984375, 434.58544921875, 1137.907958984375, 17.230831146240234, 17.221845626831055]