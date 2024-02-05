import numpy as np
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
import rms
from plotly.subplots import make_subplots


def plot_sales_customers(data, grpby):
    """"Plot sales and customer info as barplots in a neat grid.
    
    Keyword arguments:
    data -- the data frame to plot from, must have Sales, Customers and grpby as columns
    grpbyy -- the column(s?) to groupby
    """

    grouped = data.groupby(grpby, observed=False)

    plots = {"Count": grouped.Sales.count(),
             "Sales per Customer": grouped.Sales.sum() / grouped.Customers.sum(),
             "Sales (mean)": grouped.Sales.mean(),
             "Customers (mean)": grouped.Customers.mean(),
             "Sales (total)": grouped.Sales.sum(),
             "Customers (total)": grouped.Customers.sum(),
            }
    
    cols = 2
    rows = int(np.ceil(len(plots)/cols))

    fig = make_subplots(rows=rows, cols=cols, start_cell="top-left", subplot_titles=list(plots.keys()))

    suplot_iterator = [(i, j) for i in range(1, rows+1) for j in range(1, cols+1)]

    for p, (i, j) in zip(plots, suplot_iterator):
            fig.add_trace(go.Bar(x=plots[p].index, y=plots[p].values, name=p), row=i, col=j)
    
    fig.update_layout(width=1100, height=800, title_text=grpby, showlegend=False)
    fig.show()


def plot_sales_customers2(data, grpby):
    """"Plot sales and customer info as barplots in a neat grid.
    
    Keyword arguments:
    data -- the data frame to plot from, must have Sales and Customers as columns
    grpbyy -- the column(s?) to groupby
    """

    grouped = data.groupby(grpby, observed=False)

    plots = {"Count": grouped.Sales.count(),
             "Sales per Customer": grouped.Sales.sum() / grouped.Customers.sum(),
             "Sales (mean)": grouped.Sales.mean(),
             "Customers (mean)": grouped.Customers.mean(),
             "Sales (total)": grouped.Sales.sum(),
             "Customers (total)": grouped.Customers.sum(),
            }
    
    cols = 2
    rows = int(np.ceil(len(plots)/cols))

    fig = make_subplots(rows=rows, cols=cols, start_cell="top-left", subplot_titles=list(plots.keys()))

    suplot_iterator = [(i, j) for i in range(1, rows+1) for j in range(1, cols+1)]

    for p, (i, j) in zip(plots, suplot_iterator):
            fig.add_trace(go.Bar(x=plots[p].index, y=plots[p].values, name=p), row=i, col=j)
    
    # fig.update_layout(height=1200, width=1600, title_text=grpby, showlegend=False)
    fig.show()


def keep_rolling(data, col, windows_list):
    """Plot (time series) data as line graphs with rolling windows using plotly.

    Keyword arguments:
    data -- the data frame to plot from
    col -- the column(s?) from the data frame to plot
    windows_list -- the list of rolling window values to plot
    """

    fig = go.Figure()
    fig.add_traces(go.Scatter(x=data.index, y=data[col] , mode='lines', line={"dash": "dot"}, name = f"{col}", opacity=0.4))

    for window in windows_list:
        fig.add_traces(go.Scatter(x=data.index, y=data[col].rolling(window=window, center=True).mean() , mode='lines+markers', name = f"MA{window}", opacity=0.6))

    if ("CompetitionSince" in data.columns):
        competition_since = data.CompetitionSince.iloc[0]
        if (competition_since >= pd.to_datetime("2013")):
            competition_distance = data.CompetitionDistance.iloc[0]
            fig.add_vline(x=competition_since, line={"dash": "dash", "width": 1})
            fig.add_annotation(x=competition_since, y=1, yref="paper", text="competition opening ("+str(competition_distance)+"m)")

    if ("Promo2Since" in data.columns):
        promo2_since = data.Promo2Since.iloc[0]
        if (promo2_since >= pd.to_datetime("2013")):
            fig.add_vline(x=promo2_since, line={"dash": "dash", "width": 1})
            fig.add_annotation(x=promo2_since, y=1, yref="paper", yshift=-14, text="Promo2 starting")

    fig.update_layout(title=f"{col} over time", width=1100)

    fig.show()


