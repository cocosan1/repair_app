import pandas as pd
import streamlit as st
import webbrowser
import glob
from PIL import Image

#st
st.set_page_config(page_title='修理見積もり')
st.markdown('#### ソファ修理見積もりアプリ')

df_sofa = pd.read_excel('sofa.xlsx')
df_base = df_sofa.copy()

df_base['A-S/A/B'] = df_base['A-S/A/B'].astype(str)
df_base['C'] = df_base['C'].astype(str)
df_base['E'] = df_base['E'].astype(str)
df_base['本革B'] = df_base['本革B'].astype(str)
df_base['本革D'] = df_base['本革D'].astype(str)

df_base['A-S/A/B'] = df_base['A-S/A/B'].map(lambda x: x.replace(',', ''))
df_base['C'] = df_base['C'].map(lambda x: x.replace(',', ''))
df_base['E'] = df_base['E'].map(lambda x: x.replace(',', ''))
df_base['本革B'] = df_base['本革B'].map(lambda x: x.replace(',', ''))
df_base['本革D'] = df_base['本革D'].map(lambda x: x.replace(',', ''))

df_base['A-S/A/B'] = df_base['A-S/A/B'].astype(int)
df_base['C'] = df_base['C'].astype(int)
df_base['E'] = df_base['E'].astype(int)
df_base['本革B'] = df_base['本革B'].astype(int)
df_base['本革D'] = df_base['本革D'].astype(int)

df_base['A-S/A/B'] = df_base['A-S/A/B'].map(lambda x: '{:,}'.format(x))
df_base['C'] = df_base['C'].map(lambda x: '{:,}'.format(x))
df_base['E'] = df_base['E'].map(lambda x: '{:,}'.format(x))
df_base['本革B'] = df_base['本革B'].map(lambda x: '{:,}'.format(x))
df_base['本革D'] = df_base['本革D'].map(lambda x: '{:,}'.format(x))

#itemリストの作成
item_list = df_base['品番'].unique()
item_list2 = sorted(item_list)

#リストに1行目を挿入　すぐに見積もりが始まらないように
item_list2.insert(0, '--品番を選択--')


# *** selectbox item***
st.sidebar.markdown('#### ソファ見積')
selected_item = st.sidebar.selectbox(
    '品番:',
    item_list2,   
)    


if selected_item == '--品番を選択--':
    img_menu = Image.open('img_sofa/F1001.jpg')
    st.image(img_menu)
    st.write('品番を選択してください')


if not selected_item == '--品番を選択--':

    col1, col2, col3 = st.columns(3)
    with col1:
        #シリーズ名の表示
        df_selected = df_base[df_base['品番']==selected_item]
        series = df_selected.iat[0, 0]
        # st.caption('シリーズ名')
        st.caption(series)

    with col2:    
        #材種の表示
        wood_name = df_selected.iat[0, 8]
        # st.markdown('###### 材種名')
        st.caption(wood_name)

    with col3:
        #imagフォルダ内のファイル名リスト取得
        files = glob.glob("img_sofa\*.jpg")
        jpg_name = f'img_sofa\{selected_item}.jpg'
        if jpg_name in files:
            st.image(f'img_sofa\{selected_item}.jpg', width=200) 

    #品番でdfの絞り込み
    df_selected = df_base[df_base['品番']==selected_item]

    #布ランクリストの作成
    df_selected2 = df_selected[['品番', '部品', 'A-S/A/B', 'C', 'E', '本革B', '本革D']]

    #クッション価格一覧表示
    st.markdown('###### 張替え料金一覧')
    st.table(df_selected2)

