import os # 导入os模块,用于获取环境变量
from dotenv import load_dotenv # 导入load_dotenv函数,用于加载环境变量
from openai import OpenAI # 导入OpenAI类,专门用来连接LLM 的库
import streamlit as st # 专门用来创建应用页面的库

load_dotenv() # 从.env文件中读取内容

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("https://api.deepseek.com"),
    ) # 创建一个OpenAI对象,用于连接LLM

#----------------------------------页面--------------------------

st.title(
    "🤖智能助手"
)
st.caption(
    "这是一个基于OpenAI的智能助手,你可以向它提问,它会用中文回答你"
)

#----------------------------------初始化对话历史--------------------------

#session_state是st提供的会话状态管理器，用于在用户的交互过程中保存数据
if "messages" not in st.session_state:
    st.session_state.messages = []

#--------------------------显示历史消息-------------------------------

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):   #创建一个消息容器
        st.write(msg["content"])          #往容器中写入内容

 #-------------------处理用户输入的内容---------------------------

if prompt := st.chat_input("输入你的问题···"):   #创建一个input框
    # 将用户的消息添加到
     st.session_state.messages.append({'role':"user","content":prompt})
     #在页面上展现这句话
     with st.chat_message('user'):
        st.write(prompt)

        #创建一个ai响应的容器
with st.chat_message('assistant'):
    #调用deepseek，并获取到相应，写入容器中

    response = client.chat.completions.create(
   model="deepseek-v4-flash",
   messages=[   #用于填写用户的问题
   {"role":"system","content":"你好"},
   #*是解包运算符，将一个数组中的内容解包到另一个数组中
   *st.session_state.messages
    ],
    stream=True
    )

    #处理流式资源

    full_response = st.write_stream(
        chunk.choices[0].delta.content or ""
        for chunk in response
        if chunk.choices[0].delta.content
    )

    #将ai返回的内容添加到历史消息中

    st.session_state.messages.append({"role":"assistant","content":full_response})

