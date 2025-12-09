"""
每周菜谱生成器
使用 Streamlit 创建的网页应用，用于生成周一到周五的健康菜谱
优化版本：
1. 数据分离：菜品数据存储在 dishes.json 中
2. 算法优化：避免连续两天吃同一道菜
3. 容错处理：过滤条件太严格时友好提示
4. 手机适配：每天一个大卡片布局
"""

import streamlit as st
import random
from datetime import datetime
import json
import os

# 页面配置 - 手机优先设计
st.set_page_config(
    page_title="每周菜谱生成器 🍽️",
    page_icon="🍽️",
    layout="wide",  # 使用wide布局以便在手机上也能良好显示
    initial_sidebar_state="expanded"
)

# 自定义CSS样式 - 让界面更美观温馨
st.markdown("""
    <style>
    /* 主标题样式 */
    .main-title {
        font-size: 2.5rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: bold;
    }
    
    /* 卡片样式 */
    .menu-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        color: white;
    }
    
    /* 日期标题样式 */
    .day-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
        color: #FFD93D;
    }
    
    /* 菜品列表样式 */
    .dish-item {
        font-size: 1.2rem;
        margin: 0.5rem 0;
        padding: 0.5rem;
        background: rgba(255, 255, 255, 0.2);
        border-radius: 8px;
    }
    
    /* 响应式设计 - 手机优先 */
    @media (max-width: 768px) {
        .main-title {
            font-size: 1.8rem;
        }
        .day-title {
            font-size: 1.2rem;
        }
        .dish-item {
            font-size: 1rem;
        }
    }
    
    /* 按钮样式 */
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-size: 1.2rem;
        padding: 0.75rem;
        border-radius: 10px;
        border: none;
        font-weight: bold;
    }
    
    .stButton>button:hover {
        background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
        transform: scale(1.02);
    }
    </style>
""", unsafe_allow_html=True)

# ==================== 数据加载函数 ====================

def load_dishes():
    """
    从 dishes.json 文件加载菜品数据
    就像保险公司从"条款库"读取保单条款一样
    
    返回:
        包含三个类别菜品的字典: {"main_meat": [...], "semi_meat": [...], "veggie": [...]}
    """
    # 获取当前文件所在目录
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(current_dir, "dishes.json")
    
    try:
        # 尝试读取 JSON 文件（就像打开保险条款库）
        with open(json_path, 'r', encoding='utf-8') as f:
            dishes = json.load(f)
        return dishes
    except FileNotFoundError:
        # 如果文件不存在，显示错误提示（就像保单找不到一样要告诉客户）
        st.error("❌ 找不到菜品数据文件 dishes.json，请确保文件在程序目录下！")
        return {"main_meat": [], "semi_meat": [], "veggie": []}
    except json.JSONDecodeError:
        # 如果 JSON 格式错误，显示错误提示
        st.error("❌ 菜品数据文件格式错误，请检查 dishes.json 文件！")
        return {"main_meat": [], "semi_meat": [], "veggie": []}

# ==================== 核心功能函数 ====================

def filter_dishes(dishes, no_lamb=False, no_spicy=False):
    """
    根据用户偏好过滤菜品
    
    参数:
        dishes: 菜品列表，每个菜品是字典，包含 name, has_lamb, has_spicy
        no_lamb: 是否不吃羊肉
        no_spicy: 是否不吃辣
    
    返回:
        过滤后的菜品列表
    """
    filtered = dishes.copy()
    
    # 如果不吃羊肉，过滤掉包含羊肉的菜品
    if no_lamb:
        filtered = [d for d in filtered if not d.get("has_lamb", False)]
    
    # 如果不吃辣，过滤掉辣的菜品
    if no_spicy:
        filtered = [d for d in filtered if not d.get("has_spicy", False)]
    
    return filtered

