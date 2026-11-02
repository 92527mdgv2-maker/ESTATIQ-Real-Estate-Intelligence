import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DATA = ROOT / 'data'
st.set_page_config(page_title='ESTATIQ | Real Estate Intelligence', page_icon='📈', layout='wide', initial_sidebar_state='collapsed')

st.markdown('''<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html,body,[class*="css"],.stApp {font-family:Inter, sans-serif;}
.stApp {background:#071525;color:#e8f1fc;}
[data-testid="stSidebar"] {background:#0b1d32;border-right:1px solid #203953;}
[data-testid="stHeader"] {background:rgba(7,21,37,.75);}
.block-container {padding-top:1.6rem;max-width:1500px;}
h1,h2,h3 {letter-spacing:-.035em;}
h1 {font-size:2.1rem!important;}
h3 {font-size:1.25rem!important;}
.brand {font-size:2rem;font-weight:800;letter-spacing:-.06em;color:#f1f7ff;margin-bottom:0;}
.brand span {color:#39a6ff;}
.tagline {color:#94b2d0;font-size:.83rem;margin-top:-.25rem;margin-bottom:1.5rem;}
.hero {border:1px solid #25425f;background:linear-gradient(115deg,#112d4b,#091b2f 70%);padding:25px 28px;border-radius:17px;margin-bottom:20px;}
.eyebrow {color:#55c8d6;letter-spacing:.15em;font-size:.72rem;font-weight:800;}
.hero-title {font-size:2rem;font-weight:800;letter-spacing:-.045em;margin:7px 0;}
.hero-sub {color:#a9c0d7;font-size:.94rem;}
.metric-card {background:#0d2239;border:1px solid #284665;border-radius:14px;padding:18px 19px;min-height:125px;}
.metric-label {color:#a7bed4;font-size:.8rem;font-weight:600;}
.metric-value {font-size:1.7rem;font-weight:800;color:#f5f9ff;margin-top:10px;letter-spacing:-.04em;}
.metric-note {color:#53c6b7;font-size:.75rem;margin-top:5px;}
[data-testid="stPlotlyChart"] {border:1px solid #264360;border-radius:15px;background:#0c2036;padding:10px;}
[data-testid="stDataFrame"] {border:1px solid #264360;border-radius:12px;}
.stButton button[kind="primary"] {background:#1686dd;border:0;}
hr {border-color:#25415e;}

/* Native Streamlit tabs: accessible, no radio dots; understated underline animation */
[data-testid="stTabs"] [data-baseweb="tab-list"] {gap:20px;overflow-x:auto;border-bottom:1px solid #28445e;scrollbar-width:thin;}
[data-testid="stTabs"] button[data-baseweb="tab"] {position:relative;white-space:nowrap;background:transparent!important;border:0!important;color:#94abc3!important;padding:12px 4px 16px!important;font-weight:600;transition:color .25s ease,transform .25s ease;}
[data-testid="stTabs"] button[data-baseweb="tab"]:hover {color:#f5faff!important;transform:translateY(-2px);}
[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"] {color:#f7fbff!important;}
[data-testid="stTabs"] button[data-baseweb="tab"]::after {content:"";position:absolute;left:0;right:0;bottom:2px;height:3px;border-radius:8px;background:#39a6ff;transform:scaleX(0);transition:transform .32s cubic-bezier(.22,.8,.2,1),box-shadow .3s ease;}
[data-testid="stTabs"] button[data-baseweb="tab"]:hover::after {transform:scaleX(.48);}
[data-testid="stTabs"] button[data-baseweb="tab"][aria-selected="true"]::after {transform:scaleX(1);box-shadow:0 0 13px #39a6ff77;}
[data-testid="stTabs"] [data-baseweb="tab-highlight"], [data-testid="stTabs"] [data-baseweb="tab-border"] {display:none;}
[data-testid="stTabs"] [data-baseweb="tab-panel"] {animation:enter .38s ease both;padding-top:12px;}
@keyframes enter {from{opacity:.45;transform:translateY(7px)}to{opacity:1;transform:translateY(0)}}
.top-brand {font-size:2rem;font-weight:800;letter-spacing:-.055em;color:#f1f7ff;padding:0 0 5px;}
.top-brand span {color:#39a6ff;}
.top-brand small {font-size:.72rem;letter-spacing:.15em;font-weight:650;color:#94b2d0;margin-left:20px;}
.filter-note {color:#90a9c3;font-size:.8rem;}
@media(prefers-reduced-motion:reduce){[data-testid="stTabs"] *{animation:none!important;transition:none!important;}}
</style>''', unsafe_allow_html=True)

