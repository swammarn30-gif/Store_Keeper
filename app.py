import streamlit as st
import pandas as pd
import os

# စာရင်းဒေတာများကို အမြဲသိမ်းထားမည့် ဖိုင်အမည်
DATA_FILE = "stock_data.csv"

# ဖိုင်မရှိသေးရင် အသစ်တစ်ခု အလိုအလျောက် ဆောက်ပေးခြင်း
if not os.path.exists(DATA_FILE):
    df = pd.DataFrame(columns=["Name", "Opening", "In", "Issued", "Return", "Damage", "Used", "Stock", "Note"])
    df.to_csv(DATA_FILE, index=False)

# သိမ်းထားတဲ့ စာရင်းတွေကို ပြန်ဖတ်ခြင်း
df = pd.read_csv(DATA_FILE)

# Web App ရဲ့ မျက်နှာပြင် Layout ပြင်ဆင်မှု
st.set_page_config(page_title="Store Keeper App", layout="wide")
st.title("📦 Store Keeper - Stock Management System")
st.write("သင့်စာအုပ်ထဲက Formula အတိုင်း တိကျစွာ တွက်ချက်ပေးမည့် စနစ်")

st.write("---")
st.subheader("📝 နေ့စဉ်စာရင်းအသစ် ထည့်သွင်းရန်")

# အချက်အလက် ဖြည့်သွင်းရမည့်ဇယားကွက် (Form)
with st.form("stock_entry_form", clear_on_submit=True):
    col1, col2, col3 = st.columns(3)
    
    with col1:
        name = st.text_input("ပစ္စည်းအမည် (Name)")
        opening = st.number_input("အဖွင့်လက်ကျန် (Opening)", min_value=0, value=0)
    with col2:
        incoming = st.number_input("ဝင်လာသောအရေအတွက် (In)", min_value=0, value=0)
        issued = st.number_input("ထုတ်ပေးသောအရေအတွက် (Issued)", min_value=0, value=0)
    with col3:
        returned = st.number_input("ပြန်ဝင် (Return)", min_value=0, value=0)
        damaged = st.number_input("ပျက်စီး (Damage)", min_value=0, value=0)
        
    note = st.text_input("မှတ်ချက် (Note)")
    
    submitted = st.form_submit_button("💾 စာရင်းသိမ်းဆည်းမည်")

# စာရင်းသွင်းခလုတ် နှိပ်လိုက်သည့်အခါ လုပ်ဆောင်ချက်
if submitted:
    if name.strip() == "":
        st.error("⚠️ ကျေးဇူးပြု၍ ပစ္စည်းအမည် (Name) ထည့်သွင်းပေးပါ။")
    else:
        # သင်တောင်းဆိုထားသော Formula အသစ်အတိုင်း တွက်ချက်ခြင်း
        # Damage ကိုပါ အသုံးထဲထည့်ပေါင်းပြီး တကယ်ကုန်သွားတဲ့ အရေအတွက်ကို ရှာပါတယ်
        used = issued - returned + damaged
        stock = (opening + incoming) - used
        
        new_row = {
            "Name": name,
            "Opening": opening,
            "In": incoming,
            "Issued": issued,
            "Return": returned,
            "Damage": damaged,
            "Used": used,
            "Stock": stock,
            "Note": note
        }
        
        # ဒေတာအသစ်ကို သိမ်းဆည်းခြင်း
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        df.to_csv(DATA_FILE, index=False)
        st.success(f"✅ {name} အတွက် စာရင်းတွက်ချက် သိမ်းဆည်းပြီးပါပြီ။")
        st.rerun()

st.write("---")
st.subheader("📊 ယနေ့ စာရင်းဇယားပြကွက်")

# စာရင်းရှိနေလျှင် ဇယားဖြင့် ပြသပေးခြင်း
if not df.empty:
    st.dataframe(df, use_container_width=True)
    
    st.write("---")
    st.subheader("🌅 နေ့ချုပ်သိမ်းဆည်းခြင်း")
    st.write("ဒီနေ့ရဲ့ လက်ကျန် (Stock) ကို နောက်နေ့ရဲ့ အဖွင့်လက်ကျန် (Opening) ဖြစ်အောင် အလိုအလျောက် ပြောင်းလဲပေးပါမည်။")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("🌅 နေ့ချုပ်ပြီး နောက်နေ့စာရင်းစရန်"):
            # ဒီနေ့ရဲ့ Stock ကို နောက်နေ့ရဲ့ Opening နေရာကို ပို့ပြီး ကျန်ဒေတာများကို 0 ပြန်လုပ်ခြင်း
            df["Opening"] = df["Stock"]
            df["In"] = 0
            df["Issued"] = 0
            df["Return"] = 0
            df["Damage"] = 0
            df["Used"] = 0
            df["Stock"] = df["Opening"]
            df.to_csv(DATA_FILE, index=False)
            st.success("🎉 နေ့ချုပ်သိမ်းဆည်းပြီးပါပြီ။ နောက်နေ့မနက်အတွက် အဖွင့်လက်ကျန်များ ပြင်ဆင်ပြီးပါပြီ။")
            st.rerun()
            
    with col_btn2:
        if st.button("🗑️ စာရင်းအားလုံးကို အစကပြန်ဖျက်ရန်"):
            df = pd.DataFrame(columns=["Name", "Opening", "In", "Issued", "Return", "Damage", "Used", "Stock", "Note"])
            df.to_csv(DATA_FILE, index=False)
            st.warning("🗑️ စာရင်းအားလုံးကို ရှင်းလင်းပစ်လိုက်ပါပြီ။")
            st.rerun()
else:
    st.info("ယခုလောလောဆယ် ထည့်သွင်းထားသော စာရင်းမရှိသေးပါ။ အပေါ်က Form တွင် စတင်ဖြည့်သွင်းနိုင်ပါသည်။")
