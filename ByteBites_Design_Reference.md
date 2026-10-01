# ByteBites Reference File

## About This Project
You are building the backend logic for a campus food ordering app called ByteBites
using Python classes and simple algorithms.

## Project Scope
Do not add authentication logic, a database layer, or any features not described 
in the spec.

## Behavioral Instructions
<!-- Write a short set of instructions guiding how your AI assistant should behave 
when helping with this project — for example, which classes to stay within, 
what complexity to avoid, or any preferences for how suggestions are structured. -->

### Customer class
once the customer purchase_history has a transaction, the customer status should switch to verified

Customer can order multiple batch of orders

### Menu
Menu should group items by category and in each category sort by popularity

### Transaction
can handle multiple customer's multiple orders simutanously 

### menuItem
The price can be changed and the popularity rating changes higher when more customer orders this item. 