@st.cache_data
def load_data():
    path = DATA / 'zillow_cleaned.csv'
    if not path.exists():
        st.error('Missing data/zillow_cleaned.csv. Keep the cleaned dataset in your data folder.')
        st.stop()
    return pd.read_csv(path, low_memory=False)

df = load_data()
dates = sorted([c for c in df.columns if len(str(c))==10 and str(c)[4]=='-' and str(c)[7]=='-' and str(c)[:4].isdigit()])
if not dates:
    st.error('No monthly date columns were found in the Zillow dataset.')
    st.stop()
latest = dates[-1]
previous = dates[-2] if len(dates)>1 else latest
prior_year = dates[-13] if len(dates)>=13 else dates[0]
for c in (latest, previous, prior_year):
    df[c] = pd.to_numeric(df[c], errors='coerce')

st.markdown('<div class="top-brand">◈ ESTAT<span>IQ</span><small>REAL ESTATE INTELLIGENCE</small></div>', unsafe_allow_html=True)
st.caption(f'ZILLOW ZHVI  /  {latest}  /  HISTORICAL MARKET RESEARCH')
states = sorted(df['State'].dropna().astype(str).unique().tolist())
with st.expander('⚙ Market filters  ·  Select a state and cities', expanded=True):
    state_col, city_col = st.columns([1, 3])
    with state_col:
        state = st.selectbox('State', states, index=states.index('TX') if 'TX' in states else 0)
    state_df = df[df['State'].astype(str) == state].copy()
    city_names = sorted(state_df['RegionName'].dropna().astype(str).unique().tolist())
    default = [x for x in ['Dallas','Houston','Austin','San Antonio','Fort Worth'] if x in city_names]
    with city_col:
        selected = st.multiselect('Compare cities', city_names, default=default or city_names[:3])
filtered = state_df[state_df['RegionName'].isin(selected)].copy()

st.markdown(f'''<div class="hero"><div class="eyebrow">MARKET INTELLIGENCE / {state}</div><div class="hero-title">Real Estate Market Analytics</div><div class="hero-sub">Explore historical home values, compare markets, and evaluate machine learning results. &nbsp;·&nbsp; Zillow ZHVI &nbsp;·&nbsp; {latest}</div></div>''', unsafe_allow_html=True)

tabs = st.tabs(['Overview','US Market Map','Market Trends','City Comparison','Market Rankings','Machine Learning','Data Quality','About'])

# Use unique region IDs rather than counting duplicate rows as cities.
city_count = df['RegionID'].nunique() if 'RegionID' in df else len(df)
mean_value = filtered[latest].mean() if not filtered.empty else float('nan')
previous_mean = filtered[previous].mean() if not filtered.empty else float('nan')
yoy_base = filtered[prior_year].mean() if not filtered.empty else float('nan')
month_change = (mean_value/previous_mean-1)*100 if pd.notna(previous_mean) and previous_mean!=0 else None
yoy_change = (mean_value/yoy_base-1)*100 if pd.notna(yoy_base) and yoy_base!=0 else None

