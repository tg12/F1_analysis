import datetime
import os
import tempfile

import pandas as pd
from fastf1 import Cache, get_event_schedule, get_session
from tabulate import tabulate

data_options = {
    "laps": True,
    "telemetry": True,
    "weather": True,
    "messages": True,
    "livedata": None
}



def enable_caching():
    """Enables caching by creating a temporary directory for the cache."""
    tempdir = tempfile.gettempdir()
    cache_dir = os.path.join(tempdir, "fastf1_cache")
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    Cache.enable_cache(cache_dir)


def get_past_schedule(years_ago=3):
    """Returns the race schedule for the past `years_ago` seasons."""
    current_year = datetime.datetime.now().year
    schedule_lst = [
        get_event_schedule(year) for year in range(current_year - years_ago, current_year)
    ]
    schedule = pd.concat(schedule_lst)
    schedule = schedule[schedule["EventFormat"] == "conventional"]
    schedule = schedule[["RoundNumber", "Country", "Location", "EventDate", "EventName"]]
    schedule = schedule.sort_values(by=["EventName", "RoundNumber"]).set_index("RoundNumber")
    return schedule


def get_race_df(schedule):
    """Returns the race control messages for each event in the given schedule."""
    race_df_lst = []
    for _, row in schedule.iterrows():
        print("[+] Getting results for {} {} ({})".format(row["Country"], row["Location"], row["EventName"]))
        # create a temporary dataframe to store the event information, country, location, event name, and event date)
        event_df = pd.DataFrame({"Country": [row["Country"]], "Location": [row["Location"]], "EventName": [row["EventName"]], "EventDate": [row["EventDate"]]})
        print(event_df)
        year = row["EventDate"].year
        session = get_session(year, row["EventName"], "R")
        # use data_options to load the data
        session.load(**data_options)
        race_df = session.results
        # add country, location, eventname and event date to every row in race_df
        race_df = race_df.assign(Country=row["Country"], Location=row["Location"], EventName=row["EventName"], EventDate=row["EventDate"])
        race_df_lst.append(race_df)
        # using tabulate to print the results
        print(tabulate(race_df, headers="keys", tablefmt="psql"))

    return pd.concat(race_df_lst)



if __name__ == "__main__":
    enable_caching()
    print("[+] Cache enabled")

    schedule = get_past_schedule()
    print(tabulate(schedule, headers="keys", tablefmt="psql"))

    session_results = get_race_df(schedule)

    # sum of all the points for each driver, print using tabulate from high to low

    # print the datatype of the session_results

    print (session_results.dtypes)

    print (session_results.columns)

    # conver the points column to int so we can sum it and convert all the data in it to int in place

    session_results = session_results.astype({"Points": int})

    # write session_results to a csv file

    session_results.to_csv("session_results.csv")

    # read the csv file

    df = pd.read_csv("session_results.csv")

    # print the datatype of the session_results

    # print the columns of the DataFrame

    print (df.columns)

    # rcm_df = get_race_control_messages(schedule)
    # print(tabulate(rcm_df, headers="keys", tablefmt="psql"))
    # # print the columns of the DataFrame
    # print(rcm_df.columns)
    # # write the data to a CSV file
    # rcm_df.to_csv("rcm.csv")

    print("[+] Done")
