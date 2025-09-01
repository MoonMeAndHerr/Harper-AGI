import os, numpy as np, joblib
from pathlib import Path
from tensorflow.keras.applications import MobileNetV2
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Model, load_model, Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.losses import MeanSquaredError
from tensorflow.keras.preprocessing import image
from sklearn.preprocessing import StandardScaler
import pandas as pd
import random

MODEL_PATH = "models/cnn_regressor.h5"
SCALER_PATH = "models/feature_scaler.joblib"

def build_feature_extractor():
    base = MobileNetV2(weights='imagenet', include_top=False, input_shape=(224,224,3))
    x = GlobalAveragePooling2D()(base.output)
    model = Model(inputs=base.input, outputs=x)
    return model

def build_regressor(input_dim):
    m = Sequential([
        Dense(128, activation='relu', input_shape=(input_dim,)),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    m.compile(optimizer='adam', loss=MeanSquaredError(), metrics=[])
    return m

def image_to_feature(img_pil, feature_extractor):
    img = img_pil.resize((224,224)).convert('RGB')
    arr = image.img_to_array(img)
    arr = np.expand_dims(arr, 0)
    arr = preprocess_input(arr)
    feat = feature_extractor.predict(arr, verbose=0)
    return feat.flatten()

def ensure_model(sample_csv="sample_data/simulated_metrics.csv"):
    if Path(MODEL_PATH).exists() and Path(SCALER_PATH).exists():
        scaler = joblib.load(SCALER_PATH)
        reg = load_model(MODEL_PATH)
        feat_ext = build_feature_extractor()
        return feat_ext, reg, scaler
    df = pd.read_csv(sample_csv)
    rng = random.Random(42)
    embeddings = []
    targets = []
    for _, r in df.sample(n=min(1500,len(df)), random_state=42).iterrows():
        base = {"Image":0.02,"Video":0.05,"Carousel":0.04,"Text":0.015}.get(r['content_type'],0.02)
        hour_factor = (r['hour'] - 8) / 14.0
        platform_factor = {"Instagram":0.03,"LinkedIn":0.02,"Facebook":0.018,"TikTok":0.05,"X":0.012}.get(r['platform'],0.02)
        mean = base + platform_factor*0.5 + hour_factor*0.01
        vec = np.array([rng.uniform(mean-0.01, mean+0.01) for _ in range(128)])
        embeddings.append(vec)
        targets.append(r['engagement_rate'])
    X = np.vstack(embeddings)
    y = np.array(targets).reshape(-1,1)
    scaler = StandardScaler().fit(X)
    Xs = scaler.transform(X)
    reg = build_regressor(Xs.shape[1])
    reg.fit(Xs, y, epochs=5, batch_size=64, verbose=0)
    os.makedirs('models', exist_ok=True)
    reg.save(MODEL_PATH)
    joblib.dump(scaler, SCALER_PATH)
    feat_ext = build_feature_extractor()
    return feat_ext, reg, scaler

def predict_from_pil(img_pil, feat_ext, reg, scaler):
    feat = image_to_feature(img_pil, feat_ext)
    target_dim = scaler.mean_.shape[0]
    if feat.shape[0] > target_dim:
        k = feat.shape[0] // target_dim
        feat_small = feat[:k*target_dim].reshape(target_dim, k).mean(axis=1)
    else:
        feat_small = np.pad(feat, (0, target_dim - feat.shape[0]), 'constant')
    Xs = scaler.transform(feat_small.reshape(1,-1))
    score = float(reg.predict(Xs, verbose=0).flatten()[0])
    return max(0.0, min(1.0, score)), feat_small
