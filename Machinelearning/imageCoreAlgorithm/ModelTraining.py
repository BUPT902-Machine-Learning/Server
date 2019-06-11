from sklearn import svm
import numpy as np
from sklearn.model_selection import GridSearchCV
from sklearn.externals import joblib
from Machinelearning.settings import BASE_DIR
import os


def model_training(augment_images_info, model_id, model_type, X_train, y_train, X_test, y_test):
    if model_type == "SVM":
        if len(augment_images_info) == 2:
            parameters = {'kernel': ['linear'],
                          'C': np.linspace(0.1, 20, 50),
                          'gamma': np.linspace(0.1, 20, 20)}
        else:
            parameters = {'kernel': ['rbf'],
                          'C': np.linspace(0.1, 20, 50),
                          'gamma': np.linspace(0.1, 20, 20)}
        svc = svm.SVC()
        best_svm = GridSearchCV(svc, parameters, cv=5, scoring='accuracy')
        print("SVM model is training !")
        best_svm.fit(X_train, y_train)
        best = best_svm.best_params_

        model = svm.SVC(C=best['C'], kernel='rbf', gamma=best['gamma'])
        model.fit(X_train, y_train)
        # 模型训练完毕，保存SVM模型
        file_path = os.path.join(BASE_DIR, "image_model")
        is_path_exists = os.path.exists(file_path)
        if not is_path_exists:
            os.makedirs(file_path)
        file_name = model_id + "_svm.m"
        file_path = os.path.join(file_path, file_name)
        joblib.dump(model, file_path)
        print("model training is finished !")
