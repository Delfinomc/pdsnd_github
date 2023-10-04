import time
import pandas as pd
import numpy as np
pd.set_option('display.max_columns', None)
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
MONTHS=["all", "january", "february", "march", "may", "june", "july", "august", "september", "october", "november", "december"]
DAYS=["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city=input("write me a city name, either chicago, new york city, washington: ").lower()
    cities=CITY_DATA.keys()
    while city not in cities:
        city=input("invalid input: write me a city name, either chicago, new york city, washington: ").lower()

    # get user input for month (all, january, february, ... , june)

    month=input("give me any month in a year from january to june or type in \"all\" ").lower()
    while month not in MONTHS:
        month=input("invalid input:give me any month in a year from january to june or type in \"all\" ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)

    day=input("give me any day in a week from monday to sunday or type in \"all\" ").lower()
    while day not in DAYS:
        day=input("invalid input:give me any day in a week from monday to sunday or type in \"all\" ").lower()

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

    df=pd.read_csv(CITY_DATA[city])
    # convert the Start Time column to datetime
    df['Start Time'] =pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
  #  df['day_of_week'] = df['Start Time'].dt.day_of_week
    df['day_of_week'] = df['Start Time'].dt.strftime('%A')


    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        month = MONTHS.index(month.lower())


        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    if df.columns.isin(['Birth Year']).any():
        df['Birth Year'] = df['Birth Year'].astype('Int64')
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    df['hour'] = df['Start Time'].dt.hour


    # display the most common month
    common_month_num = df['month'].mode()[0]
    common_month_str = MONTHS[common_month_num].title()
    print(f"the most common month is {common_month_str}")

    # display the most common day of week
    common_day_of_week=df['day_of_week'].mode()[0]
    print(f"the most common day of week is {common_day_of_week}")

    # display the most common start hour
    common_start_hour= df['hour'].mode()[0]
    print(f"the most common start hour is {common_start_hour}")

    print("\nThis took %s seconds." % (time.time() - start_time))
    # The code above gives the same result as the code below:
    # print("\nThis took {} seconds.".format(time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station= df['Start Station'].mode()[0]
    print(f"the most commonly used start station is {common_start_station}")

    # display most commonly used end station
    common_end_station= df['End Station'].mode()[0]
    print(f"the most commonly used end station is {common_end_station}")

    # display most frequent combination of start station and end station trip
    frequent_trip=(df['Start Station'] + ' - ' + df['End Station']).mode()[0]
    print(f"the most frequent trip between start and end station is {frequent_trip}")



    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = round(df['Trip Duration'].sum()/60/60,2)
    print(f"the total travel time is {total_travel_time} hours")

    # display mean travel time
    mean_travel_time = round(df['Trip Duration'].mean()/60,2)
    print(f"the mean of travel time is {mean_travel_time} minutes")




    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_type_counts=df['User Type'].value_counts()
    print(f"the counts of user types is {user_type_counts}")

    # Display counts of gender
    if df.columns.isin(['Gender']).any():
        gender_counts=df['Gender'].value_counts()
        print(f"the counts of gender is {gender_counts}")

    # Display earliest, most recent, and most common year of birth
    if df.columns.isin(['Birth Year']).any():
        earliest_year = df['Birth Year'].min()
        most_recent_year = df['Birth Year'].max()
        most_common_year = df['Birth Year'].mode()[0]
        print("Earliest Year of Birth:", earliest_year)
        print("Most Recent Year of Birth:", most_recent_year)
        print("Most Common Year of Birth:", most_common_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def print_rows(df):
    """Prints rows as requested by the user."""
    rowc=0
    answer=input("do you want to print the first five rows of raw data?").lower()
    while (answer== "yes" and rowc<df.shape[0]):
        print(df[rowc:rowc+5])
        rowc=rowc+5
        if rowc<df.shape[0]:
            answer=input("do you want to print the next five rows of raw data?").lower()




def main():
    while True:
        city, month, day = get_filters()
        # city="chicago"
        # month="february"
        # day="sunday"
        df = load_data(city, month, day)

        while df.shape[0]==0:
            print("There is no data matching the filters, let's try again")
            city, month, day = get_filters()
            df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # df=df[0:7]
        print_rows(df)


        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
