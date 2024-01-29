'''
Data source:
Institute for Health Metrics and Evaluation (IHME). Global Fertility, Mortality, Migration, and Population Forecasts 2017-2100. Seattle, United States of America: Institute for Health Metrics and Evaluation (IHME), 2020.
https://doi.org/10.6069/MJND-3671
'''


import pandas as pd
from data import *

data = pd.read_csv("IHME_POP_2017_2100_POP_REFERENCE_Y2020M05D01 2.CSV")

def global_year (year): # global population in a year
  worldwide = data.loc[(data['location_name'] == 'Global') &       (data['year_id'] == year)] # all Global data in a year
  global_population = worldwide['val'].sum()//2 # add the Global data in a year, divide by 2 to correct for double counting from the data labeled "All Ages"
  return(global_population)


def global_change(year1, year2): # change of the global population from one year to another
  global_population_1 = global_year(year1)
  global_population_2 = global_year(year2)
  global_change = global_population_2 - global_population_1
  rate_of_change = global_change/global_population_1 # new population as a percentage of the old population
  return(rate_of_change)


def peak_population():
  max = 0
  year = 0
  for i in range(2024, 2101): # 2024 included, 2101 excluded
    worldwide = data.loc[(data['location_name'] == 'Global') & (data['year_id'] == i)]
    global_population = worldwide['val'].sum()//2 # global population in a year; divide by 2 to correct for double counting from the data labeled "All Ages"
    if global_population > max:
      max = global_population # greatest population
      year = i # year with the greatest population
  print("Peak Population: ", max, "in", year)


def get_countries():
  for k, v in countries.items(): # k = country code, v = country name
    print(k, v, "\n")


def rank_countries(year):
  ranked_list = []
  for country in countries:
    national = data.loc[(data['location_id'] == country) & (data['year_id'] == year)] # population of each country in a year
    national_population = national['val'].sum()//2 # Divide by 2 to correct for double counting from the data labeled "All Ages"
    ranked_list.append([countries[country], national_population])
  ranked_list.sort(key=lambda x: x[1], reverse=True)  # Sorting by population in descending order
  return ranked_list


def rank_change(country, year1, year2): # change in a country's rank from one year to another
  ranked_list_1 = rank_countries(year1) # rank of all countries in the starting year
  country_rank_1 = ranked_list_1.index(next(item for item in ranked_list_1 if item[0] == countries[country])) # rank of the specific country under investigation
  ranked_list_2 = rank_countries(year2) # rank of all countries in the ending year
  country_rank_2 = ranked_list_2.index(next(item for item in ranked_list_2 if item[0] == countries[country])) # rank of the specific country under investigation
  rank_change = (country_rank_1 - country_rank_2) # change in rank
  print (rank_change, "from", country_rank_1 + 1, "to", country_rank_2 + 1) # adding 1 to account for indexing


def rank_x_in_year(rank, year): # which country has a certain rank in a certain year
  ranked_list = rank_countries(year)
  country = ranked_list[rank-1][0] # country name at the specified rank; minus 1 to account for indexing
  print(country)


def rank_in_year(country, year): 
  ranked_list = rank_countries(year)
  rank = ranked_list.index(next(item for item in ranked_list if item[0] == countries[country])) # find the place of the country name in the ranked list
  rank += 1 # adding 1 to account for indexing
  print(rank)


def most_changed(year1, year2): # which country has the greatest change in population from one year to another
  #max = 0
  ranked_list = []
  for country in countries:
    country1 = national_population(country, year1) # population in the starting year
    country2 = national_population(country, year2) # population in the ending year
    country_change = country2 - country1 # change in population from one year to the other
    ranked_list.append([countries[country], country_change])
  ranked_list.sort(key=lambda x: x[1], reverse=True)  # Sorting by population change in descending order
  return ranked_list


def national_population(country, year): # population of a country in a certain year
    national = data.loc[(data['location_id'] == country) &       (data['year_id'] == year)] # data with the specified country code and year
    national_population = national['val'].sum()//2 # sum of the values of the specified data; divide by 2 to correct for double counting from the data labeled "All Ages"
    return(national_population)


def age_share(age_group1, age_group2, year): # the percentage of the global population that is a certain age range (e.g., children, adolescents)
  sum = 0
  for age_group in age_groups:
    if age_group >= age_group1 and age_group <= age_group2: # if age group falls in the specified range
        age_data = data.loc[(data['location_name'] == 'Global') & (data['age_group_id'] == age_group) & (data['year_id'] == year)] # data for that age group and year across gender and nation
        age_years_data = age_data['val'].sum()
        sum += age_years_data # accumulator for all the age groups included
  share = round(sum/global_year(year), 4)
  return(share)


