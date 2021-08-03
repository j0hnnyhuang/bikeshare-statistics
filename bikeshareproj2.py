import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("Hello! Let's explore some US bikeshare data!")


    # Gets user input for city (chicago, new york, washington)
    print("\nWould you like to see data for Chicago, New York, or Washington?")
    city = ""
    cities = ['Chicago', 'New York', 'Washington']
    while city not in cities:
        city = input('Enter city: ').title()
        if city in cities:
            print("\nIt looks like you want to hear about {}. If this is not true, restart the program now!".format(city))
        else:
            print("Invalid city name. Please enter Chicago, New York, or Washington")


    # Gets user input for month, day, or both.
    print("\nWould you like to filter by month, day, or not at all? Type \"none\" for not at all.")
    time_filter = ""
    while time_filter not in ['month','day','none']:
        time_filter = input('Choice: ').lower()
        if time_filter in ['month','day','none']:
            print("\nWe will make sure to filter by {}!".format(time_filter))
        else:
            print("\nInvalid option. Please enter month, day, or none.")

    # Gets data for month, day, or both
    day = ""
    month = ""
    if time_filter == 'month':
        print("\nWhich month? January, February, March, April, May, or June?")
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        while month not in months:
            month = input('Month: ').title()
            if month in months:
                print("\nOne Moment Please... Loading data for {}.".format(month))
            else:
                print("\nInvalid option. Please enter full month name.")
    elif time_filter == 'day':
        print("\nWhich day of the week?")
        days = ['Monday','Tuesday','Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        while day not in days:
            day = input("Day: ").title()
            if day in days:
                print("\nOne Moment Please... Loading data for {}.".format(day))
            else:
                print("\nInvalid option. Please enter full day name.")
    else:
        print("unfiltered data")

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    # Loads and filters Data into dataframe
    df = pd.read_csv(CITY_DATA[city.lower()])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    df['Month'] = df['Start Time'].dt.month
    df['Month'] = df['End Time'].dt.month

    df['Day of Week'] = df['Start Time'].dt.weekday_name
    df['Day of Week'] = df['End Time'].dt.weekday_name

    if month != "":
        months  = ['January','February','March','April','May','June']
        month = months.index(month) + 1

        df = df[df['Month'] == month]

    if day != "":
        df = df[df['Day of Week'] == day.title()]
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Displays the most common month
    print("\nWhat is the most popular month of travel?")
    df['month'] = df['Start Time'].dt.month_name()
    popular_month = df['month'].mode()[0]
    print(popular_month)

    # Displays the most common day of week
    print("\nWhat is the most commonly travelled day?")
    df['day'] = df['Start Time'].dt.weekday_name
    popular_day = df['day'].mode()[0]
    print("Most Popular Day of Week: ", popular_day)

    # Displays the most common start hour
    print("\nWhat is the most popular hour of the day to start your travels?")
    df['hour'] = df['Start Time'].dt.hour
    popular_hour = df['hour'].mode()[0]
    print("Most popular hour: ", popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Displays most commonly used start station
    print("\nWhat is the most popular start station?")
    popular_start = df['Start Station'].value_counts().idxmax()
    print("Most Popular Start Station: ", popular_start)

    # Displays most commonly used end station
    print("\nWhat is the most popular end station?")
    popular_end = df['End Station'].value_counts().idxmax()
    print("Most Popular End Station: ", popular_end)

    # Displays most frequent combination of start station and end station trip
    print("\nWhat was the most popular trip from start station to end station?")
    popular_trip = df.groupby(['Start Station','End Station']).size().idxmax()
    print(popular_trip)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Displays total travel time
    print("\nWhat was the total traveling time during this time?")
    total_hours = (df['End Time'] - df['Start Time'])
    print(total_hours.sum())

    # Displays mean travel time
    print("\nWhat was the average trip duration?")
    diff_hours = (df['End Time'] - df['Start Time'])
    print(diff_hours.mean())

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Displays counts of user types
    print("\nWhat is the breakdown of users?")
    user_types = df['User Type'].value_counts()
    print(user_types)

    # Displays counts of gender
    print("\nWhat is the breakdown of gender?")
    if 'Gender' in df.columns:
        gender = df['Gender'].value_counts()
        print(gender)
    else:
        print("No Gender Data available for this city")

    # Displays earliest, most recent, and most common year of birth
    print("\nWhat is the earliest, most recent, and most common year of birth?")
    if 'Birth Year' in df.columns:
        earliest = df['Birth Year'].min()
        most_recent = df['Birth Year'].max()
        most_common = df['Birth Year'].mode()
        print("Earliest: ", earliest, "\nMost Recent: ", most_recent, "\nMost Common: ", most_common)
    else:
        print("No Birth Year data available for this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        print(city, month, day)
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
