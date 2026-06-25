import streamlit as st
import pandas as pd
import os

DATA_FILE = "stock_data.csv"

# ပထမဆုံးအကြိမ်ဆိုရင် Data File တည်ဆောက်ခြင်း
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Name", "Category", "Opening", "In", "Issued", "Return", "Damage", "Used", "Stock", "Note"])
    # Dummy data ထည့်ပေးထားခြင်း
    df.loc[0] = ["Product A", "Production", 100, 50, 20, 2, 1, 0, 0, ""]
    df.to_csv(DATA_FILE, index=False)

# Data ဖတ်ခြင်း
df = pd.read_csv(DATA_FILE)

st.set_page_config(page_title="Store Keeper", layout="wide")
st.title("📦 Store Keeper Management")

# 1. Category ရွေးချယ်ခြင်း (Production / Packaging)
category = st.radio("အမျိုးအစား ရွေးချယ်ပါ", ["Production", "Packaging"], horizontal=True)

# ရွေးထားတဲ့ Category အလိုက် Filter လုပ်ခြင်း
filtered_df = df[df["Category"] == category]

st.subheader(f"{category} စာရင်း")
st.write("ဇယားကွက်ထဲတွင် တိုက်ရိုက်ပြင်နိုင်ပါသည် (Edit/Add/Delete လုပ်နိုင်သည်)")

# 2. Data Editor (Edit, Add, Delete လုပ်နိုင်သော Table)
edited_df = st.data_editor(
    filtered_df,
    num_rows="dynamic",
    use_container_width=True,
    column_config={
        "Category": st.column_config.SelectboxColumn("Category", options=["Production", "Packaging"], default=category),
    }
)

# 3. Formula တွက်ချက်ခြင်း (Auto-Calculate)
# Used = Issued - Return + Damage
# Stock = (Opening + In) - Used
if st.button("💾 Save & Calculate"):
    # ပြင်ဆင်ထားတဲ့ Data တွေကို မူရင်း Dataframe ထဲပြန်ထည့်ခြင်း
    # အရင်ဆုံး တခြား Category တွေကို ခွဲထုတ်ထားမယ်
    other_df = df[df["Category"] != category]
    
    # Formula တွက်ချက်ခြင်း
    edited_df["Used"] = edited_df["Issued"] - edited_df["Return"] + edited_df["Damage"]
    edited_df["Stock"] = (edited_df["Opening"] + edited_df["In"]) - edited_df["Used"]
    
    # အကုန်ပြန်ပေါင်းပြီး သိမ်းခြင်း
    updated_df = pd.concat([other_df, edited_df])
    updated_df.to_csv(DATA_FILE, index=False)
    st.success("✅ စာရင်းအားလုံး သိမ်းဆည်းပြီး Formula တွက်ချက်ပြီးပါပြီ။")
    st.rerun()

st.info("💡 အကြံပြုချက်: ဇယားအောက်ခြေရှိ 'Add row' ကိုနှိပ်၍ ပစ္စည်းအသစ်ထည့်နိုင်ပြီး၊ row များကို ရွေးချယ်၍ Delete နှိပ်ပြီး ဖျက်နိုင်ပါသည်။")
