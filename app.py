import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

st.set_page_config(page_title="Auto Data Visualization", layout="wide")
st.title("📊 Auto Data Visualization Platform")

uploaded_file = st.file_uploader("Upload CSV or Excel File", type=["csv", "xlsx"])

if uploaded_file:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(uploaded_file)
    else:
        df = pd.read_excel(uploaded_file)

    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    st.markdown("---")
    st.subheader("🎯 Select Column")

    selected_col = st.selectbox("Choose a column to visualize", df.columns)

    col_dtype = df[selected_col].dtype
    st.write(f"**Selected Column:** {selected_col}")
    st.write(f"**Data Type:** {col_dtype}")

    st.markdown("---")
    st.subheader("📈 All Possible Visualizations")

    # ---------------- NUMERIC COLUMN ----------------
    if np.issubdtype(col_dtype, np.number):

        # Histogram
        st.plotly_chart(
            px.histogram(df, x=selected_col, title=f"Histogram of {selected_col}"),
            use_container_width=True
        )

        # Box Plot
        st.plotly_chart(
            px.box(df, y=selected_col, title=f"Box Plot of {selected_col}"),
            use_container_width=True
        )

        # Line Chart
        st.plotly_chart(
            px.line(df, y=selected_col, title=f"Line Chart of {selected_col}"),
            use_container_width=True
        )

        # Violin Plot
        st.plotly_chart(
            px.violin(df, y=selected_col, box=True, points="all",
                      title=f"Violin Plot of {selected_col}"),
            use_container_width=True
        )

        # Scatter Plot (needs another numeric column)
        numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
        numeric_cols.remove(selected_col)

        if numeric_cols:
            st.subheader("🔀 Scatter Plot")
            second_col = st.selectbox(
                "Select another numeric column for Scatter Plot", numeric_cols
            )
            st.plotly_chart(
                px.scatter(df, x=selected_col, y=second_col,
                           title=f"Scatter Plot: {selected_col} vs {second_col}"),
                use_container_width=True
            )

        # Correlation Heatmap
        if len(df.select_dtypes(include=np.number).columns) > 1:
            st.subheader("🔥 Correlation Heatmap (All Numeric Columns)")
            corr = df.select_dtypes(include=np.number).corr()
            st.plotly_chart(
                px.imshow(corr, text_auto=True, title="Correlation Heatmap"),
                use_container_width=True
            )

    # ---------------- CATEGORICAL COLUMN ----------------
    elif df[selected_col].dtype == "object":

        counts = df[selected_col].value_counts().reset_index()
        counts.columns = [selected_col, "Count"]

        # Bar Chart
        st.plotly_chart(
            px.bar(counts, x=selected_col, y="Count",
                   title=f"Bar Chart of {selected_col}"),
            use_container_width=True
        )

        # Pie Chart
        st.plotly_chart(
            px.pie(counts, names=selected_col, values="Count",
                   title=f"Pie Chart of {selected_col}"),
            use_container_width=True
        )

        # Donut Chart
        st.plotly_chart(
            px.pie(counts, names=selected_col, values="Count", hole=0.4,
                   title=f"Donut Chart of {selected_col}"),
            use_container_width=True
        )

    # ---------------- DATETIME COLUMN ----------------
    else:
        try:
            df[selected_col] = pd.to_datetime(df[selected_col])
            st.info("Datetime column detected. Select a numeric column to create Time Series.")

            numeric_cols = df.select_dtypes(include=np.number).columns.tolist()
            num_col = st.selectbox("Select numeric column", numeric_cols)

            st.plotly_chart(
                px.line(df.sort_values(selected_col),
                        x=selected_col, y=num_col,
                        title=f"Time Series: {num_col} over {selected_col}"),
                use_container_width=True
            )
        except:
            st.warning("This column type is not supported.")

else:
    st.info("Please upload a dataset to start.")
