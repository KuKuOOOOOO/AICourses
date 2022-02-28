import numpy as np
import keras
from keras.models import Sequential
from keras.datasets import mnist
from keras.layers import Dense, Dropout, Activation, Flatten, Conv2D, MaxPooling2D
from keras.utils import np_utils  # 用來後續將 label 標籤轉為 one-hot-encoding
from keras import backend as K
from matplotlib import pyplot as plt
import cv2

# 定義梯度下降批量
batch_size = 128
# 定義分類數量
num_classes = 10
# 定義圖像寬、高
img_rows, img_cols = 28, 28
# 定義訓練週期
epochs = 12

# 載入 MNIST 資料庫的訓練資料，並自動分為『訓練組』及『測試組』
(x_train, y_train), (x_test, y_test) = mnist.load_data()
# 保留原始資料，供 cross tab function 使用
y_test_org = y_test

# channels_first: 色彩通道(R/G/B)資料(深度)放在第2維度，第3、4維度放置寬與高
if K.image_data_format() == 'channels_first':
    x_train = x_train.reshape(x_train.shape[0], 1, img_rows, img_cols)
    x_test = x_test.reshape(x_test.shape[0], 1, img_rows, img_cols)
    input_shape = (1, img_rows, img_cols)
# channels_last: 色彩通道(R/G/B)資料(深度)放在第4維度，第2、3維度放置寬與高
else: 
    x_train = x_train.reshape(x_train.shape[0], img_rows, img_cols, 1)
    x_test = x_test.reshape(x_test.shape[0], img_rows, img_cols, 1)
    input_shape = (img_rows, img_cols, 1)

# 轉換色彩 0~255 資料為 0~1
x_train = x_train.astype('float32')
x_test = x_test.astype('float32')
x_train /= 255
x_test /= 255

# y 值轉成 one-hot encoding
y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)


# 建立簡單的線性執行的模型
model = Sequential()
# 建立卷積層，filter=32,即 output space 的深度, Kernal Size: 3x3, activation function 採用 relu
model.add(Conv2D(32, kernel_size=(3, 3), activation='relu', input_shape=input_shape))
# 建立卷積層，filter=64,即 output size, Kernal Size: 3x3, activation function 採用 relu
model.add(Conv2D(64, kernel_size=(3, 3), activation='relu'))
# 建立池化層，池化大小=2x2，取最大值
model.add(MaxPooling2D(pool_size=(2, 2)))
# Dropout層隨機斷開輸入神經元，用於防止過度擬合，斷開比例:0.25
model.add(Dropout(0.25))
# Flatten層把多維的輸入一維化，常用在從卷積層到全連接層的過渡。
model.add(Flatten())
# 全連接層: 128個output
model.add(Dense(128, activation='relu'))
# Dropout層隨機斷開輸入神經元，用於防止過度擬合，斷開比例:0.5
model.add(Dropout(0.5))
# 使用 softmax activation function，將結果分類
model.add(Dense(num_classes, activation='softmax'))

# 編譯: 選擇損失函數、優化方法及成效衡量方式
model.compile(loss=keras.losses.categorical_crossentropy, optimizer=keras.optimizers.Adadelta(), metrics=['accuracy'])

# 將 training 的 label 進行 one-hot encoding，例如數字 7 經過 One-hot encoding 轉換後是 0000001000，即第7個值為 1
y_TrainOneHot = np_utils.to_categorical(y_train)
y_TestOneHot = np_utils.to_categorical(y_test)

# 進行訓練, 訓練過程會存在 train_history 變數中
train_history = model.fit(x_train, y_train, batch_size=batch_size, epochs=epochs, verbose=1, validation_data=(x_test, y_test))

# 顯示訓練成果(分數)
scores = model.evaluate(x_test, y_test, verbose=0)
print()
print("\t[Info] Accuracy of testing data = {:2.1f}%".format(scores[1]*100.0))

# 預測(prediction) 學號的圖檔存放位置
Output = [0] * 7
for i in range(0, len(Output)):
    imgstr = str(i)
    image = cv2.imread('image/image'+imgstr+'.png', cv2.IMREAD_GRAYSCALE)
    # 學號利用opencv將圖檔轉換成numpy陣列並轉成灰階
    res = cv2.resize(image, dsize=(img_rows, img_cols))
    if K.image_data_format() == 'channels_first':
        X1 = res.reshape(1, 1, img_rows, img_cols)
    # channels_last: 色彩通道(R/G/B)資料放在第4維度，第2、3維度放置寬與高
    else:
        X1 = res.reshape(1, img_rows, img_cols, 1)
    X1 = X1/255
    predictions = model.predict_classes(X1)
    Output[i] = predictions[0]
print(Output)
