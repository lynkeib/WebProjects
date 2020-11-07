## Tech Stack
- Python
- Django

## API Intro
- Create new profile  
POST /api/profile 
    - Handle registration of new user
    - Validate profile data
- Listing existing profiles  
GET /api/profile 
    - Search for profiles 
    - Show email and name
- View specific profiles  
GET /api/profile/<profile_id>
    - Profile ID
- Update profile of logged in user  
PUT / PATCH /api/profile/<profile_id>
    - Change name, email and password
- Delete profile  
DELETE /api/profile/<profile_id>