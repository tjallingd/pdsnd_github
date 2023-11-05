import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington).
    list_of_cities = ['chicago', 'new york city', 'washington']

    while True:
        try:
            city = input('Type in the city where you want information from: Chicago, New York City or Washington: ').lower()
            if city in list_of_cities:
                print(city.capitalize())
                break
            else:
                print("That's not a valid choice, try again")
        except:
            print("That's not a valid choice, try again")

    # get user input for month (all, january, february, ... , june) or if all is typed, data for all months will be shown
    months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']

    while True:
        try:
            month = input("Type in the month where you want information from: january, february, march, april, may, june or type 'all' if want to see all months: ").lower()
            if month in months and month != 'all':
                print(month.capitalize())
                break
            elif month in months and month == 'all':
                print("That's great, you chose to see all months")
                break
            else:
                print("That's not a valid choice, try again")
        except:
            print("That's not a valid choice, try again")

    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']
 # get user input for day - or if all is typed, data for all days will be shown
    while True:
        try:
            day = input("Type in the day where you want information from: monday, tuesday, wednesday, thursday, friday, saturday, sunday or just type 'all' if want to see all days: ").lower()
            if day in days and day != 'all':
                print(day.capitalize())
                break
            elif day in days and day == 'all':
                print("No filter for the days of the week, so showing all days!")
                break
            else:
                print("That's not a valid choice, try again")
        except:
            print("That's not a valid choice, try again")

    print('-'*40)
    return city, month, day

def load_data(city, month, day):

    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetimeextract month and day of week to create new columns
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['Month'] = df['Start Time'].dt.month
    df['Day'] = df['Start Time'].dt.day_name()

 # filter by month and or day if applicable. After that update df accordingly.
    if month != 'all':
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        df = df[df['Month'] == month]

    if day != 'all':
        df = df[df['Day'] == day.title()]

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month + change numbers into actual words
    common_month = df['Month'].mode()[0]
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    common_month = months[common_month - 1]
    print("The most common month is: ", common_month.capitalize(), "(If you didn't choose 'All', then this should be your your choice of month)")

    # display the most common day of week
    common_day = df['Day'].mode()[0]
    print("\nThe most common day is: ", common_day, "(If you didn't choose 'All', then this should be your your choice of day)")

    # display the most common start hour, first use StartTime column to make Hour column. not needed for day and month as this is already done in 'load_data'
    df['Hour'] = df['Start Time'].dt.hour
    common_hour = df['Hour'].mode()[0]
    common_hour_end = common_hour + 1
    if common_hour < 10 and common_hour >= 6:
        print("\nThe most common hour is: ", common_hour, ":00h -", common_hour_end, ":00h, a bike is a good way to start the day!")
    else:
        print("\nThe most common hour is: ", common_hour, ":00h -", common_hour_end, ":00h")
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    common_start_station = df['Start Station'].mode()[0]
    print("Most people start their bike ride at: ", common_start_station)

    # display most commonly used end station
    common_end_station = df['End Station'].mode()[0]
    print("\nMost people end their bike ride at: ", common_end_station)

    # display most frequent combination of start station and end station trip.
    # Combine 'Start Station' and "End station' in new column 'Start End Station' and give '+' as separator
    df['Start End Station'] = df['Start Station'] + '+' + df['End Station']

   # most frequent combination
    start_end_station = df['Start End Station'].mode()[0]

    # split start and end station, so in print function you can name them separately
    start_end_station = start_end_station.split('+')
    start_station = start_end_station[0]
    end_station = start_end_station[1]

    print("\nThe most popular ride is from ", start_station, " to ", end_station)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time in seconds and minutes
    total_traveltime = df['Trip Duration'].sum()
    total_traveltime_hours = round((total_traveltime / 3600), 1)
    print("Total travel time of all users in the given time period is: ", total_traveltime, "seconds, which is equal to ", total_traveltime_hours, " hours.")

    # display mean travel time in seconds and minutes
    average_traveltime = df['Trip Duration'].mean()
    average_traveltime_minutes = round((average_traveltime / 60), 1)
    print("\nAverage travel time of all users in the given time period is: ", average_traveltime, "seconds, which is equal to ", average_traveltime_minutes, " minutes.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type']
    counter = {}

    for user in user_types:
        counter[user] = counter.get(user, 0) + 1

    print("Times the specific user type was filled in: ", counter)

    # Display counts of gender. Check if gender column does exist for the chosen selection. If not display different statement.
    if 'Gender' in df:
        genders = df['Gender']
        gendercounter = {}

    #Return value per key
        for gender in genders:
            gendercounter[gender] = gendercounter.get(gender, 0) + 1

        print("\nCheck out the count of a specific gender: ", gendercounter)
    else:
        print("\nWe would love to show you gender statistics, but unfortunately does this information not exist in this city")

    # Display earliest, most recent, and most common year of birth
    from datetime import date
    today = date.today()
    vandaag = int(today.strftime("%Y"))

    if 'Birth Year' in df:
        by_oldest = round(df['Birth Year'].min(),0)
        by_common = round(df['Birth Year'].mode()[0],0)
        age_oldest = round(by_oldest - vandaag, 0)
        print("\nThe oldest person renting a bike was born in: ", by_oldest, ",meaning that person is", -age_oldest, "years old!")
        print("\nThe birth year of most people renting a bike is: ", by_common)

    else:
        print("\nWe would love to show you birth year statistics, but unfortunately does this information not exist in this city")


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def display_data(df):
    view_data = input("\nNow you've seen all kinds of filtered data, would you like to view 5 rows of individual trip data? Enter yes or no:\n")
    start_loc = 0
    while view_data.lower() == 'yes':
        print(df.iloc[start_loc : start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue? ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