def age_share_rank (age_group1, age_group2, year): # for a certain age group range, which country has the greatest share of the global population that is in that age range
  ranked_list = []
  for country in countries:
    sum = 0
    for age_group in age_groups:
      if age_group >= age_group1 and age_group <= age_group2: # if age group falls in the specified range
        age_data = data.loc[(data['location_id'] == country) & (data['age_group_id'] == age_group) & (data['year_id'] == year)] # all data for that country, age group, and year across gender
        age_years_data = age_data['val'].sum()
        sum += age_years_data # accumulator for the different age groups within the age group range
    share = round(sum/national_population(country, year), 4) # percentage of the country's population that is in the specified age range
    ranked_list.append([countries[country], share])
  ranked_list.sort(key=lambda x: x[1], reverse=True) # countries ranked in descending order by share
  for i in range(0, len(ranked_list)): 
    print(i + 1, ")", ranked_list[i][0], ranked_list[i][1], '\n')


def age_share_year(age_group1, age_group2): # the percentage of the global population that is in a certain age range each year
  max = 0
  year = 0
  for i in range (2024, 2101): # all years (2101 not included)
    share = age_share(age_group1, age_group2, i) # percentage of the global population that is in the specified age range that year
    if share > max: # share of the current year is greater than the share of the previous year
      max = share
      year = i
  print("Year with highest share: ", year, "with share of", max)


def population_target(population): # the year when the global population hits a certain number
  for i in range(2024, 2101): # all years (2101 not included)
    global_population = global_year(i) # global population in a year
    if global_population >= population: # that year, the global population reaches or exceeds the target population
      print("Year with target population: ", i + 1)
      break # This function finds the earliest year in which the global population hits the target population. Once this year is found, traversing the years that come after is not necessary. 


def growth_rate_per_year(): # of the global population
  for i in range (2024, 2100):
    rate_of_change = global_change(i, i+1) # change from one year to the following year
    print(i, " to ", i + 1, ": ", rate_of_change, "\n")


def growth_rate_per_decade(): # of the global population
  for i in range (2020, 2100, 10): # measure for every 10 years
    rate_of_change = global_change(i, i+10)
    print(i, " to ", i + 10, ": ", rate_of_change, "\n")


def country_peak_population(country): # the peak population of a country and the year in which this occurred
  max = 0
  year = 0
  for i in range(2024, 2101): # 2101 not included
    national = data.loc[(data['location_id'] == country) & (data['year_id'] == i)] # data for that country and year
    national_population = national['val'].sum()//2 # divided by 2 to correct for double counting from the data labeled "All Ages"
    if national_population > max: # population exceeds the population of the previous year
      max = national_population
      year = i
  print("Peak Population: ", max, "in", year)


def top_five(): # changes in the five most populous countries, and in which year these changes occur
  starting_countries = rank_countries(2024) # current top five countries as a baseline
  starting_case = [starting_countries[0][0], starting_countries[1][0], starting_countries[2][0], starting_countries[3][0], starting_countries[4][0]] # top five countries from the ranked list
  print(2024, starting_case)
  for i in range (2025, 2100): # 2100 not included
    first_list = rank_countries(i)
    first_case = [first_list[0][0], first_list[1][0], first_list[2][0], first_list[3][0], first_list[4][0]]
    next_list = rank_countries(i+1)
    next_case = [next_list[0][0], next_list[1][0], next_list[2][0], next_list[3][0], next_list[4][0]]
    if next_case != first_case:
      print(i, next_case)
  ending_countries = rank_countries(2100) # top five countries in 2100
  end_case = [ending_countries[0][0], ending_countries[1][0], ending_countries[2][0], ending_countries[3][0], ending_countries[4][0]] # top five countries from the ranked list
  if end_case != next_case: # if the top five changes in 2100
    print(2100, end_case)


def national_change (year1, year2): # change in a country's population from one year to another
  ranked_list = []
  for country in countries:
    national_population_1 = national_population(country, year1) # starting year
    national_population_2 = national_population(country, year2) # ending year
    national_change = national_population_2 - national_population_1 # change from starting year to ending year
    rate_of_change = round(national_change/national_population_1, 4) # change as a percentage of the starting year
    ranked_list.append([countries[country], rate_of_change])
  ranked_list.sort(key=lambda x: x[1], reverse=True)  # Sorting by population change in descending order
  return ranked_list


