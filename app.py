import streamlit as st
import json
import os
from gtts import gTTS

# 设置页面标题和布局
st.set_page_config(page_title="48音标大师课", layout="wide", page_icon="🎤")

# --- 核心功能函数 ---

# 1. 读取数据
@st.cache_data
def load_data():
    try:
        with open('data.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        st.error("找不到 data.json 文件！请确保它和 app.py 在同一个文件夹里。")
        return []

# 2. 生成发音 (带缓存，避免重复生成)
def get_audio_html(text, lang='en'):
    # 这里我们用一个小技巧，直接生成 HTML 音频播放器，不保存文件以加快速度
    try:
        tts = gTTS(text=text, lang=lang)
        filename = f"temp_{text}.mp3"
        tts.save(filename)
        
        # 读取音频文件并转换为二进制
        with open(filename, "rb") as f:
            audio_bytes = f.read()
        
        # 清理临时文件
        os.remove(filename)
        
        return audio_bytes
    except Exception as e:
        return None

# --- 界面设计 ---

def main():
    st.title("🎤 48个国际音标发音特训")
    st.markdown("### 打造地道口语的秘密武器")
    
    data = load_data()
    if not data:
        return

    # 1. 侧边栏：筛选器
    st.sidebar.header("📚 课程目录")
    
    # 提取所有分类
    categories = sorted(list(set([item['category'] for item in data])))
    selected_category = st.sidebar.radio("选择要练习的音标组：", categories)
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **学生使用指南**：\n1. 先看口型描述。\n2. 听单词发音。\n3. 完成底部的'课后挑战'。")

    # 2. 主区域：显示卡片
    st.header(f"{selected_category}")
    
    # 筛选当前分类的数据
    filtered_data = [d for d in data if d['category'] == selected_category]

    # 使用 Grid 布局，每行显示 2 个卡片
    cols = st.columns(2)
    
    for index, item in enumerate(filtered_data):
        # 奇数偶数分配到两列
        with cols[index % 2]:
            with st.container(border=True):
                # 标题栏：音标 + 名称
                st.subheader(f"{item['symbol']} {item['name']}")
                
                # 口型描述
                st.markdown(f"**👄 发音秘诀：**\n{item['desc']}")
                
                st.divider()
                
                # 单词部分
                st.markdown("**📝 核心词汇 (Words):**")
                word_str = ", ".join(item['words'])
                st.text(word_str)
                
                # 播放单词按钮
                if st.button(f"🔊 听单词 ({item['symbol']})", key=f"btn_{index}"):
                    audio_bytes = get_audio_html(word_str)
                    if audio_bytes:
                        st.audio(audio_bytes, format='audio/mp3')
                
                st.divider()
                
                # 句子部分
                st.markdown(f"**🗣️ 句子跟读:**\n*{item['sentence']}*")
                
                # 课后挑战 (高亮显示)
                st.success(f"💪 **课后挑战:** {item['challenge']}")

if __name__ == "__main__":
    main()
