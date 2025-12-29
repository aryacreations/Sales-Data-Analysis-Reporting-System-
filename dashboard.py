"""
Streamlit Dashboard for Sales Data Analysis
Interactive web interface for exploring sales data and insights
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from sales_analysis import SalesAnalyzer
from datetime import datetime
import sqlite3

# Page configuration
st.set_page_config(
    page_title="Sales Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main {
        padding: 0rem 1rem;
    }
    .stMetric {
        background-color: #f0f2f6;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .stMetric:hover {
        box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        transform: translateY(-2px);
        transition: all 0.3s ease;
    }
    h1 {
        color: #1f77b4;
        font-weight: 700;
    }
    h2 {
        color: #2c3e50;
        font-weight: 600;
        margin-top: 2rem;
    }
    h3 {
        color: #34495e;
        font-weight: 500;
    }
    .reportview-container .main .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'analyzer' not in st.session_state:
    st.session_state.analyzer = SalesAnalyzer()
    st.session_state.analyzer.load_data()

analyzer = st.session_state.analyzer

# Header
st.title("📊 Sales Data Analysis Dashboard")
st.markdown("### Real-time insights into your sales performance")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/sales-performance.png", width=80)
    st.title("Dashboard Controls")
    
    # Date range filter
    st.subheader("📅 Date Range")
    if analyzer.df is not None and len(analyzer.df) > 0:
        min_date = analyzer.df['sale_date'].min().date()
        max_date = analyzer.df['sale_date'].max().date()
        
        date_range = st.date_input(
            "Select date range",
            value=(min_date, max_date),
            min_value=min_date,
            max_value=max_date
        )
        
        # Filter data based on date range
        if len(date_range) == 2:
            mask = (analyzer.df['sale_date'].dt.date >= date_range[0]) & \
                   (analyzer.df['sale_date'].dt.date <= date_range[1])
            filtered_df = analyzer.df[mask].copy()
        else:
            filtered_df = analyzer.df.copy()
    else:
        filtered_df = analyzer.df.copy()
    
    # Product filter
    st.subheader("🏷️ Product Filter")
    if filtered_df is not None and len(filtered_df) > 0:
        all_products = sorted(filtered_df['product'].unique().tolist())
        selected_products = st.multiselect(
            "Select products",
            options=all_products,
            default=all_products
        )
        
        if selected_products:
            filtered_df = filtered_df[filtered_df['product'].isin(selected_products)]
    
    st.markdown("---")
    
    # Refresh button
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.session_state.analyzer = SalesAnalyzer()
        st.session_state.analyzer.load_data()
        st.rerun()
    
    st.markdown("---")
    st.markdown("### 📖 About")
    st.info(
        "This dashboard provides comprehensive sales analytics "
        "using SQL, Pandas, and NumPy for data processing."
    )

# Calculate metrics from filtered data
if filtered_df is not None and len(filtered_df) > 0:
    filtered_df['revenue'] = filtered_df['quantity'] * filtered_df['price']
    total_revenue = filtered_df['revenue'].sum()
    total_sales = len(filtered_df)
    total_items = filtered_df['quantity'].sum()
    avg_sale_value = filtered_df['revenue'].mean()
    
    # Key Metrics Row
    st.subheader("📈 Key Performance Indicators")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💰 Total Revenue",
            value=f"${total_revenue:,.2f}",
            delta=f"{total_sales} transactions"
        )
    
    with col2:
        st.metric(
            label="📦 Items Sold",
            value=f"{total_items:,}",
            delta=f"{filtered_df['product'].nunique()} products"
        )
    
    with col3:
        st.metric(
            label="💵 Avg Sale Value",
            value=f"${avg_sale_value:,.2f}",
            delta=f"±${filtered_df['revenue'].std():,.2f}"
        )
    
    with col4:
        st.metric(
            label="🎯 Max Sale",
            value=f"${filtered_df['revenue'].max():,.2f}",
            delta=f"Min: ${filtered_df['revenue'].min():,.2f}"
        )
    
    st.markdown("---")
    
    # Two column layout for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Monthly Revenue Trend
        st.subheader("📅 Monthly Revenue Trend")
        filtered_df['year_month'] = filtered_df['sale_date'].dt.to_period('M').astype(str)
        monthly_data = filtered_df.groupby('year_month').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'id': 'count'
        }).reset_index()
        monthly_data.columns = ['Month', 'Revenue', 'Quantity', 'Transactions']
        
        fig_monthly = go.Figure()
        fig_monthly.add_trace(go.Scatter(
            x=monthly_data['Month'],
            y=monthly_data['Revenue'],
            mode='lines+markers',
            name='Revenue',
            line=dict(color='#1f77b4', width=3),
            marker=dict(size=8),
            fill='tozeroy',
            fillcolor='rgba(31, 119, 180, 0.2)'
        ))
        
        avg_revenue = monthly_data['Revenue'].mean()
        fig_monthly.add_hline(
            y=avg_revenue,
            line_dash="dash",
            line_color="red",
            annotation_text=f"Avg: ${avg_revenue:,.0f}"
        )
        
        fig_monthly.update_layout(
            xaxis_title="Month",
            yaxis_title="Revenue ($)",
            hovermode='x unified',
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_monthly, use_container_width=True)
    
    with col2:
        # Top Products by Revenue
        st.subheader("🏆 Top 10 Products by Revenue")
        product_data = filtered_df.groupby('product').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'id': 'count'
        }).reset_index()
        product_data.columns = ['Product', 'Revenue', 'Quantity', 'Sales']
        product_data = product_data.sort_values('Revenue', ascending=False).head(10)
        
        fig_products = px.bar(
            product_data,
            x='Revenue',
            y='Product',
            orientation='h',
            color='Revenue',
            color_continuous_scale='Viridis',
            text='Revenue'
        )
        fig_products.update_traces(
            texttemplate='$%{text:,.0f}',
            textposition='outside'
        )
        fig_products.update_layout(
            xaxis_title="Revenue ($)",
            yaxis_title="",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_products, use_container_width=True)
    
    # Second row of charts
    col3, col4 = st.columns(2)
    
    with col3:
        # Sales Distribution
        st.subheader("📊 Sales Value Distribution")
        fig_dist = go.Figure()
        fig_dist.add_trace(go.Histogram(
            x=filtered_df['revenue'],
            nbinsx=50,
            name='Sales Distribution',
            marker_color='#ff7f0e',
            opacity=0.7
        ))
        fig_dist.add_vline(
            x=avg_sale_value,
            line_dash="dash",
            line_color="green",
            annotation_text=f"Mean: ${avg_sale_value:.2f}"
        )
        fig_dist.add_vline(
            x=filtered_df['revenue'].median(),
            line_dash="dash",
            line_color="blue",
            annotation_text=f"Median: ${filtered_df['revenue'].median():.2f}"
        )
        fig_dist.update_layout(
            xaxis_title="Sale Value ($)",
            yaxis_title="Frequency",
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_dist, use_container_width=True)
    
    with col4:
        # Quantity vs Revenue Scatter
        st.subheader("📈 Quantity vs Revenue Analysis")
        product_scatter = filtered_df.groupby('product').agg({
            'revenue': 'sum',
            'quantity': 'sum',
            'id': 'count'
        }).reset_index()
        product_scatter.columns = ['Product', 'Revenue', 'Quantity', 'Sales']
        
        fig_scatter = px.scatter(
            product_scatter,
            x='Quantity',
            y='Revenue',
            size='Sales',
            color='Revenue',
            hover_data=['Product'],
            color_continuous_scale='Plasma',
            size_max=30
        )
        fig_scatter.update_layout(
            xaxis_title="Total Quantity Sold",
            yaxis_title="Total Revenue ($)",
            height=400
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    st.markdown("---")
    
    # Detailed Data Tables
    st.subheader("📋 Detailed Analytics")
    
    tab1, tab2, tab3 = st.tabs(["📊 Product Performance", "📅 Monthly Breakdown", "🔍 Raw Data"])
    
    with tab1:
        st.markdown("#### Product Performance Metrics")
        product_metrics = filtered_df.groupby('product').agg({
            'revenue': ['sum', 'mean'],
            'quantity': 'sum',
            'price': 'mean',
            'id': 'count'
        }).round(2)
        product_metrics.columns = ['Total Revenue', 'Avg Revenue/Sale', 'Total Qty', 'Avg Price', 'Num Sales']
        product_metrics = product_metrics.sort_values('Total Revenue', ascending=False)
        product_metrics['Total Revenue'] = product_metrics['Total Revenue'].apply(lambda x: f"${x:,.2f}")
        product_metrics['Avg Revenue/Sale'] = product_metrics['Avg Revenue/Sale'].apply(lambda x: f"${x:,.2f}")
        product_metrics['Avg Price'] = product_metrics['Avg Price'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(product_metrics, use_container_width=True)
    
    with tab2:
        st.markdown("#### Monthly Sales Breakdown")
        monthly_metrics = filtered_df.groupby('year_month').agg({
            'revenue': ['sum', 'mean'],
            'quantity': 'sum',
            'id': 'count'
        }).round(2)
        monthly_metrics.columns = ['Total Revenue', 'Avg Sale Value', 'Total Quantity', 'Num Transactions']
        monthly_metrics['Total Revenue'] = monthly_metrics['Total Revenue'].apply(lambda x: f"${x:,.2f}")
        monthly_metrics['Avg Sale Value'] = monthly_metrics['Avg Sale Value'].apply(lambda x: f"${x:,.2f}")
        st.dataframe(monthly_metrics, use_container_width=True)
    
    with tab3:
        st.markdown("#### Raw Sales Data")
        display_df = filtered_df[['sale_date', 'product', 'quantity', 'price', 'revenue']].copy()
        display_df['sale_date'] = display_df['sale_date'].dt.date
        display_df['price'] = display_df['price'].apply(lambda x: f"${x:.2f}")
        display_df['revenue'] = display_df['revenue'].apply(lambda x: f"${x:.2f}")
        display_df = display_df.sort_values('sale_date', ascending=False)
        st.dataframe(display_df, use_container_width=True, height=400)
    
    # Download section
    st.markdown("---")
    st.subheader("💾 Export Data")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Filtered Data (CSV)",
            data=csv,
            file_name=f"sales_data_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col2:
        product_csv = product_metrics.to_csv()
        st.download_button(
            label="📥 Download Product Report (CSV)",
            data=product_csv,
            file_name=f"product_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )
    
    with col3:
        monthly_csv = monthly_metrics.to_csv()
        st.download_button(
            label="📥 Download Monthly Report (CSV)",
            data=monthly_csv,
            file_name=f"monthly_report_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            use_container_width=True
        )

else:
    st.error("⚠️ No data available. Please run `python init_database.py` to initialize the database.")
    st.info("💡 After initializing the database, refresh this page.")

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #7f8c8d; padding: 20px;'>
        <p>📊 Sales Data Analysis Dashboard | Built with Streamlit, Pandas & NumPy</p>
        <p>Last updated: {}</p>
    </div>
    """.format(datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
    unsafe_allow_html=True
)