def country_growth_rate_per_year(country):
  for i in range (2024, 2100):
    rate_of_change = national_change(country, i, i+1)
    print(i, " to ", i + 1, ": ", rate_of_change, "\n")


def country_growth_rate_per_decade(country):
  for i in range (2020, 2100, 10): # increments by decade
    rate_of_change = national_change(country, i, i+10) # change from beginning to end of decade
    print(i, " to ", i + 10, ": ", rate_of_change, "\n")


def country_age_distribution(country, year): # in a certain year, the percentage of a country's population that is in each age group
  for age_group in age_groups:
    age_data = data.loc[(data['location_id'] == country) & (data['age_group_id'] == age_group) & (data['year_id'] == year)] # data for the country, age group, and year across gender
    age_data_year = age_data['val'].sum()
    share = round(age_data_year/national_population(country, year), 4) # percentage of the country's population that is in the specified age group
    print(age_groups[age_group], ": ", share)


def age_distribution(year): # global
  for age_group in age_groups:
    age_data = data.loc[(data['location_name'] == 'Global') &(data['age_group_id'] == age_group) & (data['year_id'] == year)]
    age_data_year = age_data['val'].sum() 
    share = round(age_data_year/global_year(year), 4)
    print(age_groups[age_group], ": ", share)


def average_decade_age_share(index1, index2, year1, year2): # global
  sum_of_shares = 0
  for i in range(year1, year2): # in a decade
    sum = 0
    for j in range(index1, index2): # in a broad age group
      age_data = data.loc[(data['location_name'] == 'Global') &(data['age_group_id'] == j + 2) & (data['year_id'] == i)] # age group codes are 2 more than their indices in the age_groups dictionary
      age_data_year = age_data['val'].sum()
      sum += age_data_year # broad age group that year
    share = sum/global_year(i) # percentage of world population that year
    sum_of_shares += share # accumulator working towards 10 years
  decade_average = round(sum_of_shares/10, 4)
  return(decade_average)


def average_decade_age_share_eighties_plus(age_code1, age_code2, year1, year2): # this function is needed because age codes for this group are not consecutive with respect to the age codes of previous groups
  sum_of_shares = 0
  for i in range(year1, year2): # in a decade
    age_data_1 = data.loc[(data['location_name'] == 'Global') &(data['age_group_id'] == age_code1) & (data['year_id'] == i)]
    age_data_year_1 = age_data_1['val'].sum()
    age_data_2 = data.loc[(data['location_name'] == 'Global') &(data['age_group_id'] == age_code2) & (data['year_id'] == i)]
    age_data_year_2 = age_data_2['val'].sum()
    sum = age_data_year_1 + age_data_year_2 # broad age group that year
    share = sum/global_year(i) # percentage of world population that year
    sum_of_shares += share # accumulator working towards 10 years
  decade_average = round(sum_of_shares/10, 4) # the average of annual population shares over 10 years
  return(decade_average)


def largest_age_decade():
  largest_age_groups = [] # list of the largest age group in each decade
  for i in range(2020, 2100, 10): # increment by 10 to begin the following decade
    decade_average = [] # list of age shares of each age range
    children = average_decade_age_share(0, 5, i, i+10) # children 0-9 are comprised by 5 age groups
    decade_average.append(children)
    for j in range(5, 19, 2): # most broad age groups in the decade
      decade_average.append(average_decade_age_share(j, j + 2, i, i+10)) # age codes are 2 more than their indices in the age_groups dictionary
    decade_average.append(average_decade_age_share_eighties_plus(30, 31, i, i+10)) # eighties
    decade_average.append(average_decade_age_share_eighties_plus(32, 235, i, i + 10)) # nineties plus
    largest_age_share = max(decade_average) # the largest age share in the list of age shares
    index = decade_average.index(largest_age_share) # the index of the list of age shares that corresponds to the largest age share
    largest_age_group = broad_age_groups[index] # the indices of the list of age shares correspond with the indices of the broad_age_groups list
    largest_age_groups.append([largest_age_group, largest_age_share])
  for k in range(0, len(decades)):
    print(decades[k], ": ", largest_age_groups[k][0], " -- ", largest_age_groups[k][1]) # print the decades and their largest age groups


