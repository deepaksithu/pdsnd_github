import time
import pandas as pd
import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
cities = ['chicago', 'new york city', 'washington', 'all']
months = ['january', 'february', 'march', 'april', 'may', 'june', 'all']
days = ['monday', 'tuesday', 'wednesday', 'thursday',
        'friday', 'saturday', 'sunday', 'all']


def convert_time(t_sec):
    """
    converts seconds into hours, minutes, and seconds

    Args:
        (int) t_sec - the total number of seconds to be converted
    Returns:
        (int) hours - the total full hours converted from t_sec
        (int) minutes - the total full minutes converted from t_sec
        (int) seconds - the remaining seconds from t_sec
    """
    hours = int(t_sec / 3600)
    minutes = int((t_sec / 60) % 60)
    seconds = int(t_sec % 60)
    return hours, minutes, seconds


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - city to analyze
        (str) month - month to filter by, or "all" to apply no month filter
        (str) day - day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington).
    # HINT: Use a while loop to handle invalid inputs
    while True:
        city = input('Would you like to see data for Chicago, '
                     'New York City, Washington, '
                     'or \"all\" if you want to include all cities?\n').lower()
        if city in cities:
            break
        else:
            print('I didn\'t get that city, please try again.\n')
    # TO DO: get user input for month (all, january, february, ... , june)
    while True:
        month = input('Would you like to filter by month? '
                      'Type in the month name or \"all\" if you want '
                      'to include all months.\n').lower()
        if month in months:
            break
        else:
            print('I didn\'t get that month, please try again.\n')
    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        day = input('Would you like to filter by day of the week? '
                    'Type in the day or \"all\" if you want '
                    'to include all days.\n').lower()
        if day in days:
            break
        else:
            print('I didn\'t get that day, please try again.\n')
    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day.

    Args:
        (str) city - city to analyze
        (str) month - month to filter by, or "all" to apply no month filter
        (str) day - day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    if city == 'all':
        chicago = pd.read_csv(CITY_DATA['chicago'])
        n_y_c = pd.read_csv(CITY_DATA['new york city'])
        washington = pd.read_csv(CITY_DATA['washington'])
        frames = [chicago, n_y_c, washington]
        df = pd.concat(frames, sort=False)
    else:
        df = pd.read_csv(CITY_DATA[city])

    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    if month != 'all':
        month = months.index(month) + 1
        df = df[df['month'] == month]

    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    pop_month = months[df['month'].mode()[0] - 1]
    print('Most Popular Month: ', pop_month.title())

    # TO DO: display the most common day of week
    pop_day = df['day_of_week'].mode()[0]
    print('Most Popular Day: ', pop_day)

    # TO DO: display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    pop_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: {}:00'.format(pop_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    pop_start = df['Start Station'].mode()[0]
    print('Most Popular Starting Station: ', pop_start)

    # TO DO: display most commonly used end station
    pop_end = df['End Station'].mode()[0]
    print('Most Popular Ending Station: ', pop_end)

    # TO DO: display most frequent combo of start station and end station trip
    df['Start End'] = df['Start Station'] + " and " + df['End Station']
    pop_start_end = df['Start End'].mode()[0]
    print('Most Popular Combination Start and End: ', pop_start_end)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    hours, minutes, seconds = convert_time(total_time)
    print('Total Duration of all trips combined: {} hours, {} minutes, and '
          '{} seconds'.format(hours, minutes, seconds))

    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    hours, minutes, seconds = convert_time(mean_time)
    print('Mean Travel Time: {} hours, {} minutes, '
          'and {} seconds'.format(hours, minutes, seconds))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    subscriber = user_types.get('Subscriber')
    customer = user_types.get('Customer')
    dependent = user_types.get('Dependent')
    print('Subscribers: {} \nCustomers: {} \nDependents: '
          '{}'.format(subscriber, customer, dependent))

    # TO DO: Display counts of gender
    if 'Gender' in df.columns:
        print('')
        user_genders = df['Gender'].value_counts()
        male = user_genders.get('Male')
        female = user_genders.get('Female')
        print('Male: {} \nFemale: {}'.format(male, female))

    # TO DO: Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print('')
        earliest_year = int(df['Birth Year'].describe()['min'])
        latest_year = int(df['Birth Year'].describe()['max'])
        mode_year = int(df['Birth Year'].mode()[0])
        print('Earliest Birth Year: {} \nLatest Birth Year: {} \nMost Common '
              'Birth Year: {}'.format(earliest_year, latest_year, mode_year))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def raw_data(df):
    user_response = input('Would you like to see the raw data? '
                          'Enter yes or no.\n')
    count = 0
    while True:
        if user_response == 'yes':
            print(df.iloc[count:count + 5])
            count += 5
        elif user_response == 'no':
            break
        else:
            print('I didn\'t get that response, please try again.\n')
        user_response = input('Would you like to see more of the raw data? '
                              'Enter yes or no.\n')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
