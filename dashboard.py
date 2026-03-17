import streamlit as st
import pandas as pd
import psycopg2
import plotly.graph_objects as go
import plotly.express as px
import time
import folium
from streamlit_folium import st_folium

st.set_page_config(layout="wide")

# ---------- AUTO REFRESH ----------
if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = time.time()

if time.time() - st.session_state.last_refresh > 20:
    st.session_state.last_refresh = time.time()
    st.rerun()

# ---------- PREMIUM STYLE ----------
st.markdown("""
<style>

.stApp {
background-image: url("https://myradar.com/static/background-a089d87ba11e1a4c45a8efa960b86092.jpg");
background-size: cover;
background-attachment: fixed;
}

.main-card {
background: rgba(0,0,0,0.45);
padding:20px;
border-radius:15px;
backdrop-filter: blur(10px);
transition: transform 0.3s ease;
text-align:center;
}

.main-card:hover {
transform: scale(1.08);
}

.alert-box {
background: rgba(0,0,0,0.6);
padding:15px;
border-radius:10px;
text-align:center;
font-size:24px;
font-weight:600;
}

.title {
text-align:center;
font-size:40px;
font-weight:700;
color:white;
margin-bottom:10px;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<div class="title">🌦 Real-Time Weather Intelligence Dashboard</div>', unsafe_allow_html=True)

# ---------- DATABASE ----------
connection = psycopg2.connect(
    database="weather_pipeline_db",
    user="sreyavijay",
    host="localhost",
    port="5432"
)

df = pd.read_sql("SELECT * FROM weather_data ORDER BY recorded_at", connection)
connection.close()

df["recorded_at"] = pd.to_datetime(df["recorded_at"])
latest = df.iloc[-1]
df_latest = df.tail(20)

# ---------- WEATHER ALERT ----------
temp = latest["temperature"]
wind = latest["windspeed"]

if temp < 32 and wind < 20:
    status = "WEATHER CONDITION : NORMAL"
    color = "#00ffcc"

elif temp < 36 and wind < 35:
    status = "WEATHER CONDITION : MODERATE"
    color = "#ffb347"

else:
    status = "WEATHER CONDITION : EXTREME"
    color = "#ff2e63"

st.markdown(
    f'<div class="alert-box" style="border:2px solid {color}; color:{color};">{status}</div>',
    unsafe_allow_html=True
)

st.divider()

# ---------- GLASS KPI CARDS ----------
c1, c2, c3 = st.columns(3)

c1.markdown(f"""
<div class="main-card">
<h3>🌡 Temperature</h3>
<h1>{latest["temperature"]}</h1>
</div>
""", unsafe_allow_html=True)

c2.markdown(f"""
<div class="main-card">
<h3>💨 Wind Speed</h3>
<h1>{latest["windspeed"]}</h1>
</div>
""", unsafe_allow_html=True)

c3.markdown(f"""
<div class="main-card">
<h3>🧭 Direction</h3>
<h1>{latest["winddirection"]}</h1>
</div>
""", unsafe_allow_html=True)

st.divider()

# ---------- WIND ROSE ----------
st.subheader("🧭 Wind Rose Analysis")

df["dir_bin"] = (df["winddirection"] // 30) * 30
wind_rose = df.groupby("dir_bin")["windspeed"].mean().reset_index()

fig_rose = go.Figure()

fig_rose.add_trace(go.Barpolar(
    r=wind_rose["windspeed"],
    theta=wind_rose["dir_bin"],
    marker_color=wind_rose["windspeed"],
    marker_colorscale="Turbo",
    opacity=0.9
))

fig_rose.update_layout(
    template="plotly_dark",
    height=500
)

st.plotly_chart(fig_rose, use_container_width=True)

st.divider()

# ---------- TEMPERATURE GRAPH ----------
st.subheader("🌡 Temperature Trend")

fig_temp = px.line(
    df_latest,
    x="recorded_at",
    y="temperature",
    markers=True,
    color_discrete_sequence=["cyan"]
)

fig_temp.update_layout(template="plotly_dark")
st.plotly_chart(fig_temp, use_container_width=True)

st.divider()

# ---------- MAP ----------
st.subheader("📍 Monitoring Location")

m = folium.Map(
    location=[11.2588, 75.7804],
    zoom_start=7,
    tiles="CartoDB dark_matter"
)

folium.CircleMarker(
    [11.2588, 75.7804],
    radius=12,
    color="red",
    fill=True,
    fill_color="red",
    popup="Weather Station"
).add_to(m)

st_folium(m, use_container_width=True, height=450)
