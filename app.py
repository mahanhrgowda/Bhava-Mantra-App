import streamlit as st
import pandas as pd
import numpy as np
import ast

st.set_page_config(page_title="🎨 Styled Bhāva Mantra Card", layout="centered")
st.title("🎨 Bhāva Mantra Card by Mahān")

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("assets/phoneme_bhava_full.csv")
    df["bhava_vector"] = df["bhava_vector"].apply(ast.literal_eval)
    df["chakra_vector"] = df["chakra_vector"].apply(ast.literal_eval)
    df["rasa_vector"] = df["rasa_vector"].apply(ast.literal_eval)
    return df

df = load_data()

# Emojis
bhava_emoji = {
    "Ratiḥ": "❤️", "Hāsaḥ": "😄", "Śokaḥ": "😢", "Krodhaḥ": "😡",
    "Utsāhaḥ": "💪", "Bhayaṁ": "😨", "Jugupsā": "🤮", "Vismayaḥ": "🤯", "Śamaḥ": "🧘",
    "Rāgaḥ": "❤️", "Karuṇā": "😢"
}
chakra_emoji = {
    "Mūlādhāra": "🟥", "Svādhiṣṭhāna": "🟧", "Maṇipūra": "🟡",
    "Anāhata": "💚", "Viśuddha": "🔵", "Ājñā": "👁️", "Sahasrāra": "👑"
}
rasa_emoji = {
    "Śṛṅgāra": "💗", "Hāsya": "😂", "Karuṇā": "💙", "Raudra": "🔥",
    "Vīra": "⚔️", "Bhayānaka": "😱", "Bībhatsa": "🤢", "Adbhuta": "✨", "Śānta": "🕊"
}

# Input name
name = st.text_input("🔡 Enter your name:", "Mahān")

def extract_phonemes(name):
    name = name.lower()
    phonemes = [ph for ph in df.phoneme if ph in name]
    return phonemes

if name:
    phonemes = extract_phonemes(name)
    matches = df[df.phoneme.isin(phonemes)]

    if matches.empty:
        st.warning("⚠️ No valid phonemes found in the name.")
    else:
        bhavas = matches["bhava"].tolist()
        chakras = matches["chakra"].tolist()
        rasas = matches["rasa"].tolist()

        bhava_line = " • ".join(f"{bhava_emoji.get(b, '')} {b}" for b in bhavas)
        chakra_line = " → ".join(f"{chakra_emoji.get(c, '')} {c}" for c in chakras)
        rasa_line = " → ".join(f"{rasa_emoji.get(r, '')} {r}" for r in rasas)

        st.markdown(f"""
        ### 🎨 Styled Bhāva Mantra Card
        | Element    | Value |
        |------------|-------|
        | **Bhāvas** | {bhava_line} |
        | **Chakras**| {chakra_line} |
        | **Rasa Flow**| {rasa_line} |
        """)

        st.markdown(f"""
        ### 📛 Name: `{name}`
        🔎 **Essence from Phoneme Analysis:**
        """)

        for _, row in matches.iterrows():
            st.markdown(f"- {row['bhava']} {bhava_emoji.get(row['bhava'], '')} → {row['chakra']} {chakra_emoji.get(row['chakra'], '')} → {row['rasa']} {rasa_emoji.get(row['rasa'], '')}")

        # Bhāva vector summary
        st.subheader(f"✅ 5. Result Summary for {name}")
        bv = matches.groupby("bhava").agg({"bhava_vector": lambda x: np.sum(x.tolist(), axis=0)})
        bv_sum = bv["bhava_vector"].apply(np.linalg.norm).sort_values(ascending=False)

        st.markdown("🧬 **Name Bhāva Vector**")
        st.json({k: round(v * 10, 1) for k, v in bv_sum.items()})

        st.markdown("🌈 **Dominant Bhāva(s):**")
        st.write(", ".join(f"{k} {bhava_emoji.get(k, '')}" for k in bv_sum.head(2).index))

        if len(bv_sum) > 2:
            st.markdown("🔥 **Secondary Bhāva:**")
            st.write(f"{bv_sum.index[2]} {bhava_emoji.get(bv_sum.index[2], '')}")

        st.markdown("🌀 **Chakra Flow:**")
        st.write(" → ".join(f"{chakra_emoji.get(c)} {c}" for c in chakras))

        st.markdown("🎭 **Rasa Blend:**")
        st.write(" + ".join(f"{rasa_emoji.get(r)} {r}" for r in rasas))
