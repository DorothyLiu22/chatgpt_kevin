import streamlit as st
from streamlit_chat import message
from streamlit_extras.colored_header import colored_header
from openai import OpenAI
import time
import re
import pandas as pd
import random
from datetime import datetime
from st_files_connection import FilesConnection
from google.cloud import storage

st.set_page_config(page_title="TechVantage聊天室")

conn = st.connection('gcs', type=FilesConnection)
#df = conn.read("streamlit_kevin/myfile.csv", input_format="csv", ttl=600)


AI_img = "https://raw.githubusercontent.com/DorothyLiu22/chatgpt_kevin/main/AI.png"
#AI_img = "https://www.shutterstock.com/image-vector/robot-head-avatar-vector-design-600nw-2352274355.jpg"
human_img = "https://raw.githubusercontent.com/DorothyLiu22/chatgpt_kevin/main/human.png"


def chat_history():
    #n = random.randint(1,1000)
    name = ["role", "content"]
    test = pd.DataFrame(columns = name, data=st.session_state.past)
    n = datetime.now()
    bucket = storage.Client().bucket("streamlit_kevin")
    blob = bucket.blob("AI/chat"+ str(n) +".csv")
    blob.upload_from_string(test.to_csv(), 'text/csv')

with st.sidebar:
    st.sidebar.title("💬 TechVantage 聊天室")

    blank = st.container(border=False, height=20)
    blank.title("")

    with st.container(border=True,):
        st.header("❗ 提醒")
        st.write("如遇报错，请简单修改您的语言再次发送，感谢理解")

    with st.container(border=True,):
        st.header("❗ 结束讨论后请按下按钮 ")
        if st.button("结束聊天", type="primary"):
           chat_history()
           progress_text = "聊天连接已断开，请回到问卷页面"
           my_bar = st.progress(0, text=progress_text)
           for percent_complete in range(100):
              time.sleep(0.01)
              my_bar.progress(percent_complete + 1, text=progress_text)
           time.sleep(1)
           my_bar.empty()

    blank = st.container(border=False,height=50)
    blank.title("")

    #openai_api_key = st.text_input("TechVantage", key="chatbot_api_key", type="password")
    #"[TechVantage](https://platform.openai.com/account/api-keys)"
    "[Source by Dorothy](https://github.com/DorothyLiu22/chatgpt_kevin)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"

st.title("💬 TechVantage 聊天室")
colored_header (label='', description='',color_name = 'gray-30')
openai_api_key = st.secrets["openai_api_key"]


kevin = """You are Kevin, an employee of “TechVantage Co.Ltd”, a multinational technology company. You need to engage in a discussion about how to retain highly skilled but underpaid employees in an uncertain economy. You need to talk to me about offering any viable solutions.

Your duty is to elaborate on my initial idea and come up with a feasible implementation plan. You also need to complete the task I gave to you.

Don't come up with more than three ideas at once. Your answers should not exceed 80 words. Do not ask me questions.

I'm your teammate. Please communicate in an informal way. Don't make a list of bullet points. Answer in one paragraph.

Please communicate with me in Chinese."""
#st.session_state["messages"] = ({"role": "system", "content": "you are a translator named Kevin"})

if "input" not in st.session_state:
    st.session_state["input"] = []
    st.session_state["output"] = []
    st.session_state["past"]=[]


for msg in st.session_state.past:
    if msg["role"] == "user":
        message(msg["content"], is_user=True, avatar_style="thumbs")
        #print(msg["content"])
    if msg["role"] == "assistant":
        message(msg["content"], avatar_style="bottts")
        #print(msg["content"])



welcome = ["你好","您好","hello","hi", "哈喽"]
name = ["你是谁","你叫什么", "名字"]
#start = ["开始讨论", "讨论"]
#end = ["还有什么想法", "其他的想法", "其他想法", "还有别的","还有新的"]
appreciation = ["有道理", "真不错","厉害"]
bye = ["拜拜", "就这样","没有其他想法了", "想到这些","没有新的想法"]
identity = ["是AI", "是人", "是机器人"]


if prompt := st.chat_input("开始聊天"):
    if re.search(welcome[0], prompt) or re.search(welcome[1], prompt) or re.search(welcome[2], prompt) \
            or re.search(welcome[3], prompt):
         message(prompt, is_user=True,avatar_style="thumbs")
         time.sleep(2)
         message("你好哇！我叫Kevin，我们现在要讨论如何在公司经济不稳定期间，留住高技能但薪资偏低的员工，你有什么想法吗？", avatar_style="bottts")
         st.session_state.past.append({"role": "user", "content": prompt})
         st.session_state.past.append({"role": "assistant", "content": "你好哇！我叫Kevin，我们现在要讨论如何在公司经济不稳定期间，留住高技能但薪资偏低的员工，你有什么想法吗？"})
    else:
        client = OpenAI(api_key=openai_api_key)
        st.session_state.input.append({"role":"system", "content":kevin})
        st.session_state.input.append({"role": "user", "content": prompt})
        message(prompt, is_user=True, avatar_style="thumbs")
        #st.chat_message("user").write(prompt)
        st.session_state.past.append({"role":"user", "content":prompt})
        response = client.chat.completions.create(model="gpt-3.5-turbo", messages=st.session_state.input)
        time.sleep(2)
        msg = response.choices[0].message.content
        st.session_state.output.append({"role": "assistant", "content": msg})
        st.session_state.past.append({"role": "assistant", "content": msg})
        message(msg, avatar_style="bottts")
        #st.chat_message("assistant").write(msg)






