import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import warnings
warnings.filterwarnings('ignore')
import requests
from io import BytesIO
import random
import squarify as sqr

st.set_page_config(page_icon='🚂',layout='wide')
st.set_option('deprecation.showPyplotGlobalUse', False)

def ego_resources(series,sin,numofsin):
    sincount=numofsin
    if series['Skill 1 Sin']==sin:
        sincount+=3
    if series['Skill 2 Sin']==sin:
        sincount+=2
    if series['Skill 3 Sin']==sin:
        sincount+=1
    return sincount

def ego_cost(series,sin,num_of_sin_cost):
    sincost=num_of_sin_cost
    for i in range(len(series['Sin Cost Type'])):
        if series['Sin Cost Type'][i]==sin:
            sincost+=int(series['Number of Sin Cost'][i])
    return sincost
    

def display(sincount,sincost,sin,link):
    response = requests.get(link)
    img = Image.open(BytesIO(response.content))
    st.image(image=img,width=100)
    st.markdown(f'{sin}: :green[{sincount}]/**{sincost}**')
    return

def ego_display(ego,egoli):
    egoli.append(ego)
    egolist_df=ego_df[ego_df['Name']==ego]
    egolist_df.drop_duplicates(subset='E.G.O',keep='first',inplace=True)
    egolist_df.reset_index(drop=True,inplace=True)
    for index2,row2 in egolist_df.iterrows():
        response = requests.get(row2["Image"])
        img = Image.open(BytesIO(response.content))
        st.image(img, width=150)
        with st.expander('Sin Cost'):
            st.write(row2['Sin Cost'])
    return

def ego_display_randomize(ego,egoli):
    egoli.append(ego)
    egolist_df=ego_df[ego_df['Name']==ego]
    egolist_df.drop_duplicates(subset='E.G.O',keep='first',inplace=True)
    egolist_df.reset_index(drop=True,inplace=True)
    for index2,row2 in egolist_df.iterrows():
        response = requests.get(row2["Image"])
        img = Image.open(BytesIO(response.content))
        cap = st.write(row2['Name'])
        st.image(img, caption=cap, width=150)
        with st.expander('Sin Cost'):
            st.write(row2['Sin Cost'])
    return
id_df=pd.read_csv('data/id_list.csv', index_col=0)
ego_df=pd.read_csv('data/ego_list.csv', index_col=0)
id_df['Rarity']=id_df['Rarity'].astype(str)

menu=('Database','Teambuilder','Statistics')
option=st.sidebar.selectbox(label='What do you want to do?',label_visibility='hidden',options=menu)

st.title(option)

