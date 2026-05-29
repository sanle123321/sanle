import os # 导入os模块,用于获取环境变量
from dotenv import load_dotenv # 导入load_dotenv函数,用于加载环境变量
from openai import OpenAI # 导入OpenAI类,专门用来连接LLM 的库
import streamlit as st # 专门用来创建应用页面的库

load_dotenv() # 从.env文件中读取内容

client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url=os.getenv("BASE_URL"),
    ) # 创建一个OpenAI对象,用于连接LLM

response = client.chat.completions.create(
   model="deepseek-v4-flash",
   messages=[   #用于填写用户的问题
   {"role":"system","content":"你好"},
   {"role":"user","content":"用三句话解释人工智能"} 

   ]
    )

print(response.choices[0].message.content)
