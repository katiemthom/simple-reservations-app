"""
Reservation finder

Along with this file, you'll find two files named units.csv 
and reservations.csv with fields in the following format

units.csv
location_id, unit_size

reservations.csv
location_id, reservation_start_date, reservation_end_date

You will write a simple application that manages a 
reservation system. It will have two commands, 
'available' and 'reserve' with the following behaviors:

available <date> <number of occupants> <length of stay>
This will print all available units that match the 
criteria. Any unit with capacity equal or greater to 
the number of occupants will be printed out.

Example:
SeaBnb> available 10/10/2013 2 4
Unit 10 (Size 3) is available
Unit 20 (Size 2) is available

reserve <unit number> <start date> <length of stay>
This creates a record in your reservations that indicates
the unit has been reserved. It will print a message 
indicating its success.

A reservation that ends on any given day may be rebooked 
for the same evening, ie:
    
    If a reservation ends on 10/10/2013, a different 
    reservation may be made starting on 10/10/2013 as well.

Example:
SeaBnb> reserve 10 10/11/2013 3 
Successfully reserved unit 10 for 3 nights

Reserving a unit must make the unit unavailable for 
later reservations. Here's a sample session:

SeaBnb> available 10/10/2013 2 4
Unit 10 (Size 3) is available
Unit 20 (Size 2) is available
SeaBnb> reserve 10 10/11/2013 3 
Successfully reserved unit 10 for 3 nights
SeaBnb> available 10/10/2013 2 4
Unit 20 (Size 2) is available
SeaBnb> reserve 10 10/11/2013 3 
Unit 10 is unavailable during those dates
SeaBnb> quit

Notes:
Start first by writing the functions to read in the 
csv file. These have been stubbed for you. Then 
write the availability function, then reservation. 
Test your program at each step (it may be beneficial 
to write tests in a separate file.) Use the 'reservations'
variable as your database. Store all the reservations 
in there, including the ones from the new ones you 
will create.

The datetime and timedelta classes will be immensely
helpful here, as will the strptime function.
"""

import sys
import datetime
import time

def parse_one_record(line):
    """Take a line from reservations.csv and return a 
    dictionary representing that record. (hint: use 
    the datetime type when parsing the start and 
    end date columns)"""
    #location_id, reservation_start_date, reservation_end_date
    reservation_info = line.split(",")
    for i in range(len(reservation_info)): 
        reservation_info[i] = reservation_info[i].strip()
    start_date = time.strptime(reservation_info[1],"%m/%d/%Y")
    end_date = time.strptime(reservation_info[2],"%m/%d/%Y")
    reservation_dict = {"location_id": reservation_info[0], "reservation_start_date": start_date, "reservation_end_date": end_date}
    return reservation_dict

def read_units():
    """Read in the file units.csv and returns a list of 
    all known units."""
    #units = [(location_id, unit_size)]
    units_file = open('units.txt', 'r')
    units_list = []
    for line in units_file: 
        unit_info = line.split(",")
        units_list.append((unit_info[0],unit_info[1]))
    return units_list

def read_existing_reservations():
    """Reads in the file reservations.csv and 
    returns a list of reservations."""
    # dictionary = {id:[(start, end), (start, end)], etc.}
    reservations_dict = {}
    reservations_file = open('reservations.txt', 'r')
    for line in reservations_file: 
        reservation_dict = parse_one_record(line)
        unit_id = reservation_dict["location_id"]
        start_date = reservation_dict["reservation_start_date"]
        end_date = reservation_dict["reservation_end_date"]
        reservations_dict[unit_id] = reservations_dict.get(unit_id,[])
        reservations_dict[unit_id].append((start_date,end_date))
    reservations_file.close()
    return reservations_dict

def available(units, reservations, start_date, occupants, stay_length):
    # units: list of units
    # units = [(location_id, unit_size)]
    # reservations: dict:
    # dictionary = {id:[(start, end), (start, end)], etc.}
    available_units_list = is_available(units, reservations, start_date, occupants, stay_length)
    for unit in available_units_list: 
        print "Unit %s is available" % unit

def is_available(units, reservations, start_date, occupants, stay_length):
    available_units_list = []
    for unit in units: 
        unit_id = unit[0].strip()
        unit_size = unit[1].strip()
        if int(occupants) > int(unit_size): 
            continue
        reservations_list = reservations.get(unit_id, [])
        desired_start = time.strptime(start_date,"%m/%d/%Y")
        desired_start = datetime.date(desired_start[0],desired_start[1],desired_start[2])
        desired_end = desired_start + datetime.timedelta(days=int(stay_length))
        # reservations list: [(start,end),(stard,end),etc.]
        unit_available = True 
        for reservation in reservations_list: 
            reservation_start = reservation[0]
            reservation_start = datetime.date(reservation_start[0],reservation_start[1],reservation_start[2])
            reservation_end = reservation[1]
            reservation_end = datetime.date(reservation_end[0],reservation_end[1],reservation_end[2])
            if reservation_start < desired_start < reservation_end or reservation_start < desired_end < reservation_end:
                unit_available = False
                continue
        ## make overlap function
        ## if start2 > end 1 or start1 >= end2 # not overlap
        if unit_available: 
            available_units_list.append(unit_id) 
    return available_units_list

def reserve(units, reservations, unit_id, start_date, stay_length):
    available_units_list = is_available(units, reservations, start_date, 1, stay_length)
    if unit_id in available_units_list:
        desired_start = time.strptime(start_date,"%m/%d/%Y")
        desired_start = datetime.date(desired_start[0],desired_start[1],desired_start[2])
        desired_end = desired_start + datetime.timedelta(days=int(stay_length))
        reservations[unit_id] = reservations.get(unit_id,[])
        reservations[unit_id].append((desired_start,desired_end))
        print "Successfully reserved"
    else: 
        print "Sorry you can't reserve that. :("

def main():
    units = read_units()
    reservations_dict = read_existing_reservations() 

    while True:
        command = raw_input("SeaBnb> ")
        cmd = command.split()
        if cmd[0] == "available":
            available(units, reservations_dict, *cmd[1:])
        elif cmd[0] == "reserve":
            reserve(units, reservations_dict, *cmd[1:])
        elif cmd[0] == "quit":
            sys.exit(0)
        else:
            print "Unknown command"

if __name__ == "__main__":
    main()