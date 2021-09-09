# Notebook: an Instagram-like application.

<img src="https://raw.githubusercontent.com/RobinsonLuzo/Notebook/master/img/Profile_screenshot.JPG" alt="Profile Screenshot" width="850"/>

Work in progress personal project. Currently enabled to:

- Allow for new user creation. Edit profile details, including profile photo.

- Login and Logout for users from Navabr (under "Settings")

- Home page of photos from other users a given user is following.

- Follow/Unfollow other users. 

- Post new photos.

- See all photos associate with a given hashtag.

- Liking, Favoriting and Commenting on other users posts is now available!

<img src="https://raw.githubusercontent.com/RobinsonLuzo/Notebook/master/img/comment_screenshot.JPG" alt="Comment Screenshot" width="850"/>

- Direct Messaging. You can now message other profiles. Searching for profiles to messages is possible too - through the "New Message" button.

- Notifications. You now get notifications when another user has liked or commented on a post you made, followed you or messaged you.

<img src="https://raw.githubusercontent.com/RobinsonLuzo/Notebook/master/img/notifications_screenshot.JPG" alt="DM Screenshot" width="850"/>



**Additonal Functionality to come:**

- Video and Stories *a-la* Instagram will likely follow after these, but will require mre library imports.

**Note:** Actions involving posting photos etc require a user to be logged in to work correctly. Log in first or create a new profile if starting the app for the first time. This can be done at: "user/login" and selecting the option to Create a new profile.

## Bugs/TODO:

29.07.21 - User profile creation will create a profile, but redirect fails specifying path "post/user/login". Not immediate concern, but to be fixed.

22.08.2021 - User profile photo displays at incorrect scale when a larger photo is used. Not immediate, but possibly revise format profile phots are saved in to a certain size to prevent in future - Bulma only allows for rescaling from photos up to 4x from stated size in html.