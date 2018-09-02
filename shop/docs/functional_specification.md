# Functional Specification for the Oasis Shop

### Abstract and Basic Requirements:
All students on campus are either a Bitsian or an Outstation particiapant. Accordingly, each Consumer of our app will have a User instance and an associated Bitsian and/or Participant instance (both of which can be found in the registrations app). Each Consumer will be associated with a Wallet Instance using which they can pay for offerings from the Producers and for paying each other i.e. performing transactions.

All Producers of our app will be the people at the stalls who declare menu items, their quantity, nature (veg/non-veg), etc. and will take orders from the Consumers. They are represented in our app by means of a User instance along with a Stall instance.

The orders can be made to several stalls at once. So accordingly, the front-end team has declared how they will be relaying data to us in the backend team (see "frontend\_order_structure.jpg"). We can fragment a single large order into several composite orders. When ordering each user will have an associated cart with persistance.

This is the general idea behind the shop applications.

### Classes Involved:

Refer to the UML diagram: "Models_UML.png"


### Notes:

The definition of "Cart" is: "a temporary yet persistant storage place where the customer can add and remove items from in order to decide on their order. Once satisfied, the customer can checkout his/her cart and the contents of the cart will be converted into an order and the cart will be emptied".

Explanations for every model can be found in a docstring under the model's name in Models.py  (the same applies for methods).
