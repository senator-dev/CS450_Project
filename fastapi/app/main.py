from fastapi import FastAPI, Path
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import json
from config import get_data
import plotly.express as px
import plotly.graph_objects as go
from enum import Enum
from plotly.subplots import make_subplots

app = FastAPI()
origins = [
    "http://localhost:5173",
    "localhost:5173",
    "http://localhost:3001",
    "localhost:3001",
    "http://54.86.127.160:80",
    "http://localhost:80"

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

data = get_data("select * from mobiles_raw")

def try_func(x):
    try:
        return float(x[:-2])
    except Exception:
        return np.nan
    
data['Mobile Weight (grams)'] = data['Mobile Weight'].apply(lambda x: x[:-1]).astype(float)
data['Launched Year'] = data['Launched Year'].astype(int)
data = data[data['RAM'] != '8GB / 12GB']
data['RAM (gb)'] = data['RAM'].apply(lambda x: x[:-2]).astype(float)
data['Battery Capacity (mah)'] = data['Battery Capacity'].apply(lambda x: x[:-3].replace(',', '')).astype(float)
data['Launched Price (USA) ($)'] = data['Launched Price (USA)'].str.replace('Not available', '').apply(lambda x: x[4:].replace(',', '') if x else None).astype(float)
data['Launched Price (Pakistan) (Rs)'] = data['Launched Price (Pakistan)'].str.replace('Not available', '').apply(lambda x: x[4:].replace(',', '') if x else None).astype(float)
data['Launched Price (India) (₹)'] = data['Launched Price (India)'].str.replace('Not available', '').apply(lambda x: x[4:].replace(',', '') if x else None).astype(float)
data['Launched Price (China) (¥)'] = data['Launched Price (China)'].str.replace('Not available', '').apply(lambda x: x[4:].replace(',', '') if x else None).astype(float)
data['Screen Size (in)'] = data['Screen Size'].apply(lambda x: x.split(',')[0].replace(' (main)', '').replace(' inches', '').replace(' (internal)', '').replace(' (unfolded)', '')).astype(float)
data = data[(data['Company Name'] != 'Nokia') & (data['Model Name'] != 'T21')]
data['Front Camera (MP)'] = data['Front Camera'].apply(try_func)
data['Back Camera (MP)'] = data['Back Camera'].apply(try_func)

company_colors = {
    'Apple': "rgb(255, 99, 71)",        # Tomato
    'Samsung': "rgb(255, 140, 0)",      # Dark Orange
    'OnePlus': "rgb(255, 69, 0)",       # Red-Orange
    'Vivo': "rgb(255, 105, 97)",        # Warm Pink
    'iQOO': "rgb(255, 165, 0)",         # Orange
    'Oppo': "rgb(255, 160, 122)",       # Light Salmon
    'Realme': "rgb(255, 120, 85)",      # Coral
    'Xiaomi': "rgb(255, 127, 80)",      # Coral
    'Lenovo': "rgb(255, 87, 51)",       # Sunset Red
    'Motorola': "rgb(255, 69, 0)",      # Red-Orange
    'Huawei': "rgb(255, 110, 74)",      # Warm Rust
    'Sony': "rgb(255, 174, 66)",        # Light Orange
    'Google': "rgb(255, 85, 0)",        # Bright Orange
    'Tecno': "rgb(255, 99, 99)",        # Light Red
    'Infinix': "rgb(255, 115, 85)",     # Warm Peach
    'Honor': "rgb(255, 92, 66)",        # Soft Red
    'POCO': "rgb(255, 132, 50)",        # Bright Apricot
    'Poco': "rgb(255, 132, 50)",        # Same as POCO
}


class FeatureName(str, Enum):
    battery = "battery"
    ram = "ram"
    weight = "weight"
    screen_size = "screen_size"
    launch_price_usa = "launch_price_usa"
    launch_price_pakistan = "launch_price_pakistan"
    launch_price_india = "launch_price_india"
    launch_price_china = "launch_price_china"
    front_camera = "front_camera"
    back_camera = "back_camera"

    @staticmethod
    def map_to(feature_name):
        return {
            "battery": "Battery Capacity (mah)",
            "ram": "RAM (gb)",
            "weight": "Mobile Weight (grams)",
            "screen_size": "Screen Size (in)",
            "launch_price_usa": "Launched Price (USA) ($)",
            "launch_price_pakistan": "Launched Price (Pakistan) (Rs)",
            "launch_price_india": "Launched Price (India) (₹)",
            "launch_price_china": "Launched Price (China) (¥)",
            "front_camera": 'Front Camera (MP)',
            "back_camera": 'Back Camera (MP)'
        }[feature_name]
    

    @staticmethod
    def small_name(feature_name):
        return {
            "Battery Capacity (mah)": 'Battery (mah)',
            "RAM (gb)": 'Ram (gb)',
            "Mobile Weight (grams)": 'Weight (g)',
            "Screen Size (in)": 'Screen (in)',
            "Launched Price (USA) ($)": 'Price ($)',
            "Launched Price (Pakistan) (Rs)": 'Price (Rs)',
            "Launched Price (India) (₹)": 'Price (₹)',
            "Launched Price (China) (¥)": 'Price (¥)',
            'Front Camera (MP)': 'F Camera (mp)',
            'Back Camera (MP)': 'B Camera (mp)'
        }[feature_name]


@app.get("/api/parallel_coordinates")
def parallel_coordinates():
    filtered_data = data.dropna(subset=[
        'RAM (gb)', 'Mobile Weight (grams)',
        'Screen Size (in)', 'Battery Capacity (mah)', 'Launched Year',
        'Back Camera (MP)', 'Front Camera (MP)'
    ])

    years = filtered_data['Launched Year']

    print(data['Company Name'].unique())

    fig = go.Figure(
        data=go.Parcoords(
            line=dict(
                color=years,
                colorscale='agsunset',
                showscale=True,
                cmin=years.min(),
                cmax=years.max()
            # ['aggrnyl', 'agsunset', 'algae', 'amp', 'armyrose', 'balance',                                                                                                                                              
            # 'blackbody', 'bluered', 'blues', 'blugrn', 'bluyl', 'brbg',
            # 'brwnyl', 'bugn', 'bupu', 'burg', 'burgyl', 'cividis', 'curl',                                                                                                                                             
            # 'darkmint', 'deep', 'delta', 'dense', 'earth', 'edge', 'electric',                                                                                                                                         
            # 'emrld', 'fall', 'geyser', 'gnbu', 'gray', 'greens', 'greys',                                                                                                                                              
            # 'haline', 'hot', 'hsv', 'ice', 'icefire', 'inferno', 'jet',                                                                                                                                                
            # 'magenta', 'magma', 'matter', 'mint', 'mrybm', 'mygbm', 'oranges',                                                                                                                                         
            # 'orrd', 'oryel', 'oxy', 'peach', 'phase', 'picnic', 'pinkyl',                                                                                                                                              
            # 'piyg', 'plasma', 'plotly3', 'portland', 'prgn', 'pubu', 'pubugn',                                                                                                                                         
            # 'puor', 'purd', 'purp', 'purples', 'purpor', 'rainbow', 'rdbu',                                                                                                                                            
            # 'rdgy', 'rdpu', 'rdylbu', 'rdylgn', 'redor', 'reds', 'solar',
            # 'spectral', 'speed', 'sunset', 'sunsetdark', 'teal', 'tealgrn',                                                                                                                                            
            # 'tealrose', 'tempo', 'temps', 'thermal', 'tropic', 'turbid',                                                                                                                                               
            # 'turbo', 'twilight', 'viridis', 'ylgn', 'ylgnbu', 'ylorbr',                                                                                                                                                
            # 'ylorrd'].
            ),
            dimensions=[
                dict(label='Ram (GB)', values=filtered_data['RAM (gb)']),
                dict(label='Weight (g)', values=filtered_data['Mobile Weight (grams)']),
                dict(label='Screen (in)', values=filtered_data['Screen Size (in)']),
                dict(label='Battery (mAh)', values=filtered_data['Battery Capacity (mah)']),
                dict(label='F Camera (mp)', values=filtered_data['Front Camera (MP)']),
                dict(label='B Camera (mp)', values=filtered_data['Back Camera (MP)']),
            ],
        )
    )

    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return json.loads(fig.to_json())

@app.get("/api/correlation_heatmap")
def correlation_heatmap():
    import plotly.graph_objects as go

    numeric_cols = [
        'Launched Year', 'RAM (gb)', 'Mobile Weight (grams)',
        'Front Camera (MP)', 'Back Camera (MP)',
        'Battery Capacity (mah)', 'Screen Size (in)',
        'Launched Price (USA) ($)', 'Launched Price (Pakistan) (Rs)',
        'Launched Price (India) (₹)', 'Launched Price (China) (¥)',
        
    ]

    column_names = [
        'Year', 'Ram', 'Weight', 'F Camera (mp)', 
        'B Camera (mp)', 'Battery', 'Screen Size', 
        '$', 'Rs', '₹', '¥'
    ]
    
    corr_data = data[numeric_cols].dropna()
    corr_matrix = corr_data.corr().round(2)
    heatmap = go.Heatmap(
        z=corr_matrix.values,
        x=column_names,
        y=column_names,
        colorscale='agsunset',
        zmin=-1,
        zmax=1,
    )


    fig = go.Figure(data=[heatmap])
    fig.update_layout(
        xaxis=dict(tickangle=-45),
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return json.loads(fig.to_json())



@app.get("/api/treemap/{feature_name}")
def treemap_feature(feature_name: FeatureName):
    feature_name = FeatureName.map_to(str(feature_name.split('.')[-1]))
    treemap_data = data.dropna(subset=[feature_name])

    labels = []
    parents = []
    values = []

    added_companies = set()

    for _, row in treemap_data.iterrows():
        company = row['Company Name']
        model = row['Model Name']
        value = row[feature_name]

        # Add company only once
        if company not in added_companies:
            labels.append(company)
            parents.append("")
            values.append(0)
            added_companies.add(company)

        labels.append(model)
        parents.append(company)
        values.append(value)

    fig = go.Figure(go.Treemap(
        labels=labels,
        parents=parents,
        values=values,
        marker=dict(colors=values, colorscale='agsunset', colorbar=dict(title=FeatureName.small_name(feature_name))),
        textinfo='label+value+percent parent'
    ))

    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return json.loads(fig.to_json())


@app.get("/api/scatter_3d/{x}/{y}/{z}")
def scatter_3d(x: FeatureName, y: FeatureName, z: FeatureName):
    x = FeatureName.map_to(x)
    y = FeatureName.map_to(y)
    z = FeatureName.map_to(z)
    df = data.dropna(subset=[x, y, z])

    df = data.dropna(subset=[x, y, z])

    fig = make_subplots(
        rows=2, cols=1,
        specs=[[{"type": "xy"}], [{"type": "scene"}]],
        row_heights=[0.4, 0.6],
        vertical_spacing=0.05,
        # subplot_titles=[f"2D Scatter: {x} vs {y}", f"3D Scatter: {x}, {y}, {z}"]
    )

    for company in df['Company Name'].unique():
        subset = df[df['Company Name'] == company]


        # 2D plot
        fig.add_trace(
            go.Scatter(
                x=subset[x],
                y=subset[y],
                mode='markers',
                name=company,
                legendgroup=company,
                text=subset['Model Name'],
                hoverinfo='text',
                marker=dict(size=6, color=company_colors[company]),
            ),
            row=1, col=1
        )

        # 3D plot
        fig.add_trace(
            go.Scatter3d(
                x=subset[x],
                y=subset[y],
                z=subset[z],
                mode='markers',
                name=company,
                legendgroup=company,
                showlegend=False,
                text=subset['Model Name'],
                hoverinfo='text',
                marker=dict(
                    size=5,
                    color=company_colors[company]
                )
            ),
            row=2, col=1
        )

    fig.update_layout(
        margin=dict(l=40, r=40, t=60, b=40),
        # scene=dict(
        #     xaxis_title=x,
        #     yaxis_title=y,
        #     zaxis_title=z
        # ),
        # xaxis=dict(title=x),
        # yaxis=dict(title=y),
    )

    return json.loads(fig.to_json())

@app.get("/api/violin_chart/{feature_name}/{year}")
def violin_chart(feature_name: FeatureName, year: int):

    feature_name = FeatureName.map_to(feature_name)

    df = data[data['Launched Year'] == year]

    df_filtered = df.dropna(subset=[feature_name, 'Launched Year', 'Company Name'])

    df_filtered['Launched Year'] = df_filtered['Launched Year'].astype(int)

    fig = px.violin(
        df_filtered,
        x='Company Name',
        y=feature_name,
        animation_frame='Launched Year',
        color='Company Name',
        box=True,
        points='all',
        hover_data=['Model Name'],
        color_discrete_map=company_colors
    )

    fig.update_layout(legend_title_text='')

    return json.loads(fig.to_json())

@app.get("/api/stacked_bar_price/{feature_name}")
def stacked_bar_price(feature_name: FeatureName):
    feature_name = FeatureName.map_to(feature_name)
    df_filtered = data.dropna(subset=['Company Name', 'Launched Year', feature_name])
    # Group by company and year, and calculate average price
    df_grouped = df_filtered.groupby(['Company Name', 'Launched Year'])[feature_name].mean().reset_index()

    # Prepare figure
    fig = go.Figure()

    # Create a bar for each year, stacked by company
    for i, year in enumerate(sorted(df_grouped['Launched Year'].unique())):
        year_data = df_grouped[df_grouped['Launched Year'] == year]
        fig.add_trace(go.Bar(
            x=year_data['Company Name'],
            y=year_data[feature_name],
            name=str(year),
            marker=dict(
                color=year_data['Company Name'].apply(lambda x: company_colors[x]),
                opacity=1 - (1 - i * 0.10)
            )
        ))

    fig.update_layout(
        barmode='stack',
        xaxis_title='Company Name',
        yaxis_title=f'Avg {FeatureName.small_name(feature_name)}',
        margin=dict(l=40, r=40, t=40, b=40),
        xaxis_tickangle=-45
    )

    return json.loads(fig.to_json())

# @app.get("/api/sunburst_price/{feature_name}")
# def sunburst_price(feature_name: FeatureName):
#     feature_name = FeatureName.map_to(feature_name)
#     df_filtered = data.dropna(subset=[
#         'Company Name', 'Model Name', feature_name
#     ])

#     fig = px.sunburst(
#         df_filtered,
#         path=['Company Name', 'Model Name'],
#         values=feature_name,
#         color=feature_name,
#         color_continuous_scale='Blues'
#     )

#     fig.update_layout(
#         margin=dict(l=40, r=40, t=40, b=40),
#         coloraxis_colorbar=dict(
#             title=FeatureName.small_name(feature_name)
#         )
#     )

#     return json.loads(fig.to_json())

@app.get("/api/pie_company_counts")
def pie_company_counts():
    df_filtered = data.dropna(subset=['Company Name', 'Model Name'])

    company_counts = df_filtered['Company Name'].value_counts().reset_index()
    company_counts.columns = ['Company Name', 'Count']

    fig = px.pie(
        company_counts,
        names='Company Name',
        values='Count',
        title='Distribution of Models by Company',
        color_discrete_sequence=px.colors.sequential.Oranges
    )

    fig.update_traces(textinfo='none', showlegend=True)

    fig.update_layout(
        margin=dict(l=40, r=40, t=40, b=40)
    )

    return json.loads(fig.to_json())