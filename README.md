# Online Tourism System Implementation Guide

The Online Tourism System developed by Wonder What Is Tourism (WAIT) Pte Ltd is a dynamic application designed to conduct global surveys on tourist attractions worldwide. This application plays a critical role in collecting and analyzing travel, tourism, and culture information, thereby optimizing destinations and enhancing visitor experiences. Through its unique features, it enables active user participation, allowing for a more comprehensive understanding of global tourism insights.

Implementation on New PC/Server

This guide will walk you through the process of setting up the Online Survey System on a new PC or server. The system is built with Python, ensuring easy deployment and scalability.

## Features
#### Dynamic Survey System
- **Global Participation**: Users from around the world can participate in surveys, offering a diverse range of insights and perspectives on tourist attractions.
- **Real-Time Data Collection**: The system collects data in real-time, allowing for up-to-date analysis and reporting on global tourism trends.

#### User Engagement
- **Interactive Voting**: Users can vote for their favorite places of interest, contributing to the ranking of top tourist destinations.
- **Feedback Mechanism**: Alongside voting, users can leave feedback on attractions, providing valuable qualitative data on visitor experiences.

#### Data Analysis and Reporting
- **Top Places and Countries**: The system automatically calculates and presents the top places and countries based on user votes, offering insights into popular destinations.
- **Search and Filter**: Users can search for specific places or filter places by country, making it easy to find detailed information on particular attractions.

#### Administration and Data Management
- **Place Management**: Administrators can add new places of interest and countries to the survey system, ensuring the database is comprehensive and up-to-date.
- **User Management**: The system supports user registration, allowing for personalized experiences and tracking of individual voting histories.

#### Technical Features
- **Flask Web Application**: Built with Flask, the system offers a lightweight and flexible web server with a user-friendly interface for both participants and administrators.
- **Scheduled Data Persistence**: Utilizes scheduled tasks to periodically save world and user data, ensuring data integrity and loss prevention.

#### Customization and Extensibility
- **Open API**: The system's API endpoints enable integration with other applications or systems, allowing for extended functionality and customization.
- **Modular Design**: Designed with modularity in mind, the system can be easily extended or modified to include additional features or adapt to changing requirements.

#### Security and Reliability
- **Data Security**: Implements best practices in data security, ensuring user information and survey data are protected.
- **System Stability**: Designed for reliability, the system can handle high volumes of user interactions and data processing without compromising performance.


## Prerequisites
- **Python 3.x**
- **Flask**
- **A modern web browser**

## Install
Adjust Flask Port (Optional for MacBook Users):

For MacBook users, change the default port from 5000 to 5050 in the Flask application file to avoid potential conflicts.

```
port = int(os.environ.get("PORT", 5000))
```
Change it to:
```
port = int(os.environ.get("PORT", 5000))
```
No extra python packages are needed to be installed in this application.





## Configuration
Environment Variables: 

Set the FLASK_APP environment variable to your application's entry point file, for example, app.py.

Unix/MacOS: export FLASK_APP=app.py

Windows Command Prompt: set FLASK_APP=app.py

Windows PowerShell: $env:FLASK_APP = "app.py"

Database and Backend Configuration: 

Review and adjust the backend configuration as needed to connect to your database and ensure proper data handling.




## API
The Online Survey System provides various API endpoints for interacting with the Flask web application. These endpoints enable users to perform actions such as adding places of interest, voting, and retrieving top places and countries. Additionally, two specific endpoints allow for filtering by country and searching for specific place data.

- `GET /`: Displays the main page with top places.
- `POST /add_place_of_interest`: Adds a new place of interest to a specified country.
- `POST /vote_for_place`: Allows a user to submit a vote for a place along with feedback.
- `GET /get_top_places`: Retrieves information about the top-rated places based on votes.
- `GET /get_top_countries`: Retrieves the top-rated countries based on the total votes of their places.
- `GET /get_id`: Generates a new unique user ID for tracking votes and history.
- `GET /history`: Returns the voting history for a specified user ID, showing the places they've voted for.
- `GET /filter_by_country`: Filters and returns all places of interest within a specified country.
  - **Parameters**:
    - `country`: The name of the country to filter places by.
  - **Returns**: A list of places within the specified country along with their vote counts. If no country name is provided or no places are found, an error message is returned.

- `GET /search`: Searches for specific place data within a country.
  - **Parameters**:
    - `country`: The name of the country where the place is located.
    - `place`: The name of the place of interest.
  - **Returns**: Detailed data about the specified place, including votes and user feedback. If the place or country cannot be found, an error message is returned.

These endpoints facilitate the dynamic interaction with the Online Survey System, allowing users to not only participate in surveys but also to explore the data collected on global tourist attractions.



## 