def generate_weekly_menu(no_lamb=False, no_spicy=False):
    """
    生成一周的菜单（周一到周五）
    优化版：避免连续两天吃同一道菜，添加容错处理
    
    就像核保时要检查"连续出险记录"一样，我们要确保不会连续两天吃一样的菜
    
    参数:
        no_lamb: 是否不吃羊肉
        no_spicy: 是否不吃辣
    
    返回:
        包含5天菜单的列表，每天包含 main_meat, semi_meat, veggie 三个菜品
        如果过滤条件太严格导致无菜可选，返回 None
    """
    # 从 JSON 文件加载菜品数据
    dishes = load_dishes()
    
    # 过滤菜品
    main_meat_filtered = filter_dishes(dishes["main_meat"], no_lamb, no_spicy)
    semi_meat_filtered = filter_dishes(dishes["semi_meat"], no_lamb, no_spicy)
    veggie_filtered = filter_dishes(dishes["veggie"], no_lamb, no_spicy)
    
    # ===== 容错处理：检查是否有足够的菜品 =====
    # 就像核保时检查"可承保额度"一样，确保有足够的菜品可选
    if len(main_meat_filtered) == 0 or len(semi_meat_filtered) == 0 or len(veggie_filtered) == 0:
        # 如果某个类别完全没有菜品，返回 None（让调用者显示友好提示）
        return None
    
    # 用于跟踪已使用的菜品，确保不重复（就像理赔记录一样）
    used_dishes = set()
    
    # 用于记录"昨天"的菜品，避免连续两天吃一样的
    # 就像保险公司会记录"上一次理赔时间"一样
    yesterday_dishes = {"main_meat": None, "semi_meat": None, "veggie": None}
    
    weekly_menu = []
    days = ["周一", "周二", "周三", "周四", "周五"]
    
    for day in days:
        # ===== 第一步：找出"可用的菜品"（排除已使用的） =====
        main_meat_available = [d for d in main_meat_filtered if d["name"] not in used_dishes]
        semi_meat_available = [d for d in semi_meat_filtered if d["name"] not in used_dishes]
        veggie_available = [d for d in veggie_filtered if d["name"] not in used_dishes]
        
        # ===== 第二步：如果某个类别没有未使用的菜品了，需要重置 =====
        # 就像"赔付额度用完了，需要续保"一样
        if not main_meat_available:
            used_dishes -= {d["name"] for d in main_meat_filtered}  # 清空这个类别的"已使用"记录
            main_meat_available = main_meat_filtered.copy()
            # ===== 关键优化：避免"今天的菜"等于"昨天的菜" =====
            if yesterday_dishes["main_meat"] and len(main_meat_available) > 1:
                # 如果昨天吃过某道菜，今天就不选它（除非只剩这一道菜了）
                main_meat_available = [d for d in main_meat_available if d["name"] != yesterday_dishes["main_meat"]]
        
        if not semi_meat_available:
            used_dishes -= {d["name"] for d in semi_meat_filtered}
            semi_meat_available = semi_meat_filtered.copy()
            if yesterday_dishes["semi_meat"] and len(semi_meat_available) > 1:
                semi_meat_available = [d for d in semi_meat_available if d["name"] != yesterday_dishes["semi_meat"]]
        
        if not veggie_available:
            used_dishes -= {d["name"] for d in veggie_filtered}
            veggie_available = veggie_filtered.copy()
            if yesterday_dishes["veggie"] and len(veggie_available) > 1:
                veggie_available = [d for d in veggie_available if d["name"] != yesterday_dishes["veggie"]]
        
        # ===== 第三步：从可用菜品中随机选择 =====
        main_meat = random.choice(main_meat_available)
        semi_meat = random.choice(semi_meat_available)
        veggie = random.choice(veggie_available)
        
        # ===== 第四步：记录已使用的菜品和"昨天"的菜品 =====
        used_dishes.add(main_meat["name"])
        used_dishes.add(semi_meat["name"])
        used_dishes.add(veggie["name"])
        
        yesterday_dishes["main_meat"] = main_meat["name"]
        yesterday_dishes["semi_meat"] = semi_meat["name"]
        yesterday_dishes["veggie"] = veggie["name"]
        
        # ===== 第五步：添加到周菜单 =====
        weekly_menu.append({
            "day": day,
            "main_meat": main_meat["name"],
            "semi_meat": semi_meat["name"],
            "veggie": veggie["name"]
        })
    
    return weekly_menu

# ==================== 主界面 ====================