if option==menu[0]:
    tab1,tab2=st.tabs(['Identity','E.G.O'])
    with tab1:
        st.subheader('Filters')
        id_rarity=st.multiselect('Rarity:',options=['O','OO','OOO'])
        id_sin=st.multiselect('Sin:',options=['Wrath','Lust','Sloth','Gluttony','Gloom','Pride','Envy'],key='id_sin')
        id_type=st.multiselect('Type:',options=['Slash','Pierce','Blunt'],key='id_type')
        id_sinner=st.multiselect('Sinner:',options=['Yi Sang','Faust','Don Quixote','Ryoshu','Meursault','Hong Lu','Heathcliff','Ishmael','Rodion','Sinclair','Outis','Gregor'],key='id_sinner')
        if st.button('Search'):
            # rarity_df=id_df[id_df['Rarity'].isin(id_rarity)]
            # sin_df=id_df[(id_df['Skill 1 Sin'].isin(id_sin)) | (id_df['Skill 2 Sin'].isin(id_sin)) | (id_df['Skill 3 Sin'].isin(id_sin))]
            # type_df=id_df[(id_df['Skill 1 Type'].isin(id_type)) | (id_df['Skill 2 Type'].isin(id_type)) | (id_df['Skill 3 Type'].isin(id_type))]
            # sinner_df=id_df[id_df['Sinner'].isin(id_sinner)]
            selected_id_df=id_df[(id_df['Rarity'].isin(id_rarity))
                               &((id_df['Skill 1 Sin'].isin(id_sin)) | (id_df['Skill 2 Sin'].isin(id_sin)) | (id_df['Skill 3 Sin'].isin(id_sin)))
                               &((id_df['Skill 1 Type'].isin(id_type)) | (id_df['Skill 2 Type'].isin(id_type)) | (id_df['Skill 3 Type'].isin(id_type)))
                               &(id_df['Sinner'].isin(id_sinner))]
            selected_id_df.reset_index(drop=True, inplace=True)
            colu=st.columns(2)
            for index,row in selected_id_df.iterrows():
                response = requests.get(row["Image"])
                img = Image.open(BytesIO(response.content))
                with colu[index%2]:
                    cap = st.write(f"[{row['ID']}] {row['Sinner']}")
                    st.image(img, caption=cap, width=150)
                    with st.expander("Info"):
                        list_col = list(id_df.columns)
                        list_col.remove('Image')
                        for col in list_col:
                            st.write(f"- {col}: {row[col]}")
    with tab2:
        st.subheader('Filters')
        ego_tier=st.multiselect('Tier:',options=['ZAYIN','TETH','HE'])
        ego_sin=st.multiselect('Sin:',options=['Wrath','Lust','Sloth','Gluttony','Gloom','Pride','Envy'],key='ego_sin')
        ego_type=st.multiselect('Type:',options=['Slash','Pierce','Blunt'],key='ego_type')
        ego_sinner=st.multiselect('Sinner:',options=['Yi Sang','Faust','Don Quixote','Ryoshu','Meursault','Hong Lu','Heathcliff','Ishmael','Rodion','Sinclair','Outis','Gregor'],key='ego_sinner')
        if st.button('Search '):
            selected_ego_df=ego_df[(ego_df['Tier'].isin(ego_tier))
                                   &(ego_df['Sin'].isin(ego_sin))
                                   &(ego_df['Type'].isin(ego_type))
                                   &(ego_df['Sinner'].isin(ego_sinner))]
            selected_ego_df.reset_index(drop=True, inplace=True)
            for index,row in selected_ego_df.iterrows():
                if row['Image']!=' ':
                    response=requests.get(row['Image'])
                    img=Image.open(BytesIO(response.content))
                    cap = st.write(f"[{row['E.G.O']}]\n {row['Sinner']}")
                    st.image(img, caption=cap, width=150)
                with st.expander("Info"):
                    list_col = list(ego_df.columns)
                    list_col.remove('Image')
                    for col in list_col:
                        st.write(f"- {col}: {row[col]}")

