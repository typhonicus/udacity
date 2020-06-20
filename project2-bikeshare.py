# -*- coding: utf-8 -*-
"""
Created on Sun Apr 15 15:59:44 2018

@author: Typhonicus
"""
# The following lines import packages to help do more complex operations more easily.
import time
import pandas as pd
import numpy as np

#The Following dictionary is used to help choose the correct csv, based on user input.
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    '''So for this function, I was thinking about making a dictionary or a list of 
       prompts that I could use to nest the while-loops into a for loop to make this function 
       more compact, but I kinda ran out of time. Just know that that was my intent.'''
    
    #*************************** City Choice ****************************
    #The following assignments are a prompts the user will see.    
    choice_prompt = "You chose: "
    no_prompt = ".\nAre you sure? Type 'n' to choose again or enter any other value to continue. "
    city_prompt = "\nChoose a CITY: Enter Chicago, New York City, or Washington: "
    city_answer = "" #initializes the city_answer variable
    error_message = "Not a valid input...\n" 
    while True: #Used to reset city choice or break to the city loop.
        while True: #Used to choose the name of the city which will be used to open relevant csv.
            city = input(city_prompt).lower().strip() #takes in the user's input and forces it to be lower.
            if city not in CITY_DATA.keys(): #checks to see if user input matches a CITY_DATA key.
                print(error_message) #prints an error message.
                continue #Resets the loop
            else:
                break #Breaks out of the loop if user input matches a CITY_DATA key.
        city_answer = input(choice_prompt + city.title() + no_prompt) #Requests user input to verify their choice.
        if city_answer.lower().strip() == 'n': #Checks to see if the user chose 'n' relative to the no_prompt.
            continue #resets the loop to the beginning, asking the user for a city.
        else: #if the user enters in any other value...
            break #...break from the city loop.
    #********************************************************************   
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~ Month Choice ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #The following assignments are a prompts the user will see. 
    months = ['january', 'february', 'march', 'april', 'may', 'june']
    month_prompt = "\nChoose a MONTH between January and June to filter results by. "
    month_prompt += "\nEnter 'all' if you don't want to filter by month: "         
    month_answer = "" #initializes the month_answer variable
    while True: #Used to reset month choice or break to the month loop.
        while True: #Used to attempt to get month choice until valid input is given.    
            month = input(month_prompt).lower().strip() #assigns the month to the users input.
            if month not in months and month != 'all': #an if block designed to ensure input is valid.
                print(error_message) #prints an error message if input is invalid.
                continue #locks the user in the while loop in invalid input is given.
            else:
                break #breaks out of the loop if valid input is given
        month_answer = input(choice_prompt + month.title() + no_prompt) #Asks the user to verify input.
        if month_answer.lower().strip() == 'n': #if the user enters 'n' the user is allowed to choose another month.
            continue # resets the choice loop if 'n' is chosen.
        else:
            break #rest
    #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #//////////////////////////// Day Choice ////////////////////////////
    week_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    day_prompt = "\nEnter in a DAY of the week. " 
    day_prompt += "\nEnter 'all' if you don't want to filter by day: "
    day_answer = "" #initializes the day_answer variable
    while True: #Used to reset day choice or break to the day loop.
        while True: #Used to attempt to get day choice until valid input is given.    
            day = input(day_prompt).lower().strip() #assigns the day to the users input.
            if day not in week_days and day != 'all': #an if block designed to ensure input is valid.
                print(error_message) #prints an error message if input is invalid.
                continue #locks the user in the while loop in invalid input is given.
            else:
                break #breaks out of the loop if valid input is given
        day_answer = input(choice_prompt + day.title() + no_prompt) #Asks the user to verify input.
        if day_answer.lower().strip() == 'n': #if the user enters 'n' the user is allowed to choose another day.
            continue #resets the choice loop if 'n' is chosen.
        else:
            break #proceed if the user enters anything other than 'n'
    #////////////////////////////////////////////////////////////////////
    
    print('-----'*8)
    print('-----'*8)     
    return city, month, day #returns the user's choice of city, month, and day


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
    filename = CITY_DATA[city] #The filename is equivalent to the it's value in the CITY_DATA dictionary.
    df = pd.read_csv(filename) #uses pandas to read in csv files relative to chosen city.
    
       # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month], weekday, and from Start Time to create new columns
    df['Month'] = df['Start Time'].dt.month #creates a new column called Month
    df['Day of Week'] = df['Start Time'].dt.weekday_name #creates a new column called Day of Week
    df['Start Hour'] = df['Start Time'].dt.hour #creates a new column called Start Hour
    
    # filters by month if applicable
    if month != 'all': #runs if the user didn't choose 'all' for month.
        # The following lines use the index of the months list to get a corresponding int value
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1
        # Filters df by month to create the new dataframe
        df = df[df['Month'] == month]

    # filters by day of week if applicable
    if day != 'all': #runs only if the user didn't choose 'all' for day
        # Filters df by weekday to create the new dataframe
        df = df[df['Day of Week'] == day.title()]
        
    return df #returns df.


