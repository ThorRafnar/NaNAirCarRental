# NaNAirCarRental
Verklegt námskeið 1, mvp group 22

For best results, run the program in full screen, other sizes are  partly supported, but might cause issues.

Vehicle rates are the same across all locations  and differ only by vehicle type, eg. Medium water is the same price in Nuuk and Longyearbyen.
They are changable and viewable by office employees and administrators, but not airport staff. All rates are in icelandic kronur (ISK / Kr.)

Locations' opening hours are an attribute of each location (destination). Opening hours are different for each location (but allows duplicates), 
meaning each location has its own opening hours.

Employees, customers and vehicles cannot be removed from the database through the program. Vehicles can be put in the workshop if they are unusable
Contracts can be terminated and this will remove them from the database.

In the system there are three priviledge types, administrator, office and airport employee. They have different rights. 
Administrators and office employees can find and create destinations/locations but airport employees can only view a list of all airports.
Admins and office can create contracts and modify them (start and end date or vehicle) or terminate them. Airport employees cannot

Contracts can be modified, start date, end date and vehicle can be modified if the contract is pending.
if the contract is active the end date can be modified but start and vehicle cannot.
A contract can be terminated if and only it's status is pending. An active, returned or paid cannot be terminated.

Contracts can be billed only if the status is returned. This is to prevent a person from paying and then extending the date or returning late.
Because of this, contracts are paid in full every time, and all chanrges will have been calculate by then.
