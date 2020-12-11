# NaNAirCarRental
Verklegt námskeið 1, mvp group 22

To run the program, cd to src and run the command "python3 run.py"

For best results, run the program in full screen, other sizes are  partly supported, but might cause issues. After starting, do not change terminal size

Airport employees can register new vehicles.
All staff types can view vehicles and their details.
The view available option shows all vehicles in a given location that are currently rentable. Note that it does not take into account vehicles that might be 
picked up later during that day or later that week, however when picking a vehicle in contracts, that is taken care of.
If user is an airport employee they do not need to choose a location, and will see available vehicles in their location. KEF/office employees will need to choose
a location to view.

When creating a vehicle, if user enters a non existing vehicle type they will be informed that it doesn't exist and prompted if they want
to create it. They will then decide the rate and confirm, and their new vehicle will have that as its type.

Vehicle rates are the same across all locations  and differ only by vehicle type, eg. Medium water is the same price in Nuuk and Longyearbyen.
They are changable and viewable by office employees and administrators, but not airport staff. All rates are in icelandic kronur (ISK / Kr.)
Any staff type can view and change vehicle rates.

Locations' opening hours are an attribute of each location (destination). Opening hours are different for each location (but allows duplicates), 
meaning each location has its own opening hours.

Employees, customers and vehicles cannot be removed from the database through the program. Vehicles can be put in the workshop if they are unusable
Contracts can be terminated and this will remove them from the database.

All staff types can create, modify and list all other employees, per A demands.

In the system there are two priviledge types, office and airport employee. They have different rights. 
We intereperated the demands so that there only need to be two types. We initially planned to include admin access, but found it redunant in regards to B demands
Office employees can find and create destinations/locations but airport employees can only view a list of all airports.
Office employees can create contracts and modify them (start and end date or vehicle) or terminate them. Airport employees cannot

Office employees can modify contracts:
Contracts can be modified, start date, end date and vehicle can be modified if the contract is pending.
if the contract is active the end date can be modified but start and vehicle cannot.
A contract can be terminated if and only it's status is pending. An active, returned or paid cannot be terminated.

Contracts can be billed only if the status is returned. This is to prevent a person from paying and then extending the date or returning late.
Because of this, contracts are paid in full every time, and all chanrges will have been calculate by then.

Airport employees can check out and return vehicles, and when returning the system makes sure that they are returning a valid vehicle for their location, 
and that the vehicle is in an active contract

Profits reports support only up to 13 vehicle types, before the formatting gets out of hand. Given more time this could be fixed but at the moment it is not feasible

When creating a contract, employee, vehicle or customer, if you go back, it will return to the menu before you started, losing your information.

No error checking is in place to make sure that start date is earlier than the end date. Given more time we would have implented such check but as of now, it is "allowed" but it will 
calculate the price as a negative number. So just don't do that please.