def metric(label, value, note):
    st.markdown(f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>', unsafe_allow_html=True)

def style(fig, height=390):
    fig.update_layout(template='plotly_dark',paper_bgcolor='#0c2036',plot_bgcolor='#0c2036',font=dict(family='Inter, Arial',color='#c6d7e9'),height=height,margin=dict(l=20,r=20,t=55,b=35),legend_title_text='',hovermode='x unified')
    fig.update_xaxes(showgrid=True,gridcolor='#1b3651',zeroline=False)
    fig.update_yaxes(showgrid=True,gridcolor='#1b3651',zeroline=False,tickprefix='$',tickformat=',.0f')
    return fig

def long_data(frame):
    if frame.empty: return pd.DataFrame(columns=['RegionName','Date','HomeValue'])
    result=frame.melt(id_vars=['RegionName'],value_vars=dates,var_name='Date',value_name='HomeValue')
    result['Date']=pd.to_datetime(result['Date'])
    result['HomeValue']=pd.to_numeric(result['HomeValue'],errors='coerce')
    return result.dropna(subset=['HomeValue'])

with tabs[0]:
        cols=st.columns(4)
        with cols[0]: metric('CITIES IN DATASET',f'{city_count:,}','Unique Zillow region IDs')
        with cols[1]: metric('SELECTED STATE',state,'Current market filter')
        with cols[2]: metric('SELECTED CITIES',str(len(selected)),'Compare up to multiple markets')
        with cols[3]: metric('AVG. HOME VALUE',f'${mean_value:,.0f}' if pd.notna(mean_value) else 'N/A',f'Monthly change: {month_change:+.2f}%' if month_change is not None else 'No monthly comparison')
        st.write('')
        left,right=st.columns([1.45,1])
        with left:
            st.subheader('Housing value trends')
            if not filtered.empty:
                fig=px.line(long_data(filtered),x='Date',y='HomeValue',color='RegionName',color_discrete_sequence=['#36a3ff','#24c6b6','#ffbd59','#a68aff','#ff7285'])
                st.plotly_chart(style(fig),use_container_width=True)
            else: st.info('Choose one or more cities in Market filters.')
        with right:
            st.subheader('City value comparison')
            if not filtered.empty:
                comp=filtered.groupby('RegionName',as_index=False)[latest].mean().dropna().sort_values(latest,ascending=False)
                fig=px.bar(comp,x='RegionName',y=latest,color='RegionName',color_discrete_sequence=['#36a3ff','#24c6b6','#ffbd59','#a68aff','#ff7285'])
                fig.update_layout(showlegend=False)
                st.plotly_chart(style(fig),use_container_width=True)
            else: st.info('Choose one or more cities in Market filters.')
        left,right=st.columns([1.45,1])
        with left:
            st.subheader('Statewide value distribution')
            hist=state_df.dropna(subset=[latest])
            fig=px.histogram(hist,x=latest,nbins=45,color_discrete_sequence=['#36a3ff'])
            fig.update_yaxes(tickprefix='',title='Number of cities')
            st.plotly_chart(style(fig,350),use_container_width=True)
        with right:
            st.subheader('Market snapshot')
            if yoy_change is not None: st.metric('Year-over-year change, selected cities',f'{yoy_change:+.2f}%')
            if not filtered.empty:
                top=filtered.groupby('RegionName')[latest].mean().dropna().sort_values(ascending=False)
                if len(top): st.metric('Highest-value selected city',top.index[0],f'${top.iloc[0]:,.0f}')
            st.caption('ZHVI estimates typical home values; these are not individual sale prices. Averages are unweighted across selected city rows.')

with tabs[1]:
    st.subheader('U.S. Housing Market Map')
    st.caption('Interactive Zillow ZHVI map. State shading summarizes available city-level ZHVI estimates; it is not a state-level Zillow index. Locations are displayed only where verified coordinates are provided.')
    valid = df.copy()
    valid[latest] = pd.to_numeric(valid[latest], errors='coerce')
    valid[prior_year] = pd.to_numeric(valid[prior_year], errors='coerce')
    valid = valid.dropna(subset=[latest])
    valid['AnnualGrowth'] = (valid[latest] / valid[prior_year] - 1) * 100
    state_summary = valid.groupby('State', as_index=False).agg(AvgHomeValue=(latest,'mean'), MedianHomeValue=(latest,'median'), Cities=('RegionID','nunique'), AnnualGrowth=('AnnualGrowth','median'))
    metric_choice = st.segmented_control('Map coloring', ['Average home value', 'Median annual growth'], default='Average home value', key='map_metric')
    metric_col = 'AvgHomeValue' if metric_choice == 'Average home value' else 'AnnualGrowth'
    state_summary['Label'] = state_summary.apply(lambda r: f"{r['State']} | {int(r['Cities']):,} cities | Avg: ${r['AvgHomeValue']:,.0f} | Median YoY: {r['AnnualGrowth']:+.2f}%" if pd.notna(r['AnnualGrowth']) else f"{r['State']} | {int(r['Cities']):,} cities | Avg: ${r['AvgHomeValue']:,.0f}", axis=1)
    figmap = go.Figure(go.Choropleth(locations=state_summary['State'], z=state_summary[metric_col], locationmode='USA-states', colorscale='Blues' if metric_col=='AvgHomeValue' else 'RdYlGn', colorbar=dict(title='$' if metric_col=='AvgHomeValue' else '%',tickfont=dict(color='#c6d7e9')), customdata=state_summary[['Label']], hovertemplate='%{customdata[0]}<extra></extra>', marker_line_color='#18344d', marker_line_width=.7))
    figmap.update_geos(scope='usa', projection_type='albers usa', showlakes=False, showland=True, landcolor='#10243b', bgcolor='#0c2036')
    figmap.update_layout(height=520, paper_bgcolor='#0c2036', margin=dict(l=0,r=0,t=10,b=0),font=dict(color='#c6d7e9'))
    st.plotly_chart(figmap, use_container_width=True)
    st.caption('Each state color represents an unweighted aggregation of available city rows. Missing annual values are excluded from annual-growth calculations.')
    st.markdown('#### Explore city locations')
    st.caption('To avoid inaccurate map pins, upload an optional city coordinate file with columns RegionID, Latitude, Longitude. The file must contain verified coordinates for each Zillow RegionID.')
    coords_path = DATA / 'city_coordinates.csv'
    if coords_path.exists():
        coords = pd.read_csv(coords_path)
        needed={'RegionID','Latitude','Longitude'}
        if needed.issubset(coords.columns):
            coords=coords[['RegionID','Latitude','Longitude']].copy()
            coords['Latitude']=pd.to_numeric(coords['Latitude'],errors='coerce')
            coords['Longitude']=pd.to_numeric(coords['Longitude'],errors='coerce')
            coords=coords.dropna().drop_duplicates('RegionID')
            coords=coords[coords['Latitude'].between(18,72) & coords['Longitude'].between(-180,-65)]
            city_map=valid.merge(coords,on='RegionID',how='inner')
            city_map=city_map[city_map['State']==state]
            if not city_map.empty:
                figcities=px.scatter_geo(city_map,lat='Latitude',lon='Longitude',hover_name='RegionName',hover_data={'State':True,latest:':$,.0f','Latitude':False,'Longitude':False},size=latest,scope='usa',projection='albers usa',color=latest,color_continuous_scale='Blues',size_max=22)
                figcities.update_geos(showland=True,landcolor='#10243b',bgcolor='#0c2036',showlakes=False)
                figcities.update_layout(height=460,paper_bgcolor='#0c2036',margin=dict(l=0,r=0,t=10,b=0),font=dict(color='#c6d7e9'))
                st.plotly_chart(figcities,use_container_width=True)
                st.caption(f'{len(city_map):,} mapped cities in {state} with verified coordinates. Other cities are not shown.')
            else: st.info(f'No verified city coordinates found for {state}. The state map above is available for all states.')
        else: st.warning('city_coordinates.csv must contain RegionID, Latitude, and Longitude columns.')
    else:
        st.info('The state map is ready. To enable accurate individual city pins, add data/city_coordinates.csv with verified RegionID, Latitude, Longitude columns.')
    st.download_button('Download state market summary',state_summary.to_csv(index=False).encode('utf-8'),'estatiq_state_market_summary.csv','text/csv',key='download_state_map')

with tabs[2]:
        st.subheader('Historical housing market trends')
        years=sorted({int(c[:4]) for c in dates})
        start=st.slider('Start year',min_value=min(years),max_value=max(years),value=max(min(years),2018))
        long=long_data(filtered)
        long=long[long['Date'].dt.year>=start]
        if not long.empty:
            fig=px.line(long,x='Date',y='HomeValue',color='RegionName',color_discrete_sequence=px.colors.qualitative.Set2)
            st.plotly_chart(style(fig,540),use_container_width=True)
            st.download_button('Download selected historical data',long.to_csv(index=False),'estatiq_market_trends.csv','text/csv')
        else: st.info('Select cities with available historical data.')

with tabs[3]:
        st.subheader('City-by-city market comparison')
        if not filtered.empty:
            comp=filtered.groupby('RegionName',as_index=False)[[latest,prior_year]].mean().dropna(subset=[latest])
            comp['Annual change (%)']=(comp[latest]/comp[prior_year]-1)*100
            comp=comp.rename(columns={latest:'Latest home value ($)'})
            st.dataframe(comp,hide_index=True,use_container_width=True)
            fig=px.bar(comp.sort_values('Latest home value ($)',ascending=False),x='RegionName',y='Latest home value ($)',color='Latest home value ($)',color_continuous_scale=['#1a578c','#3ca8ff'])
            st.plotly_chart(style(fig,480),use_container_width=True)
            st.download_button('Download comparison',comp.to_csv(index=False),'estatiq_city_comparison.csv','text/csv')
        else: st.info('Select cities in Market filters.')

with tabs[5]:
        st.subheader('Predictive Intelligence Center')
        st.caption('Historical one-month-ahead backtesting · Models are evaluated on the most recent 12 months, not on future outcomes.')
        results_path = DATA / 'model_results.csv'
        predictions_path = DATA / 'model_predictions.csv'
        if not results_path.exists() or not predictions_path.exists():
            st.warning('Prediction files are missing. Run `python machine_learning_v2.py` from the project folder first.')
        else:
            @st.cache_data
            def load_ml_files(results_file, predictions_file, results_mtime, predictions_mtime):
                return pd.read_csv(results_file), pd.read_csv(predictions_file)
            results, predictions = load_ml_files(str(results_path), str(predictions_path), results_path.stat().st_mtime, predictions_path.stat().st_mtime)
            required = {'Model','MAE','RMSE','R2'}
            prediction_fields = {'RegionID','RegionName','State','Date','Actual','Predicted','Model'}
            if not required.issubset(results.columns) or not prediction_fields.issubset(predictions.columns):
                st.error('The prediction files have unexpected columns. Please rerun machine_learning_v2.py.')
            else:
                for col in ['MAE','RMSE','R2']:
                    results[col] = pd.to_numeric(results[col], errors='coerce')
                for col in ['Actual','Predicted']:
                    predictions[col] = pd.to_numeric(predictions[col], errors='coerce')
                predictions['Date'] = pd.to_datetime(predictions['Date'], errors='coerce')
                predictions = predictions.dropna(subset=['Date','Actual','Predicted'])
                valid = results.dropna(subset=['MAE'])
                best = valid.sort_values('MAE').iloc[0] if not valid.empty else None
                baseline = results[results['Model'].astype(str).str.contains('baseline',case=False,na=False)]
                base_mae = float(baseline.iloc[0]['MAE']) if not baseline.empty and pd.notna(baseline.iloc[0]['MAE']) else None
                c1,c2,c3,c4 = st.columns(4)
                with c1: st.metric('MODELS EVALUATED',str(results['Model'].nunique()))
                with c2: st.metric('BEST TEST MAE',f'${best["MAE"]:,.0f}' if best is not None else 'N/A')
                with c3: st.metric('BEST MODEL',str(best['Model']) if best is not None else 'N/A')
                with c4:
                    gain = (base_mae-float(best['MAE']))/base_mae*100 if best is not None and base_mae and base_mae>0 else None
                    st.metric('MAE VS. BASELINE',f'{gain:+.1f}%' if gain is not None else 'N/A',help='Positive means the best model has lower MAE than the previous-month baseline.')
                st.write('')
                st.markdown('#### Model performance comparison')
                metric_choice = st.selectbox('Evaluation metric', ['MAE','RMSE','R2'], key='ml_metric')
                left,right = st.columns([1.35,1])
                with left:
                    plot_results = results.dropna(subset=[metric_choice]).sort_values(metric_choice, ascending=metric_choice=='R2')
                    fig = px.bar(plot_results,x=metric_choice,y='Model',orientation='h',color='Model',color_discrete_sequence=['#36a3ff','#24c6b6','#a68aff'],text_auto='.3f' if metric_choice=='R2' else ',.0f')
                    fig.update_layout(showlegend=False,title=f'{metric_choice} by model')
                    fig = style(fig,380)
                    fig.update_yaxes(tickprefix='',tickformat=None)
                    fig.update_xaxes(tickprefix='$' if metric_choice!='R2' else '',tickformat=',.0f' if metric_choice!='R2' else '.5f')
                    st.plotly_chart(fig,use_container_width=True)
                with right:
                    st.dataframe(results,use_container_width=True,hide_index=True)
                    st.caption('MAE and RMSE are in U.S. dollars; lower is better. R² is unitless; higher is generally better. Metrics aggregate observations across cities and months.')
                    st.download_button('Download model metrics',results.to_csv(index=False).encode('utf-8'),'estatiq_model_metrics.csv','text/csv',key='ml_metrics_dl')
                st.markdown('#### City-level prediction explorer')
                available = predictions[predictions['State'].astype(str)==str(state)].copy()
                cities_available = sorted(available['RegionName'].dropna().astype(str).unique().tolist())
                if not cities_available:
                    st.info('No backtest predictions are available for the selected state.')
                else:
                    preferred = next((x for x in selected if x in cities_available),cities_available[0])
                    c1,c2 = st.columns([1,1])
                    with c1: ml_city = st.selectbox('City to analyze',cities_available,index=cities_available.index(preferred),key='ml_city')
                    with c2: ml_model = st.selectbox('Prediction model',results['Model'].dropna().astype(str).tolist(),key='ml_model')
                    city_rows = available[(available['RegionName'].astype(str)==ml_city)&(available['Model'].astype(str)==ml_model)].copy()
                    region_ids = city_rows['RegionID'].dropna().unique().tolist()
                    if len(region_ids)>1:
                        selected_region = st.selectbox('Zillow Region ID (duplicate city names)',region_ids,key='ml_region')
                        city_rows=city_rows[city_rows['RegionID']==selected_region]
                    city_rows=city_rows.sort_values('Date')
                    if city_rows.empty:
                        st.info('No predictions are available for this city and model.')
                    else:
                        city_mae = (city_rows['Actual']-city_rows['Predicted']).abs().mean()
                        city_rmse = ((city_rows['Actual']-city_rows['Predicted'])**2).mean()**0.5
                        city_pct = ((city_rows['Actual']-city_rows['Predicted']).abs()/city_rows['Actual'].replace(0,float('nan'))*100).mean()
                        m1,m2,m3=st.columns(3)
                        with m1: st.metric('CITY TEST MAE',f'${city_mae:,.0f}')
                        with m2: st.metric('CITY TEST RMSE',f'${city_rmse:,.0f}')
                        with m3: st.metric('MEAN ABSOLUTE % ERROR',f'{city_pct:.2f}%' if pd.notna(city_pct) else 'N/A')
                        series=city_rows.melt(id_vars=['Date'],value_vars=['Actual','Predicted'],var_name='Series',value_name='Home Value ($)')
                        fig=px.line(series,x='Date',y='Home Value ($)',color='Series',markers=True,color_discrete_map={'Actual':'#36a3ff','Predicted':'#24c6b6'},title=f'{ml_city}: actual vs. predicted ZHVI')
                        st.plotly_chart(style(fig,450),use_container_width=True)
                        city_rows['Error ($)']=city_rows['Predicted']-city_rows['Actual']
                        err=px.bar(city_rows,x='Date',y='Error ($)',color_discrete_sequence=['#ffbd59'],title='Prediction error by month (predicted − actual)')
                        st.plotly_chart(style(err,330),use_container_width=True)
                        detail=city_rows[['Date','Actual','Predicted','Error ($)']].copy()
                        detail['Date']=detail['Date'].dt.strftime('%Y-%m-%d')
                        st.dataframe(detail,hide_index=True,use_container_width=True)
                        st.download_button('Download this city’s predictions',detail.to_csv(index=False).encode('utf-8'),f'estatiq_{state}_{ml_city.replace(" ","_")}_predictions.csv','text/csv',key='ml_city_dl')
                st.info('**How to interpret:** These models use the previous three monthly ZHVI estimates to predict the next month. Test data are held out chronologically. Very high R² can occur because cities have widely different price levels and monthly changes are small; compare MAE against the naive baseline before claiming improvement. This is not a validated multi-month future forecast.')

with tabs[4]:
        st.subheader('Market rankings & momentum')
        st.caption('Rank cities within the selected state. Rankings require valid Zillow ZHVI estimates for both the latest month and the comparison month.')
        scope = st.radio('Market scope', ['All cities in selected state', 'Only selected cities'], horizontal=True)
        ranked = (state_df if scope.startswith('All') else filtered).copy()
        ranked[latest] = pd.to_numeric(ranked[latest], errors='coerce')
        ranked[prior_year] = pd.to_numeric(ranked[prior_year], errors='coerce')
        ranked[previous] = pd.to_numeric(ranked[previous], errors='coerce')
        ranked = ranked.dropna(subset=[latest, prior_year])
        ranked = ranked[(ranked[prior_year] > 0) & (ranked[latest] > 0)]
        ranked['YoY (%)'] = (ranked[latest] / ranked[prior_year] - 1) * 100
        ranked['MoM (%)'] = (ranked[latest] / ranked[previous] - 1) * 100
        ranked = ranked.rename(columns={'RegionName':'City',latest:'Home Value ($)'})
        if ranked.empty:
            st.info('No cities have sufficient data for this comparison. Try another state or selection.')
        else:
            metric_choice = st.selectbox('Rank by', ['YoY (%)', 'Home Value ($)', 'MoM (%)'])
            direction = st.radio('Sort', ['Highest first', 'Lowest first'], horizontal=True)
            limit = st.slider('Number of cities', 5, 30, 10)
            top = ranked.sort_values(metric_choice, ascending=direction=='Lowest first').head(limit)
            cols = st.columns(3)
            with cols[0]: st.metric('Cities with comparable data', f'{len(ranked):,}')
            with cols[1]: st.metric('Median annual change', f'{ranked["YoY (%)"].median():+.2f}%')
            with cols[2]: st.metric('Cities with annual growth', f'{(ranked["YoY (%)"]>0).sum():,}')
            fig = px.bar(top.sort_values(metric_choice), x=metric_choice, y='City', orientation='h', color=metric_choice, color_continuous_scale='Blues', title=f'{state}: {metric_choice}')
            fig.update_layout(showlegend=False, coloraxis_showscale=False)
            fig = style(fig, max(390, limit*30))
            fig.update_xaxes(tickprefix='$' if metric_choice=='Home Value ($)' else '', ticksuffix='%' if metric_choice!='Home Value ($)' else '')
            fig.update_yaxes(tickprefix='', tickformat=None)
            st.plotly_chart(fig, use_container_width=True)
            fields = [c for c in ['City','CountyName','Metro','Home Value ($)','YoY (%)','MoM (%)'] if c in ranked.columns]
            st.dataframe(top[fields], hide_index=True, use_container_width=True)
            st.download_button('Download ranked markets CSV', ranked[fields].to_csv(index=False), 'estatiq_market_rankings.csv', 'text/csv')
        st.caption('Year-over-year compares the latest month with the same month one year earlier. The figures are Zillow regional estimates, not realized investment returns.')

with tabs[6]:
        st.subheader('Data quality & methodology')
        st.write('Review data completeness before interpreting charts or model outputs.')
        numeric = df[dates].apply(pd.to_numeric, errors='coerce')
        count_nonmissing = numeric.notna().sum(axis=1)
        k1,k2,k3,k4=st.columns(4)
        with k1: st.metric('Region records', f'{len(df):,}')
        with k2: st.metric('Monthly periods', f'{len(dates):,}')
        with k3: st.metric('Latest-month coverage', f'{numeric[latest].notna().mean()*100:.1f}%')
        with k4: st.metric('Missing monthly values', f'{numeric.isna().sum().sum():,}')
        coverage = pd.DataFrame({'Month':pd.to_datetime(dates), 'Available cities':numeric.notna().sum(axis=0).values})
        fig=px.line(coverage,x='Month',y='Available cities',title='Historical coverage by month')
        fig=style(fig,420)
        fig.update_yaxes(tickprefix='',tickformat=',d')
        st.plotly_chart(fig,use_container_width=True)
        st.write(f'**Date coverage:** {dates[0]} through {latest}.')
        st.write(f'**Duplicate RegionIDs:** {int(df["RegionID"].duplicated().sum()) if "RegionID" in df else "Not available"}.')
        st.write(f'**Records with no monthly values:** {int((count_nonmissing==0).sum()):,}.')
        st.info('Zillow ZHVI measures typical home values, not actual sale transactions. Regional averages shown here are unweighted and should not be interpreted as a national home-price index.')
        st.download_button('Download monthly data coverage',coverage.to_csv(index=False),'estatiq_data_coverage.csv','text/csv')

with tabs[7]:
        st.subheader('About ESTATIQ')
        st.write('ESTATIQ is an educational real estate intelligence dashboard built with Python, Streamlit, Pandas, and Plotly.')
        st.write('Data source: Zillow Home Value Index (ZHVI). The index measures typical home values by region over time.')
        st.write('This application supports descriptive market analysis and comparison of trained regression models.')

st.divider()
st.caption('ESTATIQ • Real Estate Intelligence | Zillow ZHVI data | Built with Python, Streamlit & Plotly')
