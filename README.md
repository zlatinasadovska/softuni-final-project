# Echo Music App

Echo is a Django-based web application that integrates with Spotify’s Web API to provide users with an intuitive platform for discovering, managing, and personalizing their music collections. The application allows users to explore a wide range of tracks, albums, and artists directly from Spotify’s vast music library, with features designed to enhance the user experience.

### Key Features:

- Spotify Integration: The app pulls real-time data from Spotify’s API, allowing users to browse and view detailed information about tracks, albums, and artists, without the need to manually input data.

- Track, Album, and Artist Discovery: Users can explore detailed information about individual tracks, albums, and artists, including their titles, release dates, and cover images, all sourced from Spotify.

- User Feedback System: Users can provide feedback on the app or specific music content, and this feedback is stored within the system. They can easily view and delete their feedback whenever they choose, offering complete control over their interactions.

- Playlist Management: Users have the ability to create, edit, and manage their own playlists. They can add or remove tracks to/from playlists, giving them full control over their personal music collections.

- Profile Customization: Registered users can customize their profiles by uploading a profile picture and changing their username. Password changes can also be made with proper validation to ensure security.

- Admin Panel: The Django admin interface allows for seamless management of artists, albums, tracks, playlists and testimonials. Staff members with appropriate permissions can add, update, or delete these resources.

### User Roles & Permissions:

- Superuser: The superuser has full administrative privileges, including complete access to manage all aspects of the application. This includes adding, editing, and deleting artists, albums, tracks, playlists, testimonials, as well as managing user profiles. The superuser can perform any action within the Django admin interface.

- Staff: Staff members have limited administrative access. They can manage artists, albums, tracks, playlists and testimonials, including adding new content, editing existing resources, and deleting them. However, staff members cannot edit user profiles. They have view-only access to user profiles, ensuring that the privacy and security of user data are maintained.

- Regular Users: Regular users have the ability to explore and interact with music data, such as browsing tracks, albums, and artists fetched from the Spotify API. They can create and manage their own playlists but are restricted from modifying any of the music data or user profiles.

### Technology Stack:

- Backend: Django

- Frontend: HTML, CSS

- API Integration: Spotify Web API

- Database: PostgreSQL

- Authentication: Django’s built-in authentication system for user login and profile management.


## Getting Started

Follow these steps to set up and run the application on your local machine.

### Prerequisites

- Python 3.9+
- PostgreSQL 12+
- pip (Python package manager)

---

## Installation

1. Clone the repository:
```
git clone https://github.com/zlatinasadovska/softuni-final-project.git
```

2. Create the virtual environment (if not created):
```
python -m venv venv
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Spotify Credentials:

- For easier testing of the Spotify functionality, the required Spotify API credentials (CLIENT_ID and CLIENT_SECRET) are already included in the project files.

- These credentials are located in the Echo/spotify/spotify_config.py file. No additional setup is required.

5. Set Up the Database:

- Apply migrations to initialize the database:
```
python manage.py migrate
```

5. Optionally, create a superuser to access the Django admin panel:
```
python manage.py createsuperuser
```

6. Run the Development Server:
```
python manage.py runserver
```

Access the app at http://127.0.0.1:8000.