if option==menu[1]:
    id_df['Name']='['+id_df['ID']+']'+' '+id_df['Sinner']
    ego_df['Name']='['+ego_df['E.G.O']+']'+' '+ego_df['Sinner']
    ego_df['Sin Cost Type']=ego_df['Sin Cost'].str.findall('([^\s]+)\sx[^,]+')
    ego_df['Number of Sin Cost']=ego_df['Sin Cost'].str.findall('[^\s]+\sx([^,]+)')
    list_id=[]
    egoli=[]
    list_id=st.multiselect('Choose 5 Identities:',id_df['Name'].unique())
    cols=st.columns(5)
    if len(list_id)>5:
        st.warning('Too many IDs chosen.',icon='❗')
    else:
        list_id_df=id_df[id_df['Name'].isin(list_id)]
        list_id_df.reset_index(drop=True,inplace=True)
        for index,row in list_id_df.iterrows():
            response = requests.get(row["Image"])
            img = Image.open(BytesIO(response.content))
            with cols[index%5]:
                st.image(img, width=150)
                with st.expander('Skills'):
                    st.write(f"3x {row['Skill 1 Sin']}")
                    st.write(f"2x {row['Skill 2 Sin']}")
                    st.write(f"1x {row['Skill 3 Sin']}")
                zayin_ego=st.selectbox('Choose your E.G.O:',ego_df[(ego_df['Sinner']==row['Sinner']) & (ego_df['Tier']=='ZAYIN')]['Name'].unique(),key='zayin'+str(index))
                ego_display(zayin_ego,egoli)
                teth_ego=st.selectbox(label='Choose your E.G.O:',label_visibility='hidden',options=ego_df[(ego_df['Sinner']==row['Sinner']) & (ego_df['Tier']=='TETH')]['Name'].unique(),key='teth'+str(index))
                ego_display(teth_ego,egoli)
                he_ego=st.selectbox(label='Choose your E.G.O:',label_visibility='hidden',options=ego_df[(ego_df['Sinner']==row['Sinner']) & (ego_df['Tier']=='HE')]['Name'].unique(),key='he'+str(index))
                ego_display(he_ego,egoli)
        
    if st.button('Randomize'):
        columnial=st.columns(5)
        list_id=[]
        egoli=[]
        for i in range(5):
            chosen=random.randint(0,id_df.shape[0]-1)
            list_id.append(id_df['Name'][chosen])
            id_df.drop(index=chosen,axis=0)
        list_id_df=id_df[id_df['Name'].isin(list_id)]
        list_id_df.reset_index(drop=True,inplace=True)
        for index,row in list_id_df.iterrows():
            response = requests.get(row["Image"])
            img = Image.open(BytesIO(response.content))
            with columnial[index%5]:
                cap = st.write(f"{row['Name']}")
                st.image(img,caption=cap,width=150)
                with st.expander('Skills'):
                    st.write(f"3x {row['Skill 1 Sin']}")
                    st.write(f"2x {row['Skill 2 Sin']}")
                    st.write(f"1x {row['Skill 3 Sin']}")
                zayin_ego=random.choice(ego_df[(ego_df['Sinner']==row['Sinner']) & (ego_df['Tier']=='ZAYIN')]['Name'].unique())
                ego_display_randomize(zayin_ego,egoli)
                teth_ego=random.choice(ego_df[(ego_df['Sinner']==row['Sinner']) & (ego_df['Tier']=='TETH')]['Name'].unique())
                ego_display_randomize(teth_ego,egoli)
                if row['Sinner']=='Sinclair':
                    pass
                else:
                    he_ego=random.choice(ego_df[(ego_df['Sinner']==row['Sinner']) & (ego_df['Tier']=='HE')]['Name'].unique())
                    ego_display_randomize(he_ego,egoli)
    egoli_df=ego_df[ego_df['Name'].isin(egoli)]
    egoli_df.drop_duplicates(subset='E.G.O',keep='first',inplace=True)
    egoli_df.reset_index(drop=True,inplace=True)
    wrath,lust,sloth,gluttony,gloom,pride,envy=st.columns(7)   
    with wrath:
        wrath_count=0
        wrath_cost=0
        for index,row in list_id_df.iterrows():
            wrath_count=ego_resources(row,'Wrath',wrath_count)
        for index2,row2 in egoli_df.iterrows():
            wrath_cost=ego_cost(row2,'Wrath',wrath_cost)
        display(wrath_count,wrath_cost,'Wrath','https://www.prydwen.gg/static/166d55532f6dd4b802b309cd3ed5ecbd/927d1/affinity_wrath_big.webp')
    with lust:
        lust_count=0
        lust_cost=0
        for index,row in list_id_df.iterrows():
            lust_count=ego_resources(row,'Lust',lust_count)
        for index2,row2 in egoli_df.iterrows():
            lust_cost=ego_cost(row2,'Lust',lust_cost)
        display(lust_count,lust_cost,'Lust','https://www.prydwen.gg/static/75aca67c0ad4ab498e1d88846668555e/927d1/affinity_lust_big.webp')
    with sloth:
        sloth_count=0
        sloth_cost=0
        for index,row in list_id_df.iterrows():
            sloth_count=ego_resources(row,'Sloth',sloth_count)
        for index2,row2 in egoli_df.iterrows():
            sloth_cost=ego_cost(row2,'Sloth',sloth_cost)
        display(sloth_count,sloth_cost,'Sloth','https://www.prydwen.gg/static/6233cebf8c3f4cacef41d7651399fe51/927d1/affinity_sloth_big.webp')
    with gluttony:
        gluttony_count=0
        gluttony_cost=0
        for index,row in list_id_df.iterrows():
            gluttony_count=ego_resources(row,'Gluttony',gluttony_count)
        for index2,row2 in egoli_df.iterrows():
            gluttony_cost=ego_cost(row2,'Gluttony',gluttony_cost)
        display(gluttony_count,gluttony_cost,'Gluttony','https://www.prydwen.gg/static/1b93c7d1d5ba253d7aad56b894736749/927d1/affinity_gluttony_big.webp')
    with gloom:
        gloom_count=0
        gloom_cost=0
        for index,row in list_id_df.iterrows():
            gloom_count=ego_resources(row,'Gloom',gloom_count)
        for index2,row2 in egoli_df.iterrows():
            gloom_cost=ego_cost(row2,'Gloom',gloom_cost)
        display(gloom_count,gloom_cost,'Gloom','https://www.prydwen.gg/static/0b20159a49d1d901c0f1eb7740b5f6b8/927d1/affinity_gloom_big.webp')
    with pride:
        pride_count=0
        pride_cost=0
        for index,row in list_id_df.iterrows():
            pride_count=ego_resources(row,'Pride',pride_count)
        for index2,row2 in egoli_df.iterrows():
            pride_cost=ego_cost(row2,'Pride',pride_cost)
        display(pride_count,pride_cost,'Pride','https://www.prydwen.gg/static/d3917da09566620d6c42bbf08a0e330d/927d1/affinity_pride_big.webp')
    with envy:
        envy_count=0
        envy_cost=0
        for index,row in list_id_df.iterrows():
            envy_count=ego_resources(row,'Envy',envy_count)
        for index2,row2 in egoli_df.iterrows():
            envy_cost=ego_cost(row2,'Envy',envy_cost)
        display(envy_count,envy_cost,'Envy','https://www.prydwen.gg/static/424b29e0224b4e7188717698c9b8903a/927d1/affinity_envy_big.webp')