def main():
    # 标题
    st.markdown('<h1 class="main-title">🍽️ 每周菜谱生成器 🍽️</h1>', unsafe_allow_html=True)
    st.markdown("---")
    
    # 侧边栏 - 用户偏好设置
    with st.sidebar:
        st.header("⚙️ 偏好设置")
        st.markdown("---")
        
        # 不吃羊肉选项
        no_lamb = st.checkbox("🐑 不吃羊肉", value=False, help="勾选后将过滤掉所有包含羊肉的菜品")
        
        # 不吃辣选项
        no_spicy = st.checkbox("🌶️ 不吃辣", value=False, help="勾选后将过滤掉所有辣的菜品")
        
        st.markdown("---")
        st.markdown("### 📋 菜单说明")
        st.markdown("""
        - **大荤**：高蛋白肉类主菜
        - **中荤**：蛋奶类或小荤菜
        - **素菜**：健康清淡蔬菜
        
        每天包含：1个大荤 + 1个中荤 + 1个素菜
        """)
        
        st.markdown("---")
        st.markdown("### 💡 使用提示")
        st.markdown("""
        1. 设置您的饮食偏好
        2. 点击"生成本周菜单"按钮
        3. 查看生成的周一到周五菜单
        4. 可以多次点击生成不同组合
        """)
    
    # 主内容区
    # 生成按钮
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        if st.button("🎲 生成本周菜单", use_container_width=True):
            # 生成菜单
            weekly_menu = generate_weekly_menu(no_lamb=no_lamb, no_spicy=no_spicy)
            
            # ===== 容错处理：如果过滤条件太严格导致无菜可选 =====
            # 就像核保时"风险太高无法承保"，但我们要友好地告诉客户原因
            if weekly_menu is None:
                st.session_state['menu_generated'] = False
                st.session_state['error_message'] = True
                st.error("😅 亲爱的，您的筛选条件有点严格哦！")
                st.warning("""
                ### 💡 建议：
                - 如果您勾选了"不吃羊肉"和"不吃辣"，可能会导致某些菜品类别没有菜可选
                - 请尝试放宽一些条件，比如取消"不吃辣"的勾选
                - 或者我们可以考虑增加更多菜品到菜单库中
                
                **就像保险一样，筛选条件太多可能会"无法承保"哦~ 😊**
                """)
            else:
                # 保存到session state，以便刷新后仍能看到
                st.session_state['weekly_menu'] = weekly_menu
                st.session_state['menu_generated'] = True
                st.session_state['error_message'] = False
    
    # 显示生成的菜单
    if st.session_state.get('menu_generated', False):
        st.markdown("---")
        st.markdown("### 📅 本周菜单")
        
        weekly_menu = st.session_state.get('weekly_menu', [])
        
        # ===== 手机适配：每天一个大卡片 =====
        # 就像给宝宝换尿布要铺开整张一样，让每天的菜单占满整个屏幕宽度
        for menu_day in weekly_menu:
            # 构建HTML卡片（不使用HTML注释，避免渲染问题）
            card_html = f'''
            <div style="background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 1.5rem; border-radius: 15px; margin: 1rem 0; box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2); color: white;">
                <div style="font-size: 1.8rem; font-weight: bold; margin-bottom: 1rem; text-align: center; color: #FFD93D; text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);">📆 {menu_day['day']}</div>
                <div style="background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%); padding: 1.2rem; border-radius: 10px; margin: 0.8rem 0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
                    <div style="font-size: 1rem; opacity: 0.9; margin-bottom: 0.3rem;">🥩 大荤</div>
                    <div style="font-size: 1.4rem; font-weight: bold;">{menu_day['main_meat']}</div>
                </div>
                <div style="background: linear-gradient(135deg, #4ECDC4 0%, #6EDDD6 100%); padding: 1.2rem; border-radius: 10px; margin: 0.8rem 0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
                    <div style="font-size: 1rem; opacity: 0.9; margin-bottom: 0.3rem;">🥚 中荤</div>
                    <div style="font-size: 1.4rem; font-weight: bold;">{menu_day['semi_meat']}</div>
                </div>
                <div style="background: linear-gradient(135deg, #95E1D3 0%, #B5F0E8 100%); padding: 1.2rem; border-radius: 10px; margin: 0.8rem 0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);">
                    <div style="font-size: 1rem; opacity: 0.9; margin-bottom: 0.3rem;">🥬 素菜</div>
                    <div style="font-size: 1.4rem; font-weight: bold;">{menu_day['veggie']}</div>
                </div>
            </div>
            '''
            st.markdown(card_html, unsafe_allow_html=True)
        
        # 底部提示
        st.markdown("---")
        st.info("💡 提示：可以多次点击生成按钮，获取不同的菜单组合！")
    
    else:
        # 初始状态提示
        st.markdown("""
        <div style="text-align: center; padding: 3rem; color: #666;">
            <h2>👋 欢迎使用每周菜谱生成器！</h2>
            <p style="font-size: 1.2rem;">请在侧边栏设置您的饮食偏好，然后点击上方按钮生成菜单</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()