def time_stats(df, month, day):
    """Displays statistics on the most frequent times of travel.
    
    Args:
        (pd.df) df - dataframe in usage
        (int) month - the numeral month 
        (str) day - name of the day of week if filtered or 'all'
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time() #starts a timer
    
    #The following dictionary is used to change the numeral month to its word equivalent.
    month_number_to_words = {1: 'January',
                             2: 'Ferbruary',
                             3: 'March',
                             4: 'April',
                             5: 'May',
                             6: 'June'}

    #The following dictionary is used to change the numeral hour to its word equivalent.
    hour_number_to_words = {0: '12 am', 1: '1 am', 2: '2 am', 3: '3 am',
                            4: '4 am', 5: '5 am', 6: '6 am', 7: '7 am',
                            8: '8 am', 9: '9 am', 10: '10 am', 11: '11 am',
                            12: '12 pm', 13: '1 pm', 14: '2 pm', 15: '3 pm', 
                            16: '4 pm', 17: '5 pm', 18: '6 pm', 19: '7 pm', 
                            20: '8 pm', 21: '9 pm', 22: '10 pm', 23: '11 pm'}

    # The following lines display the most common month. 
    if month == 'all': #If the user chose 'all' This block will be run.
        mode_month = df['Month'].mode()[0] #Assigns the mode month value to a variable.
        mode_month = month_number_to_words[int(mode_month)] #assigns mode_month to a dictionary value.
        print("The most common month was {}.".format(mode_month)) #prints out the mode month with words. 
        #I put mode_month inside int() just in case this datetime stuff fails somehow.  

    # display the most common day of week
    if day == 'all':
        mode_day = df['Day of Week'].mode()[0]
        print("The most common day of the week was {}.".format(mode_day))
    
    # display the most common start hour
    mode_hour = df['Start Hour'].mode()[0]
    if int(mode_hour) in hour_number_to_words.keys():
        mode_hour = hour_number_to_words[mode_hour]
    print("The most common starting hour was {}.".format(mode_hour))

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('^V^v^'*8)
    print('V^v^v'*8)
    

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # The following lines the most commonly used start station:
    mode_start_station = df['Start Station'].mode()[0]
    print("The most common starting station was:\n{}.\n".format(mode_start_station))
    
    # The following lines display the most commonly used end station:
    mode_end_station = df['End Station'].mode()[0]
    print("The most common station of arrival was:\n{}.\n".format(mode_end_station))
    
    # The following lines create a new column by adding the start and end station strings
    df['Start & End Stations'] = df['Start Station'] + " to " + df['End Station']
    mode_station_combo = df['Start & End Stations'].mode()[0]
    print("The most common trip was from:\n{}.".format(mode_station_combo))
    #   ↓↑ Used in testing accuracy of my results ↑↓  
    #print(df['Start Station'].value_counts())
    #print(df['End Station'].value_counts())
    #print(df['Start & End Stations'].value_counts())

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('^V^v^'*8)
    print('V^v^v'*8)
    

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # The following line sums the seconds for all values in the Trip Duration column:
    total_time_in_secs = df['Trip Duration'].sum() 
    
    #total_seconds in Chicago = 280871787  ← ← test metric
    seconds_per_year = 31536000
    seconds_per_day = 86400
    seconds_per_hour = 3600
    seconds_per_min = 60

    # The following statements convert Trip Duration from seconds to other equivalents:
    total_years =              total_time_in_secs // seconds_per_year
    remainder_secs_from_year = total_time_in_secs % seconds_per_year
    
    remainder_days =           remainder_secs_from_year // seconds_per_day
    remainder_secs_from_day =  remainder_secs_from_year % seconds_per_day

    remainder_hours =          remainder_secs_from_day // seconds_per_hour
    remainder_secs_from_hour = remainder_secs_from_day % seconds_per_hour

    remainder_minutes =        remainder_secs_from_hour // seconds_per_min
    remainder_secs_from_min =  remainder_secs_from_hour % seconds_per_min
    
    # The following lines assign, append, and print the calculated values into an easily digestable format:
    readable_total_time = "{} year(s), {} day(s), ".format(total_years, remainder_days)
    readable_total_time += "{} hour(s), {} minute(s), ".format(remainder_hours, remainder_minutes)
    readable_total_time += "{} second(s).\n".format(remainder_secs_from_min)
    print("Total travel time among specified set of users: \n" + readable_total_time)

    # The following lines find the mean travel time and the calculates minutes and 
    # leftover seconds from the mean in or to print the values in a digestable format:
    mean_time_spent = df['Trip Duration'].mean() #Finds and assigns mean travel time.
    mean_minutes = mean_time_spent // seconds_per_min #Finds and assigns the minute value of the mean.
    mean_leftover_secs = mean_time_spent % seconds_per_min #Finds and assigns the seconds value of the mean.
    readable_mean_time = "{} minutes, {} second(s).".format(int(mean_minutes), int(mean_leftover_secs))
    print("Mean travel time among the specified set of users:\n" + readable_mean_time) 


    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('^V^v^'*8)
    print('V^v^v'*8)

    
def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # The following lines tally up the user counts by type using the value_counts method
    user_type_count = df['User Type'].value_counts()
    print("Here's the tally of users by type:")
    print(user_type_count)
    print("")

    #++++++++++++++++++++++++++ In Limbo ++++++++++++++++++++++++++++    
    # The following code is just stuff I messed around with. The problem
    # is that dependents aren't always in the set of results and I assume
    # this would cause an error that I would have to fix with an if block.
    # Moreover, I think it's possible that customers could be higher than
    # subcribers at some point, which may assign the wrong value to the
    # wrong variable. but I might try to make it work some time in the future:    
    
    # subscriber_count = df['User Type'].value_counts()[0]
    # customer_count= df['User Type'].value_counts()[1]
    # dependent_count= df['User Type'].value_counts()[2]
    
    # user_counts =  "Subscribers: {} \n".format(subscriber_count)
    # user_counts += "Customers:   {} \n".format(customer_count)
    # user_counts += "Dependents:  {}".format(dependent_count)
    # print(user_counts)
    #++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

    # Displays counts of gender using the value_counts method if Gender exists as a column
    if 'Gender' in df.columns:
        print("Here's the breakdown by gender:")
        gender_counts = df['Gender'].value_counts()
        print(gender_counts)
        print("")

    # The following lines gather their specified age values into variables if Birth Year exists as a column
    if 'Birth Year' in df.columns:
        eldest_birth_year = df['Birth Year'].min() #Finds the oldest user's birth year
        youngest_birth_year = df['Birth Year'].max() #Finds the youngest user's birth year
        mode_birth_year = df['Birth Year'].mode() #Finds the most common birth year
    
        # The following lines display earliest, most recent, and most common year of birth.
        print("Here's the breakdown by age:")
        age_info = "Eldest User Birth Year: {}\n".format(int(eldest_birth_year))
        age_info += "Youngest User Birth Year: {}\n".format(int(youngest_birth_year))
        age_info += "Average User Birth Year: {}".format(int(mode_birth_year))
        print(age_info) #prints the gathered metrics about age in one disjointed string.
        #print(df['Birth Year'].describe()) 

    print("\nThis took %s seconds.\n" % (time.time() - start_time))
    print('^V^v^'*8)
    print('V^v^v'*8)

    
def display_data(df): #errr, forgot to comment
    #start_time = time.time()
    user_query = "\nWould you like to see some raw data?\n"
    user_input_message = "Enter 'n' to quit or enter any other value to proceed with the data: " 
    again = "\nWould you like to see even more raw data?\n"
    j = 0 #initializes the starting point of the range  in a for-loop
    k = 5 #initializes the ending point of range used in a for-loop
  
    while True: #err, I noticed in my re-re-submission that I messed up the for loop with regards to 'j' and 'k' 
        if j == 0: #if j = 0 then a certain message is written
            request = input(user_query + user_input_message).lower().strip()
        else: #if j becomes any other value, a new, grammatically correct message is written
            request = input(again + user_input_message).lower().strip()

        if request != 'n': #an if-block that runs if the user inputs any value other than 'n'
            print("Alright. Here's some raw data: \n")
            for i in range(j,k): #a loop that keeps going and going so long as the user doesn't enter 'n'
                print(df.iloc[i]) #prints the row designated by position relative to the values of j and k
                print('\n')
                j += 1 #updates j to a new starting point
                k += 1 #updates k to a new ending point
        else:#break out of the while loop if the user chooses anything other than 'n'
            break 
        

      
def main():    
    # The following lines initiate city, month, and day variables for use.
    city = ""
    month = ""
    day = ""
    
    while True:
        city, month, day = get_filters()
        #**** This IF-Block displays the user's choices in a mostly grammatically-correct way ****        
        if month != 'all' and day != 'all':
            print("\nAlright. {}, filtered by {}s in the month of {}:".format(city.title(), day.title(), month.title()))
        elif month == 'all' and day != 'all':
            print("\nAlright. {}, filtered by {}s.".format(city.title(), day.title()))
        elif month != 'all' and day == 'all':
            print("\nAlright. {}, filtered by the month of {}:".format(city.title(), month.title()))
        else:
            print("\nAlright. Here's the data for {}:".format(city.title()))
        #*****************************************************************************************
             
        df = load_data(city, month, day) #assigns whatever is chose in the function to the dataframe df. 
        #↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓ A problem ↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓↓
        #     It was fine orignially, but I messed up the variable scope and by the     
        #     time I finished my program, it was too late to try and fix time_stats()   
        #     such that it didn't require any arguements. Oh wellz                        
        time_stats(df, month, day)
        #↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑↑
        station_stats(df) #calls station_stats() to act on df.
        trip_duration_stats(df) #calls trip_duration_stats() to act on df.
        user_stats(df) #calls user_stats() to act on df.
        display_data(df) #calls display_data() to act on df.

#     Test stuff ↓         
        #print(df.iloc[0])
        #print(df.iloc[1])
        #print(month)
        
        restart = input("\nEnter 'n' to quit OR enter any other value to restart and make a new city selection: ")
        if restart.lower().strip() == 'n':
            break #quits if the user enters 'n'. Restarts the program from the beginning if the user enter any other value.
        
if __name__ == "__main__":
	main()