def plotly_boxes(data, col):
    """Plot Sales and Customers data as boxplots by col using plotly.

    Keyword arguments:
    data -- the data frame to plot from
    col -- the column(s?) from the data frame to plot
    """
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.05)
    fig.add_trace(go.Box(x=data[col], y=data.Sales, boxmean=True, boxpoints='all', jitter=0.4, text=data.index.date, name="Sales (EUR)"), row=1, col=1)
    fig.add_trace(go.Box(x=data[col], y=data.Customers, boxmean=True, boxpoints='all', jitter=0.4, text=data.index.date, name="Customers"), row=2, col=1)
    fig.update_layout(height=800, width=1100, title_text=f"Sales, Customers by {col}", showlegend=False)
    fig.update_xaxes(tickmode = 'array', tickvals = [0, 1], ticktext = [f'No {col}', f'{col}'])
    fig.update_yaxes(title_text="Sales (EUR)", row=1, col=1)
    fig.update_yaxes(title_text="Customers", row=2, col=1)
    fig.show()


def print_store_info(store_id):
    """"Gather infos on a specific store an print them in a neat table."""
    if store_id > 1115:
        print(f"StoreID {store_id} out of range (1 - 1115)")
        return
        
    # gather data
    train = rms.get_train_df()
    data = rms.get_store_data_df(store_id)
    data_open = data.loc[data.Open==1]
    
    # top-lists
    top_total_sales = train.groupby("Store").Sales.sum().sort_values(ascending=False)
    top_total_customers = train.groupby("Store").Customers.sum().sort_values(ascending=False)    
    top_mean_sales = train.groupby("Store").Sales.mean().sort_values(ascending=False)
    top_mean_open_sales = train[train.Open==1].groupby("Store").Sales.mean().sort_values(ascending=False)
    top_mean_customers = train.groupby("Store").Customers.mean().sort_values(ascending=False)
    top_mean_open_customers = train[train.Open==1].groupby("Store").Customers.mean().sort_values(ascending=False)
    top_spc = (top_total_sales/top_total_customers).sort_values(ascending=False)

    # ranks
    sales_total_rank = top_total_sales.index.get_loc(store_id) + 1
    sales_mean_rank = top_mean_sales.index.get_loc(store_id) + 1
    sales_mean_open_rank = top_mean_open_sales.index.get_loc(store_id) + 1
    customers_total_rank = top_total_customers.index.get_loc(store_id) + 1
    customers_mean_rank = top_mean_customers.index.get_loc(store_id) + 1
    customers_mean_open_rank = top_mean_open_customers.index.get_loc(store_id) + 1
    spc_rank = top_spc.index.get_loc(store_id) + 1

    # some helper variables
    n_stores = len(train.groupby("Store"))
    n_days = len(data)    
    n_days_open = len(data_open)
    n_holidays = (data.StateHoliday != '0').sum()
    n_open_on_state_holidays = (data_open.StateHoliday != '0').sum()
    n_promodays = data.Promo.sum()
    n_school_holidays = (data.SchoolHoliday != 0).sum()
    is_promo2 = data.Promo2.iloc[0]==1
    
    # holidays
    oh_days = data_open.StateHoliday.value_counts()[1:].sum()
    h_days = data.StateHoliday.value_counts()[1:].sum()
    
    # store info
    sales_total = data.Sales.sum()
    sales_mean_per_open_day = data_open.Sales.mean()
    customers_total = data.Customers.sum()
    customers_mean_per_open_day = data_open.Customers.mean()
    sales_per_customer = sales_total / customers_total
    store_type = data.StoreType.iloc[0]
    assortment = data.Assortment.iloc[0]
    competition_distance = data.CompetitionDistance.iloc[0]
    competition_since = data.CompetitionSince.iloc[0]
    promo2_status = 'yes' if is_promo2 else 'no'
    renovation_status = 'yes' if n_days == 758 else 'no'
 
    # Create a dictionary to store formatted store-specific information
    store_info = {
        "Sales total": f"{sales_total:,.0f} EUR",
        "Sales total rank": f"#{sales_total_rank} / {n_stores} stores \n",
        "Sales per open day": f"{sales_mean_per_open_day:,.2f} EUR",
        "Sales per open day rank": f"#{sales_mean_open_rank} / {n_stores} stores \n",
        "Customers total": f"{customers_total:,.0f}",
        "Customers total rank": f"#{customers_total_rank} / {n_stores} stores \n",
        "Customers per open day": f"{customers_mean_per_open_day:,.0f}",
        "Customers per open day rank": f"#{customers_mean_open_rank} / {n_stores} stores \n",
        "Sales per Customer": f"{sales_per_customer:,.3f} EUR",
        "Sales per Customer rank": f"#{spc_rank} / {n_stores} stores \n",
        "Days open": f"{n_days_open} / {n_days} days",
        "Closed for renovation": f"{renovation_status}\n",
        "Promodays": f"{n_promodays} / {n_days} days \n",
        "Open on State Holidays": f"{n_open_on_state_holidays} / {n_holidays} days\n",
        "School Holidays": f"{n_school_holidays} \n",
        "Store Type": f"{store_type}",
        "Assortment": f"{assortment} \n",
        "Competition Distance": f"{competition_distance:,.0f}m",
        "Competition Since": f"{competition_since} \n",
        "Promo2": f"{promo2_status}"
    }
    
    if is_promo2:
        store_info["since"] = f"{data.Promo2Since.iloc[0]}"
        store_info["Intervall"] = f"{data.PromoInterval.iloc[0]}"
    
    print(f"***** General Information about Store {store_id} ***** \n")
    for k, v in store_info.items():
        print(f"{k:.<25}: {v}")

    return pd.DataFrame(store_info, index=[store_id])