if option==menu[2]:
    tab3,tab4=st.tabs(['IDs','E.G.O'])
    with tab3:
        st.write('### Boxplot')
        with st.expander('See more...'):
            cat1=st.selectbox('Choose a skill to view:',options=['Skill 1','Skill 2','Skill 3'],key='bxplt')
            cat2=st.selectbox('Sort by?',options=['Minimum Value','Maximum Value','No. of Coins'])
            category=cat1+' '+cat2
            sns.boxplot(data=id_df,y=category)
            plt.title(f'Average {category}')
            st.pyplot()
        
        st.write('### Treemap')
        with st.expander('See more...'):
            cate1=st.selectbox('Choose a skill to view:', options=['Skill 1','Skill 2','Skill 3'],key='sqrplt')
            cate2=st.selectbox('Sort by?',options=['Sin','Type'])
            total_cate=cate1+' '+cate2
            df_group = id_df.value_counts(total_cate, sort=False).to_frame().reset_index()
            
            st.dataframe(df_group)
            labels = df_group.apply(lambda x: str(x.iloc[0]) + ': ' + str(x.iloc[1]), axis=1)
            plt.figure(figsize=(12, 7))
            sqr.plot(sizes=df_group['count'], label=labels, color=sns.color_palette('GnBu'))
            plt.title(f'Number of {cate1} sort by {cate2}')
            plt.axis('off')
            st.pyplot()
        with st.expander('See more...'):
            cat=st.selectbox('Sort by?',options=['Season','Rarity','Sinner'])
            df_grouper = id_df.value_counts(cat, sort=False).to_frame().reset_index()
            
            labelss = df_grouper.apply(lambda x: str(x[0]) + ': ' + str(x[1]), axis=1)
            plt.figure(figsize=(12, 7))
            sqr.plot(sizes=df_grouper['count'], label=labelss, color=sns.color_palette('YlOrRd',10))
            plt.title(f'Number of Identites sort by {cat}')
            plt.axis('off')
            st.pyplot()
    with tab4:
        st.write('### Boxplot')
        with st.expander('See more...'):
            categ=st.selectbox(label='Sort by?',options=['Minimum Value','Maximum Value','Sanity Cost'],key='ego_bxplt')
            sns.boxplot(data=ego_df,y=categ)
            plt.title(f'Average {categ}')
            st.pyplot()
        
        st.write('### Treemap')
        with st.expander('See more...'):
            cag=st.selectbox('Sort by?',options=['Season','Tier','Sinner','Version','Sin','Type','Sanity Cost'])
            df_groupers = ego_df.value_counts(cag, sort=False).to_frame().reset_index()
            
            labe = df_groupers.apply(lambda x: str(x[0]) + ': ' + str(x[1]), axis=1)
            plt.figure(figsize=(12, 7))
            sqr.plot(sizes=df_groupers['count'], label=labe, color=sns.color_palette('RdPu',10))
            plt.title(f'Number of E.G.Os sort by {cag}')
            plt.axis('off')
            st.pyplot()
