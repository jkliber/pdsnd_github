import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'nyc': 'new_york_city.csv',
              'washington': 'washington.csv' }
    
def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data from Chicago, NYC or Washington!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    city = input("Would you like to see data for Chicago, NYC, or Washington?\n").lower()
    while city not in ["chicago", "nyc","washington"]:
        print("You did not type the correct name, please try again.")
        city = input("Would you like to see data for Chicago, NYC, or Washington?\n").lower()

    print("You selected: " + str.capitalize(city))
            
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input("Which month would you like to look at?  January, February, March, April, May, June  or All\n").lower()
    while month not in ["january", "february","march", "april", "may", "june", "all"]:
        print("You did not type the correct month, please try again.")
        month = input("Which month would you like to look at?  January, February, March, April, May, June  or All\n").lower()
    print("You selected: " + str.capitalize(month))
    
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("Which day of week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, All:\n").lower()
    while day not in ["monday", "tuesday", "wednesday", "thursday", "friday","saturday","sunday", "all"]:
        print("You did not type the correct name, please try it again:\n")
        day = input("Which day of week: Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, All:\n").lower()
    
    print("You selected: " + str.capitalize(day))
    print("\nThe following information is for\nCity: " + str.capitalize(city) + "\nMonth: " + str.capitalize(month) + "\nDay Of Week: " + str.capitalize(day))  
    
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
     
    df = pd.read_csv(CITY_DATA[city])
    
    df['start_time'] = pd.to_datetime(df['Start Time'])
    
    df['hour'] = pd.to_datetime(df['Start Time']).dt.hour
    
    df['month'] = df['start_time'].dt.month
    
    df['DOW'] = df['start_time'].dt.weekday_name

    if month != 'all':
        months = ["january", "february","march", "april", "may", "june"]
        month = months.index(month) + 1
        df = df[df['month'] == month]
    
    if day != 'all':
        df = df[df['DOW'] == day.title()]

  
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    common_month = df['month'].mode()
    print("The most common month: ")
    print(common_month)

    # TO DO: display the most common day of week
    common_dow = df['DOW'].mode()
    print("The most common day of week: ")
    print(common_dow)

    # TO DO: display the most common start hour
    common_hr = df['hour'].mode()[0] 
    print("The most common start hour: ")
    print(common_hr)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

    
def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()
    print("The most commonly used start station: ")
    print(start_station)
    
    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()
    print("The most commonly used end station: ")
    print(end_station)

    # TO DO: display most frequent combination of start station and end station trip
    start_end_stations = df.groupby(['Start Station', 'End Station']).size().sort_values(ascending=False).nlargest(5)
    print("The 5 most commonly used start and end stations: ")
    print(start_end_stations)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    
    # TO DO: display total travel time
    tot_travel_time = df['Trip Duration'].sum()
    hour = float(tot_travel_time) // 3600
    tot_travel_time %= 3600
    minutes = tot_travel_time // 60
    tot_travel_time %= 60
    seconds = tot_travel_time
    
    print("The total travel time:")
    print('Hours: ', hour)
    print('Minutes: ', minutes)
    print('Seconds: ', seconds)
    
    # TO DO: display mean travel time
    avg_travel_time = df['Trip Duration'].mean()
    print("The mean travel time: ")
    print(time.strftime("%H:%M:%S", time.gmtime(avg_travel_time)))
    
    # TO DO: display total travel time
    longest_duration = df['Trip Duration'].max()
    print("The longest travel time was : ")
    print(time.strftime("%H:%M:%S", time.gmtime(longest_duration)))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    if 'User Type' in df.columns:
        user_types = df['User Type'].value_counts()
        print("Count of User Types: ")
        print(user_types)

    # TO DO: Display counts of gender
    try:
        gender = df['Gender'].value_counts()
        print("Counts of Gender: ")
        print(gender)
    except:
        print("There is no gender information available for that city.")
    

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        youngest = min(df['Birth Year'])
        print("Earliest Year of Birth: ")
        print(youngest)
        recent_birth = max(df['Birth Year'])
        print("Most Recent Year of Birth: ")
        print(recent_birth)
        common_year_birth = df['Birth Year'].mode()
        print("Most common year of birth: ")
        print(common_year_birth)
    except:
        print("There is no birth year information available in this city")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)
    
    #Solicit and handle raw user input
    raw_data_input = input("Would you like to see some raw data?  Please enter 'Yes' or 'No'.\n").lower()
    while raw_data_input not in ["yes", "no"]:
        print("Invalid response, please try again.")
        raw_data_input = input("Would you like to see some raw data?  Please enter 'Yes' or 'No'.\n").lower()
    num = 0
    while raw_data_input == 'yes':
        try:
            num_input = int(input("How many rows?"))
        except ValueError:
            print("Please input an integer only.")
            continue
        print(df[num:num+num_input])
        num += num_input 
        raw_data_input = input("Would you like to see more raw data?  Please enter 'Yes' or 'No'.\n").lower()
        while raw_data_input not in ["yes", "no"]:
            print("Invalid response, please try again.")
            raw_data_input = input("Would you like to see some raw data?  Please enter 'Yes' or 'No'.\n").lower()


def main():
    while True:
        city, month, day = get_filters()
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