def plot_impact(col, data_type, min_days=None):
    """"Plot impact of an event on a specific column.
    
        Keyword arguments:
        col -- the colum to plot
        data_type -- type of the event, default is "competition", "promo2" is the other valid option atm
        min_days -- only use stores that have at least min_days before and after the event"""
    data_open_df = rms.get_data_open_df()
    competition_impact_df = rms.get_impact_df(data_open_df, data_type=data_type)
    
    if min_days != None:
        competition_impact_df = competition_impact_df[(competition_impact_df.pre_days>=min_days) & (competition_impact_df.post_days>=min_days)]

    plot_me = competition_impact_df.sort_values(by=col, ascending=False).reset_index()
    mean_pos = (plot_me[col].mean() - plot_me[col]).abs().argsort()[0]

    if data_type == "competition":
        fig = px.bar(plot_me, x=plot_me.index, y=col, hover_data=["store"], color="competition_distance", width=1100, title=f"{data_type} impact on {col} by stores")
    else:
        fig = px.bar(plot_me, x=plot_me.index, y=col, hover_data=["store"], width=1100, title=f"{data_type} impact on daily_mean_sales by stores")

    fig.add_vline(x=competition_impact_df.shape[0]/2, annotation_text="median", annotation_position="bottom right", line={"dash": "dash", "width": 1})
    fig.add_vline(x=mean_pos, annotation_text="mean", line={"dash": "dash", "width": 1})
    fig.add_vline(x=plot_me.index[np.sign(plot_me[col]).diff().ne(0)][1] - 0.5, annotation_text="0", line={"dash": "dash", "width": 1})
    fig.show()


def plot_shared_x(col1, col2, freq="M"):
    """"Plot two columns on shared x axis."""
    data = rms.get_data_open_df()
    # data = rms.get_metrics(data)

    plot_me_col1 = data.resample(freq, level=1)[["Sales", "Customers"]].sum()
    plot_me_col1 = rms.get_metrics(plot_me_col1)
    plot_me_col1 = plot_me_col1[col1]

    plot_me_col2 = data.resample(freq, level=1)[["Sales", "Customers"]].sum()
    plot_me_col2 = rms.get_metrics(plot_me_col2)
    plot_me_col2 = plot_me_col2[col2]


    # plot_me_sales = data.resample(freq, level=1)[col1].sum()
    # plot_me_customers = data.resample(freq, level=1)[col2].sum()

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=plot_me_col1.index, y=plot_me_col1.values, name=col1), secondary_y=False)
    fig.add_trace(go.Scatter(x=plot_me_col2.index, y=plot_me_col2.values, name=col2), secondary_y=True)

    fig.update_layout(title_text=f"{col1} and {col2} (sum) by Date", width=1100)
    fig.update_xaxes(title_text="Date")
    fig.update_yaxes(title_text=f"{col1} (sum)", secondary_y=False)
    fig.update_yaxes(title_text=f"{col2} (sum)", secondary_y=True)

    fig.show()