def main():
  get_countries() # provides alphabetical list of countries and their country codes so users can reference the country codes when inputting data
  while True: # menu is presented after each function is run so that users can run as many functions as they want before deciding to quit
    menu_input = input("Press m for menu: ")
    if menu_input == "m":
      print("\n")
      print(menu)
      selection = input("Select a number or press q to quit: ")
      print("\n")
      
      if selection == '1':
        year = int(input("Enter a year: "))
        print("\n")
        print(global_year(year))

      elif selection == '2':
        year1 = int(input("Starting year: "))
        year2 = int(input("Ending year: "))
        print("\n")
        print(global_change(year1, year2))

      elif selection == '3':
        print("\n")
        peak_population()

      elif selection == '4':
        print("\n")
        get_countries()

      elif selection == '5':
        year = int(input("Enter a year: "))
        ordered_list = rank_countries(year)
        print("\n")
        for i in range(0, len(ordered_list)): 
          print(i + 1, ")", ordered_list[i][0], ordered_list[i][1], '\n')

      elif selection == '6':
        country = int(input("Enter a country code: "))
        year1 = int(input("Starting year: "))
        year2 = int(input("Ending year: "))
        print("\n")
        rank_change(country, year1, year2)

      elif selection == '7':
        rank = int(input("Enter a rank: "))
        year = int(input("Enter a year: "))
        print("\n")
        rank_x_in_year(rank, year)

      elif selection == '8':
        country = int(input("Enter a country code: "))
        year = int(input("Enter a year: "))
        print("\n")
        rank_in_year(country, year)

      elif selection == '9':
        year1 = int(input("Starting year: "))
        year2 = int(input("Ending year: "))
        print("\n")
        ordered_list = most_changed(year1, year2)
        for i in range(0, len(ordered_list)): 
          print(i + 1, ")", ordered_list[i][0], ordered_list[i][1], '\n')

      elif selection == '10':
        country = int(input("Enter a country code: "))
        year = int(input("Enter a year: "))
        print("\n")
        print(national_population(country, year))

      elif selection == '11':
        for k, v in age_groups.items():
          print(k, v, "\n")
        print("Select an age group or age range and a year.")
        age_group1 = int(input("Age group code (start of range): "))
        age_group2 = int(input("Age group code (end of range): "))
        year = int(input("Enter a year: "))
        print("\n")
        print(age_share(age_group1, age_group2, year))

      elif selection == '12':
        for k, v in age_groups.items():
          print(k, v, "\n")
        age_group1 = int(input("Age group code (start of range): "))
        age_group2 = int(input("Age group code (end of range)"))
        year = int(input("Enter a year: "))
        print("\n")
        age_share_rank(age_group1, age_group2, year)

      elif selection == '13':
        for k, v in age_groups.items():
          print(k, v, "\n")
        age_group1 = int(input("Age group code (start of range): "))
        age_group2 = int(input("Age group code (end of range): "))
        print("\n")
        age_share_year(age_group1, age_group2)

      elif selection == '14':
        population = int(input("Enter a population target: "))
        print("\n")
        population_target(population)

      elif selection == '15':
        print("\n")
        growth_rate_per_year()

      elif selection == '16':
        print("\n")
        growth_rate_per_decade()

      elif selection == '17': 
        country = int(input("Enter a country code: "))
        print("\n")
        country_peak_population(country)

      elif selection == '18':
        print("\n")
        top_five()

      elif selection == '19':
        country = int(input("Enter a country code: "))
        print("\n")
        country_growth_rate_per_year(country)

      elif selection == '20':
        country = int(input("Enter a country code: "))
        print("\n")
        country_growth_rate_per_decade(country)

      elif selection == '21':
        year1 = int(input("Starting year: "))
        year2 = int(input("Ending year: "))
        print("\n")
        ordered_list = national_change(year1, year2)
        print("\n")
        for i in range(0, len(ordered_list)): 
          print(i + 1, ")", ordered_list[i][0], ordered_list[i][1], '\n')

      elif selection == '22':
        country = int(input("Enter a country code: "))
        year = int(input("Enter a year: "))
        print("\n")
        country_age_distribution(country, year)

      elif selection == '23':
        year = int(input("Enter a year: "))
        print("\n")
        age_distribution(year)

      elif selection == '24':
        print("\n")
        largest_age_decade()

      elif selection == 'q':
        break

      else:
        print("Invalid input")




if __name__ == "__main__":
  main()