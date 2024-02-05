import numpy as np
import pandas as pd


def get_train_df():
    """Read train.csv with appropriate dtypes. Set Store and Date as Multiindex"""
    train_df = pd.read_csv("train.csv", 
                        parse_dates=["Date"],
                        index_col=[0, 2], 
                        dtype={"Store": "int16", "DayOfWeek": "int8", "Sales": "int32", 
                               "Customers": "int16", "Open": "int8", "Promo": "int8", 
                               "StateHoliday": "category", "SchoolHoliday": "int8"})
    
    train_df.loc[:, "isHoliday"] = train_df.StateHoliday!="0"

    # StateHoliday 1-hot encoden
    # train_df = pd.get_dummies(train_df, columns=["StateHoliday"], drop_first=True)

    train_df = train_df.sort_index()
    
    return train_df

def get_store_df():
    """"Read store.csv, do some date conversions and return the resulting df."""
    store = pd.read_csv("store.csv",
                        index_col=[0],    
                        dtype={"Store": "Int16", "StoreType": "category", "Assortment": "category", 
                               "CompetitionDistance": "Int32", "CompetitionOpenSinceMonth": "Int32", 
                               "CompetitionOpenSinceYear": "Int32", "Promo2": "Int8",
                               "Promo2SinceWeek": "Int32", "Promo2SinceYear": "Int32", "PromoInterval": "category"})
                        
    store["CompetitionSince"] = store.CompetitionOpenSinceMonth.astype("str")+"-"+store.CompetitionOpenSinceYear.astype("str")
    store["Promo2Since"] = store.Promo2SinceWeek.astype("str")+"-"+store.Promo2SinceYear.astype("str")
    
    store.CompetitionSince = pd.to_datetime(store.CompetitionSince, format="%m-%Y", errors="coerce")
    store.Promo2Since = pd.to_datetime(store.Promo2Since+"0", format="%W-%Y%w", errors="coerce")
    
    store = store.drop(["CompetitionOpenSinceMonth", "CompetitionOpenSinceYear", "Promo2SinceWeek", "Promo2SinceYear"], axis=1)

    store.loc[:, "Assortment"] = store.Assortment.replace({"a": "basic", "b": "extra", "c": "extended"})

    return store


def get_data_df():
    """ Get train.csv and store.csv and merge them on store...obviously."""
    train_df = get_train_df()
    store_df = get_store_df()
    
    data_df = pd.merge(train_df.reset_index(), store_df.reset_index(), on="Store")
    data_df = data_df.set_index(["Store", "Date"])

    # return get_metrics(data)
    return data_df


def get_data_open_df():
    """"Get merged data only for open days."""
    data_df = get_data_df()
    return data_df.loc[data_df.Open==1]


def get_store_data_df(id):
    """Get data for a specific store. """
    train_store = get_train_df().loc[id]
    train_store["Store"] = id

    store = get_store_df()
    
    data = pd.merge(train_store.reset_index(), store.reset_index(), on="Store")
    data = data.set_index("Date")

    return get_metrics(data)


def get_stores_data_df():
    """ Get train.csv and store.csv, merge them on Store and groupby Store.
     
    Returns the data aggregated by Store.  """
    train_df = get_train_df()
    store_df = get_store_df()
    
    stores_data_df = pd.merge(train_df.reset_index(), store_df.reset_index(), on="Store")

    stores_data_df = stores_data_df.groupby("Store").aggregate({
                                        # 'DayOfWeek': "sum",
                                        'Sales': "sum",
                                        'Customers': "sum",
                                        'Open': "sum",
                                        'Promo': "sum",
                                        # 'StateHoliday',
                                        'SchoolHoliday': "sum",
                                        # 'Store': "first",
                                        'StoreType': "first",
                                        'Assortment': "first",
                                        'CompetitionDistance': "first",
                                        'Promo2': "first",
                                        'PromoInterval': "first",
                                        'CompetitionSince': "first",
                                        'Promo2Since': "first",
                                    })
    
    stores_data_df.loc[:, "Renovation"] = (stores_data_df.Promo==286)
    # stores_data_df.drop("Promo", axis=1, inplace=True)

    stores_data_df.loc[:, "SalesPerCustomer"] = stores_data_df.Sales / stores_data_df.Customers
    stores_data_df.loc[:, "AvgSalesPerOpenDay"] = stores_data_df.Sales / stores_data_df.Open
    stores_data_df.loc[:, "AvgCustomersPerOpenDay"] = stores_data_df.Customers / stores_data_df.Open

    return stores_data_df


