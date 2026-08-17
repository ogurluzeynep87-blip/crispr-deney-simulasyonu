
import streamlit as st
import pandas as pd
import joblib
import os
import requests
import joblib

MODEL_URL = "https://huggingface.co/user2026-ai/crispr_model.pkl/resolve/main/crispr_model.pkl"
MODEL_PATH = "/tmp/crispr_model.pkl"

if not os.path.exists(MODEL_PATH):
    r = requests.get(MODEL_URL, stream=True)
    r.raise_for_status()
    with open(MODEL_PATH, "wb") as f:
        for chunk in r.iter_content(chunk_size=1024 * 1024):
            if chunk:
                f.write(chunk)

model = joblib.load(MODEL_PATH)

st.title("🧬 CRISPR Deney Simülasyonu")

st.write("20 bazlık bir sgRNA dizisi gir:")

dizi = st.text_input(
    "sgRNA",
    placeholder="CATCTTCTTTCACCTGAACG"
)

if st.button("🧪 Deneyi Başlat"):

    seq = dizi.upper().strip()

    if len(seq) != 20:
        st.error("Dizi tam 20 baz olmalı.")

    elif any(b not in "ACGT" for b in seq):
        st.error("Sadece A, C, G ve T kullanılabilir.")

    else:

        ozellik = []

        for baz in seq:
            ozellik.extend([
                int(baz == "A"),
                int(baz == "C"),
                int(baz == "G"),
                int(baz == "T")
            ])

        X_yeni = pd.DataFrame(
            [ozellik],
            columns=[
                f"P{i}_{b}"
                for i in range(1, 21)
                for b in "ACGT"
            ]
        )

        tahmin = model.predict(X_yeni)[0]

        st.subheader("🔬 Deney Sonucu")

        st.write(f"🧬 sgRNA: `{seq}`")
        st.write(f"📊 Tahmini LogFC: **{tahmin:.4f}**")

        if tahmin < 0:
            st.write("📉 Tahmin edilen yön: **NEGATİF**")
        else:
            st.write("📈 Tahmin edilen yön: **POZİTİF**")

        st.warning(
            "Bu sonuç bir makine öğrenmesi tahminidir; "
            "gerçek laboratuvar sonucu değildir."
        )
