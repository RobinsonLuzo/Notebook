# Notebook: an instagram-like app

Work in progress. Currently enabled to:

Admin at "/admin".

User login at "/user/login". Also creation of new users.

User logout at "/user/logout". To log out at present users must enter this into the bar - not enabled at navbar level yet.

Example user post at "/post".

**Note:** Actions involving posting photos etc require a user to be logged in to work correctly. Log in first or create a new profile if starting the app for the first time.

# Bugs/TODO:

29.07.21 - issue with needing to strip out whitespace from tags. When multiple tags are specified in a post it splits on commas, but does not do cleanup. This can cause a failure as a hashtag with a space will violate the unique constraint if that tag name (but without the space) already exists. Modify view for NewPost to fix.
29.07.21 - User profile creation will create a profile, but redirect fails specifying path "post/user/login". Not immediate concern, but to be fixed.