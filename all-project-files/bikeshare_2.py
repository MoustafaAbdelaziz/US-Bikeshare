import time
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_row', None)
# import numpy as np

CITY_DATA = {'chicago': 'chicago.csv',
             'new york': 'new_york_city.csv',
             'washington': 'washington.csv'}


def check_data_entry(prompt, valid_entries):
    """Asks user to type some input and verify if the entry typed is valid.

    Since we have 3 inputs to ask the user in get_filters(), it is easier to
    write a function.

    Args:
    ----
        (str) prompt - message to display to the user
        (list) valid_entries - list of string that should be accepted
    Returns:
    -------
        (str) user_input - the user's valid input
    """
    user_input = input(prompt).lower()
    while user_input not in valid_entries:
        print('Sorry... it seems like you\'re not typing a correct entry.')
        print('Let\'s try again!')
        user_input = input(prompt).lower()

    print('Great! the chosen entry is: {}\n'.format(user_input))
    return user_input


def get_filters():
    """Asks user to specify a city, month, and day to analyze.

    Args:
    ----
        this functoion takes no arguments
    Returns:
    -------
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
        day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

# =============================================================================
#     get user input for city (chicago, new york city, washington). HINT: Use a
#     while loop to handle invalid inputs
# =============================================================================
    valid_cities = CITY_DATA.keys()
    prompt_cities = """Please choose one of the 3 cities (chicago, new york
    city, washington): """
    city = check_data_entry(prompt_cities, valid_cities)
    # get user input for month (all, january, february, ... , june)
    valid_months = ['all', 'january', 'february', 'march', 'april', 'may',
                    'june']
    prompt_month = 'Please choose a month (all, january, february, ..., june):'
    month = check_data_entry(prompt_month, valid_months)

    # get user input for day of week (all, monday, tuesday, ... sunday)
    valid_days = ["all", "monday", "tuesday", "wednesday", "thursday",
                  "friday", 'saturday', 'sunday']
    prompt_day = 'Please choose a day (all, monday, tuesday, ... sunday): '
    day = check_data_entry(prompt_day, valid_days)

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """Load data for the specified city & filters by month & day if applicable.

    Args:
    ----
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no
        month filter
        (str) day - name of the day of week to filter by, or "all" to apply no
        day filter
    Returns:
    --------
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df["month"] = df["Start Time"].dt.month_name()
    df["day"] = df["Start Time"].dt.day_name()
    df["hour"] = df["Start Time"].dt.hour
    if month not in ["All", "all"]:
        df = df[df["month"] == month.title()]
    if day not in ["All", "all"]:
        df = df[df["day"] == day.title()]
    return df


def time_stats(df):
    """Display statistics on the most frequent times of travel."""
    start_time = time.time()

    # display the most common month
    print("What is the most common month:", df["month"].mode()[0], "\n")

    # display the most common day of week
    print("What is the most common day of week:", df["day"].mode()[0], "\n")

    # display the most common start hour
    print("What is the most common start hour:", df["hour"].mode()[0], "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Display statistics on the most popular stations and trip."""
    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("Most commonly used start station:", df["Start Station"].mode()[0],
          "\n")

    # display most commonly used end station
    print("most commonly used end station:", df["End Station"].mode()[0], "\n")

    # display most frequent combination of start station and end station trip
    print("most frequent combination of start station and end station trip:",
          df.groupby(
              ["Start Station", "End Station"]).size().nlargest(1), "\n")

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, month):
    """Display statistics on the total and average trip duration."""
    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time per month
    print("Total travel time per month:\n",
          df.groupby(["month"])["Trip Duration"].sum(), "\n")

    if month == "all":
        # display total travel time
        print("Total travel time:", df["Trip Duration"].sum(), "\n")

    # display mean travel time per month
    print("Total MEAN per month:\n",
          df.groupby(["month"])["Trip Duration"].mean(), "\n")

    if month == "all":
        # display total mean travel time
        print("Total travel MEAN:", df["Trip Duration"].mean(), "\n")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Display statistics on bikeshare users."""
    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print("Counts of user types:")
    print(df["User Type"].value_counts(), "\n")

    # Display earliest, most recent, and most common year of birth
    if city not in ["washington", "Washington"]:
        # Display counts of gender
        print("Counts of gender:\n", df["Gender"].value_counts(), "\n")

        # Display earliest year of birth.
        print("The earliest year of birth:", df["Birth Year"].min(), "\n")

        # Display most recent year of birth.
        print("The Most recent year of birth:", df["Birth Year"].max(), "\n")

        # Display common year of birth.
        print("Most common year of birth:", df["Birth Year"].mode()[0], "\n")
    else:
        print("There is no Gender, birth year column in Washington's Dataset!")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    """Print 5 rows of the data to the user."""
    view_data = input("""\nWould you like to view 5 rows of the data?
                      Enter yes or no\n""").lower()
    start = 0
    end = 5

    while view_data == "yes":
        print(df.iloc[start:end])
        start += 5
        end += 5
        view_data = input("""Do you like to see another 5 rows?:
                          Enter yes or no\n""").lower()
        if view_data != 'yes':
            break


def main():
    """Run the project."""
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df, month)
        user_stats(df, city)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