def get_weekly_data(id):
    """"Get weekly data for store id. Cut the edge weeks and renovations
    
        Keyword arguments:
        id -- store id to get data for
    """
    train_df = get_train_df()

    train_df = train_df.drop(["DayOfWeek", "StateHoliday"], axis=1)
    train_df = train_df.loc[id].resample("W").sum()
    
    # die erste und die letzte Woche sind unvollständig
    train_df = train_df.drop([train_df.index.min(), train_df.index.max()])

    # ggf. Renovierungswochen löschen (incl. Randwochen)
    if(train_df.loc["2014-07-13":"2014-12-28"].Open.sum()==0):
        train_df = train_df.drop(train_df.loc["2014-07-06":"2015-01-04"].index)

    # ggf. Competition und Promo2 Daten einfügen
    weekly_data = pd.merge(train_df, get_competition_and_promo2(id), left_index=True, right_index=True)

    return get_metrics(weekly_data)

def get_weekly_prediction_df(id):
    """"Get weekly data for store id. Cut the edge weeks and renovations
    
        Keyword arguments:
        id -- store id to get data for
    """
    train_df = get_train_df()
    train_df = pd.get_dummies(train_df, columns=["StateHoliday"], drop_first=True)

    train_df = train_df.drop(["DayOfWeek", "Customers"], axis=1)
    train_df = train_df.loc[id].resample("W").sum()
    
    # die erste und die letzte Woche sind unvollständig
    train_df = train_df.drop([train_df.index.min(), train_df.index.max()])

    # ggf. Renovierungswochen löschen (incl. Randwochen)
    if(train_df.loc["2014-07-13":"2014-12-28"].Open.sum()==0):
        train_df = train_df.drop(train_df.loc["2014-07-06":"2015-01-04"].index)

    # ggf. Competition und Promo2 Daten einfügen
    weekly_data = pd.merge(train_df, get_competition_and_promo2(id), left_index=True, right_index=True)

    return weekly_data


def get_metrics(df):
    """" Compute some business metrics.
    
        Currently: SalesPerCustomers, cummulativeSales, PercentageChangeSales, diffSales
        Keyword arguments:
        df -- the data frame to compute the metrics from
    """
    df["spc"] = df.Sales / df.Customers
    df["spc"] = df.spc.fillna(0)
    
    df["cum_sales"] = df.Sales.cumsum()
    df["pct_change_sales"] = df.Sales.pct_change()
    df["diff_sales"] = df.Sales.diff()

    df["cum_customers"] = df.Customers.cumsum()
    df["pct_change_customers"] = df.Customers.pct_change()
    df["diff_customers"] = df.Customers.diff()
    return df


