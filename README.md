# CIT-225 Final Lab
### Stephen Hendricks

This lab is a culmination of everything that I've learned throughout this course. My lab here is a boilerplate
for creating a simple backend webserver in flask, and a frontend in React.

Some of the details of this project:

- React frontend built with vite and has the following features
  - Linting with ESLint
  - Unit testing with vitest
  - API mocking with msw
- The backend is built with flask and has the following features
  - A simple set of REST endpoints to get and increment a counter value
  - Render the frontend index.html file
- The project is deployed in a Docker container through kubernetes.
  - There are both dev and prod deployments which run live data tests and database rollbacks in the test environment using python with selenium.
  - pytest is used to run tests in the backend test environment
  - Dastardly is used to run security scans on the backend