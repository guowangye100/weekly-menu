"""
每周菜谱生成器
使用 Streamlit 创建的网页应用，用于生成周一到周五的健康菜谱
"""

import streamlit as st
import random
from datetime import datetime

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

# ==================== 菜单数据定义 ====================

# 大荤类（main_meat）- 北方口味，高蛋白，偏咸鲜
MAIN_MEAT_DISHES = [
    {"name": "葱爆羊肉", "has_lamb": True, "has_spicy": False},
    {"name": "红烧排骨", "has_lamb": False, "has_spicy": False},
    {"name": "酱牛肉", "has_lamb": False, "has_spicy": False},
    {"name": "宫保鸡丁", "has_lamb": False, "has_spicy": True},
    {"name": "溜肉段", "has_lamb": False, "has_spicy": False},
    {"name": "糖醋里脊", "has_lamb": False, "has_spicy": False},
    {"name": "红烧肉", "has_lamb": False, "has_spicy": False},
    {"name": "鱼香肉丝", "has_lamb": False, "has_spicy": True},
    {"name": "回锅肉", "has_lamb": False, "has_spicy": True},
    {"name": "京酱肉丝", "has_lamb": False, "has_spicy": False},
    {"name": "红烧带鱼", "has_lamb": False, "has_spicy": False},
    {"name": "糖醋鱼", "has_lamb": False, "has_spicy": False},
    {"name": "红烧鸡块", "has_lamb": False, "has_spicy": False},
    {"name": "水煮肉片", "has_lamb": False, "has_spicy": True},
    {"name": "干煸豆角", "has_lamb": False, "has_spicy": True},
]

# 中荤类（semi_meat）- 蛋奶类，高蛋白
SEMI_MEAT_DISHES = [
    {"name": "西红柿炒蛋", "has_lamb": False, "has_spicy": False},
    {"name": "木须肉", "has_lamb": False, "has_spicy": False},
    {"name": "肉末茄子", "has_lamb": False, "has_spicy": False},
    {"name": "麻婆豆腐", "has_lamb": False, "has_spicy": True},
    {"name": "青椒肉丝", "has_lamb": False, "has_spicy": True},
    {"name": "鱼香茄子", "has_lamb": False, "has_spicy": True},
    {"name": "韭菜炒蛋", "has_lamb": False, "has_spicy": False},
    {"name": "蒜苔炒肉", "has_lamb": False, "has_spicy": False},
    {"name": "豆角炒肉", "has_lamb": False, "has_spicy": False},
    {"name": "尖椒炒蛋", "has_lamb": False, "has_spicy": True},
    {"name": "土豆丝炒肉", "has_lamb": False, "has_spicy": False},
    {"name": "芹菜炒肉", "has_lamb": False, "has_spicy": False},
    {"name": "洋葱炒蛋", "has_lamb": False, "has_spicy": False},
    {"name": "干煸四季豆", "has_lamb": False, "has_spicy": True},
    {"name": "蚂蚁上树", "has_lamb": False, "has_spicy": True},
]