def get_competition_and_promo2(id, df=None ):
    """"Gather competition and promo2 info if store id is affected by either.
    
        Keyword arguments:
        id -- the store id
        df -- the data to get the info from, 
              if no df is provided we take get_store_df() by default
    """
    ans = pd.DataFrame(index=pd.date_range("2013-1-1", "2015-7-31"))

    if df==None:
        df = get_store_df()

    aggregation_dict = {}

    # CompetitionSince und Promo2Since sind nur interessant, wenn sie im Beobachtungszeitraum liegen
    if not pd.isnull(df.loc[id].CompetitionSince):
        if df.loc[id].CompetitionSince>=pd.Timestamp("2013"):
            ans.loc[df.loc[id].CompetitionSince:, "Competition"] = 1
            ans.loc[:, "CompetitionSince"] = df.loc[id].CompetitionSince
            ans.loc[:, "CompetitionDistance"] = df.loc[id].CompetitionDistance
            aggregation_dict = {"Competition": "sum", "CompetitionSince": "first", "CompetitionDistance": "first"}

    if not pd.isnull(df.loc[id].Promo2Since):    
        if df.loc[id].Promo2Since>=pd.Timestamp("2013"):
            ans.loc[(df.loc[id].Promo2Since):, "Promo2"] = 1
            ans.loc[:, "Promo2Since"] = df.loc[id].Promo2Since
            ans.loc[:, "PromoInterval"] = df.loc[id].PromoInterval
            aggregation_dict["Promo2"] = "sum"
            aggregation_dict["Promo2Since"] = "first"
            aggregation_dict["PromoInterval"] = "first"

    if len(aggregation_dict) == 0:
        ans = ans.resample("W").sum()
    else:
        ans = ans.fillna(0)
        ans.resample("W").agg(aggregation_dict)
    return ans



def get_impact_df(df, data_type="competition"):
    """"Gather sales and customer info before and after some event.
    
        This is a generalization of the deprecated get_competition_impact.
        Keyword arguments:
        df -- the data frame to plot from
        data_type -- type of the event, default is "competition", "promo2" is the other valid option atm 
    """
    data_column = f"{data_type.capitalize()}Since"
    data_stores = df.loc[df[data_column] >= "2013"].index.unique(level="Store").to_list()
    
    """"Only competition has a distance."""
    if data_type=="competition":
        impact_df = pd.DataFrame(columns="store competition_since competition_distance pre_days post_days pre_sales post_sales pre_customers post_customers".split())
    else:
        impact_df = pd.DataFrame(columns=f"store {data_type}_since pre_days post_days pre_sales post_sales pre_customers post_customers".split())
    
    impact_df = impact_df.set_index("store")

    for store in data_stores:
        data_since = df.loc[store, data_column][0]
        my_dict = {f"{data_type}_since": data_since}

        if data_type=="competition":
            data_distance = df.loc[store, f"{data_type.capitalize()}Distance"][0]
            my_dict[f"{data_type}_distance"] = data_distance

        pre_data_df = df.loc[(store, slice(None, data_since)), :]
        post_data_df = df.loc[(store, slice(data_since, None)), :]

        my_dict["pre_days"] = pre_data_df.shape[0]
        my_dict["post_days"] = post_data_df.shape[0]

        my_dict["pre_sales"] = pre_data_df.Sales.sum()
        my_dict["post_sales"] = post_data_df.Sales.sum()

        my_dict["pre_customers"] = pre_data_df.Customers.sum()
        my_dict["post_customers"] = post_data_df.Customers.sum()

        impact_df.loc[store] = my_dict

    impact_df[f"pre_daily_mean_sales"] = impact_df["pre_sales"] / impact_df["pre_days"]
    impact_df[f"post_daily_mean_sales"] = impact_df["post_sales"] / impact_df["post_days"]
    impact_df[f"daily_mean_sales_diff"] = impact_df["post_daily_mean_sales"] - impact_df["pre_daily_mean_sales"]

    impact_df[f"pre_daily_mean_customers"] = impact_df["pre_customers"] / impact_df["pre_days"]
    impact_df[f"post_daily_mean_customers"] = impact_df["post_customers"] / impact_df["post_days"]
    impact_df[f"daily_mean_customers_diff"] = impact_df["post_daily_mean_customers"] - impact_df["pre_daily_mean_customers"]

    impact_df[f"pre_spc"] = impact_df["pre_sales"] / impact_df["pre_customers"]
    impact_df[f"post_spc"] = impact_df["post_sales"] / impact_df["post_customers"]
    impact_df[f"spc_diff"] = impact_df["post_spc"] -  impact_df["pre_spc"]

    return impact_df