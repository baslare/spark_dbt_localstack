CREATE TABLE Aeroplane
(
aeroplane_id int NOT NULL,
aeroplane_model char NOT NULL,
aeroplane_manufacturer char NOT NULL,
PRIMARY KEY(aeroplane_id)
);


CREATE TABLE Customer
(
customer_id int NOT NULL PRIMARY KEY,
name char NOT NULL,
customer_group_id int REFERENCES CustomerGroup(id),
email char,
phone_number char,
PRIMARY KEY(customer_id)

);

CREATE TABLE CustomerGroup
(
id int NOT NULL,
type char NOT NULL,
name char NOT NULL,
registry_number char,
PRIMARY KEY(id)
);


CREATE TABLE Orders
(
order_id int NOT NULL,
customer_id int NOT NULL REFERENCES Customer(customer_id),
trip_id int NOT NULL REFERENCES Trip(trip_id),
price_eur float NOT NULL,
seat_no char,
status char,
PRIMARY KEY(order_id)
);


CREATE TABLE Trip
(
trip_id int NOT NULL,
origin_city char NOT NULL,
destination_city char NOT NULL,
aeroplane_id char NOT NULL  REFERENCES Aeroplane(aeroplane_id),
start_timestamp char NOT NULL,
end_timestamp char NOT NULL,
PRIMARY KEY(trip_id)

);