# 素菜类（veggie）- 健康清淡
VEGGIE_DISHES = [
    {"name": "地三鲜（少油）", "has_lamb": False, "has_spicy": False},
    {"name": "凉拌土豆丝", "has_lamb": False, "has_spicy": False},
    {"name": "蒜蓉西兰花", "has_lamb": False, "has_spicy": False},
    {"name": "醋溜白菜", "has_lamb": False, "has_spicy": False},
    {"name": "清炒小白菜", "has_lamb": False, "has_spicy": False},
    {"name": "蒜蓉菠菜", "has_lamb": False, "has_spicy": False},
    {"name": "清炒豆芽", "has_lamb": False, "has_spicy": False},
    {"name": "凉拌黄瓜", "has_lamb": False, "has_spicy": False},
    {"name": "清炒时蔬", "has_lamb": False, "has_spicy": False},
    {"name": "蒜蓉生菜", "has_lamb": False, "has_spicy": False},
    {"name": "清炒豆角", "has_lamb": False, "has_spicy": False},
    {"name": "凉拌豆腐丝", "has_lamb": False, "has_spicy": False},
    {"name": "清炒冬瓜", "has_lamb": False, "has_spicy": False},
    {"name": "蒜蓉空心菜", "has_lamb": False, "has_spicy": False},
    {"name": "凉拌海带丝", "has_lamb": False, "has_spicy": False},
]

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
    
    参数:
        no_lamb: 是否不吃羊肉
        no_spicy: 是否不吃辣
    
    返回:
        包含5天菜单的列表，每天包含 main_meat, semi_meat, veggie 三个菜品
    """
    # 过滤菜品
    main_meat_filtered = filter_dishes(MAIN_MEAT_DISHES, no_lamb, no_spicy)
    semi_meat_filtered = filter_dishes(SEMI_MEAT_DISHES, no_lamb, no_spicy)
    veggie_filtered = filter_dishes(VEGGIE_DISHES, no_lamb, no_spicy)
    
    # 检查是否有足够的菜品
    if len(main_meat_filtered) < 5:
        st.warning("⚠️ 大荤类菜品不足，可能无法生成完整菜单")
    if len(semi_meat_filtered) < 5:
        st.warning("⚠️ 中荤类菜品不足，可能无法生成完整菜单")
    if len(veggie_filtered) < 5:
        st.warning("⚠️ 素菜类菜品不足，可能无法生成完整菜单")
    
    # 用于跟踪已使用的菜品，确保不重复
    used_dishes = set()
    
    weekly_menu = []
    days = ["周一", "周二", "周三", "周四", "周五"]
    
    for day in days:
        # 从每个类别中随机选择菜品，确保不重复
        main_meat_available = [d for d in main_meat_filtered if d["name"] not in used_dishes]
        semi_meat_available = [d for d in semi_meat_filtered if d["name"] not in used_dishes]
        veggie_available = [d for d in veggie_filtered if d["name"] not in used_dishes]
        
        # 如果某个类别没有未使用的菜品，则从全部菜品中随机选择（允许重复）
        if not main_meat_available:
            main_meat_available = main_meat_filtered
        if not semi_meat_available:
            semi_meat_available = semi_meat_filtered
        if not veggie_available:
            veggie_available = veggie_filtered
        
        # 随机选择菜品
        main_meat = random.choice(main_meat_available)
        semi_meat = random.choice(semi_meat_available)
        veggie = random.choice(veggie_available)
        
        # 记录已使用的菜品
        used_dishes.add(main_meat["name"])
        used_dishes.add(semi_meat["name"])
        used_dishes.add(veggie["name"])
        
        # 添加到周菜单
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
            
            # 保存到session state，以便刷新后仍能看到
            st.session_state['weekly_menu'] = weekly_menu
            st.session_state['menu_generated'] = True
    
    # 显示生成的菜单
    if st.session_state.get('menu_generated', False):
        st.markdown("---")
        st.markdown("### 📅 本周菜单")
        
        weekly_menu = st.session_state.get('weekly_menu', [])
        
        # 为每一天创建卡片展示
        for menu_day in weekly_menu:
            # 使用容器创建卡片效果
            with st.container():
                # 日期标题
                st.markdown(f"### {menu_day['day']} 📆")
                
                # 使用列布局展示菜品
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #FF6B6B 0%, #FF8E8E 100%); 
                                padding: 1rem; border-radius: 10px; text-align: center; 
                                color: white; font-weight: bold; font-size: 1.1rem;">
                        🥩 大荤<br>{menu_day['main_meat']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #4ECDC4 0%, #6EDDD6 100%); 
                                padding: 1rem; border-radius: 10px; text-align: center; 
                                color: white; font-weight: bold; font-size: 1.1rem;">
                        🥚 中荤<br>{menu_day['semi_meat']}
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div style="background: linear-gradient(135deg, #95E1D3 0%, #B5F0E8 100%); 
                                padding: 1rem; border-radius: 10px; text-align: center; 
                                color: white; font-weight: bold; font-size: 1.1rem;">
                        🥬 素菜<br>{menu_day['veggie']}
                    </div>
                    """, unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
        
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
