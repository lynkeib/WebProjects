## Tech Stack
- Python
- Django

## API Intro
### Profile
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

### Feed 
- Create new feed  
  POST /api/feed
- Listing all feed  
  GET /api/feed
- View specific feed  
  GET /api/feed/<feed_id>
- Update feed  
  PUT / PATCH /api/feed/<feed_id>
- Delete feed  
  DELETE /api/feed/<feed_id>