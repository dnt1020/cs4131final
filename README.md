# csci4131final
Made a website for users to look up wine and food pairings and write reviews for them. 

Main features:
  - User can look up pairings
  - Pairings is stored as history
  - Reviews can be left for pairings

Walkthrough covering features: register and log in, choose food/wine to look up (try food = steak), click a pairing after look up to see pairing page, look at reviews and write reviews for pairings, click on profile to look at history and reviews you have left

Here are the requirements for an A for the project and how they are covered (Left out some extra controller, templates etc. used in website).

Controllers: 
  - /index - main page used for searching
  - /pairs - does API call on spoonacular to find pairings
  - /user/<username> - show profile of a user as well as their reviews and pairing they looked at previously
  
Templates:
  - Profile - profile of user as well as their reviews and pairing they looked at previously 
  - Index - main page to search for pairs
  - Pair - show pairs as well as their reviews and submission of reviews
  
Session Management: users log in to keep track of their reviews and previous pairs they found

Databases: 
  - User - store user information
    - each user can create multiple history and reviews
  - Pair - stores pairs users look up - no duplicate pairs
    - each pair has multiple history and multiple reviews
  - History - everytime the user clicks on the pair it is stored in their history
  - Reviews - reviews user leaves on pairs
  
Forms: used for submitting info into the databases

Web API: spoonacular API is used to find pairings

Bootstrap Template: Lumia Template from https://bootstrapmade.com/lumia-bootstrap-business-template/
