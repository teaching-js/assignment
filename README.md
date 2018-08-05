# COMP2041 JavaScript Assignment (2041stagram)

## Quickstart

If you're using NPM the following simple scripts are avalable to you to help
your development.

```bash
# run the development server on port 8080
npm run dev

# run the linter to check your js
npm run lint
```

In addition we've provided a basic project scaffold for you to build from.
You can use everything we've given you, although there's no requirement to use anything.
```bash
# scaffold
data
  - feed.json  # A sample feed data object
  - me.json    # A sample user/profile object
  - post.json  # A sample post object

src
  - main.js   # The main entrypoint for your app
  - api.js    # maybe for your api logic
  - helper.js # some helper functions

styles
  - main.css  # where your css goes (add more stylesheets as you please)

```

## Introduction

JavaScript is used increasingly to provide a native-like application experience in the web. One
major avenue of this has been in the use of Single Page Applications or SPAs. SPAs
are generated, rendered, and updated using JavaScript. Because SPAs don't require a user
to navigate away from a page to do anything, they retain a degree of user and application state.

There are millions of websites that utilise SPAs in part of, or all of their web applications.

The assignment intends to teach students to build a simple SPA which can fetch dynamic data from a HTTP/S API.
Your task will be to provide an implemention of a SPA that can provide a number of key features.

Some of the skills/concepts this assignment aims to test (and build upon):

* Simple event handling (buttons)
* Advanced Mouse Events (Swipe)
* Fetching data from an API
* Infinite scroll
* CSS Animations
* Web Workers
* Push Notifications (Polling)
* Offline Support
* Routing (URL fragment based routing)

## API
We can build API documentation using [Swagger](https://swagger.io/) or API Blueprint.
A simple express JS API server can be built that is provided to students to allow them to develop offline. It could also be hosted somewhere to ease development when online?

TODO: Someone will need to build a API server to support all of this client side functionality.

The following specification is a WIP and only includes some endpoints.

> POST `/login`

**Request**
```json
{
  "username": "string",
  "password": "string",
}
```

**Response**
`200` On successful login, sets a cookie with a session token
```json
{
  "error": false,
  "errorMsg": null
}
```

`403` for invalid credentials
```json
{
  "error": true,
  "errorMsg": "Invalid Credentials"
}  
```

> POST `/signup`

**Request**
```json
{
  "email": "string",
  "username": "string",
  "password": "string",
}
```
**Response**
`200` On successful signup, sets a cookie with a session token
```json
{
  "error": false,
  "errorMsg": null
}
```

`403` for existent username
```json
{
  "error": true,
  "errorMsg": "Username Already In Use"
}  
```

> PUT `/post/like?postId=13`

**Request**
```
postId : Id of the post the current logged in user wishes to like
```

**Response**
`200` On successful like
```json
{
  "error": false,
  "errorMsg": null
}
```

`403` for Non Existent post or user not logged in
```json
{
  "error": true,
  "errorMsg": "You Are Not Logged In | Invalid Post Id"
}  
```


> PUT `/post/comment`

**Request**

```json
{
  "postId": "integer",
  "text": "string"
}
```

**Response**
`200` On successful comment
```json
{
  "error": false,
  "errorMsg": ""
}
```

`403` for user is not logged in or invalid post id
```json
{
  "error": true,
  "errorMsg": "You Are Not Logged In | Invalid Post Id"
}  
```

> POST `/post/new`

**Request**
```json
{
  "description_text": "string",
  "src": "string"
}
```

_TODO: Decide if we are doing a file upload or just base64 encode the image_

**Response**
`200` On successful Post
```json
{
  "error": false,
  "errorMsg": ""
}
```

`403` for user is not logged in or image/description invalid
```json
{
  "error": true,
  "errorMsg": "You Are Not Logged In | Invalid Description | Invalid Image"
}  
```


> GET `/user/feed?p=17`

**Request**

```
p : a number specifying where to begin fetching posts,
    the server will response with 10 posts from the feed in the range
    [10*p,10*p+10). If not specified p is set to 0
```

**Response**
`200` On successful fetch
```json
[
  {
      "id": 1,
      "meta": {
          "author": "Nina",
          "description_text": "My lounge",
          "published": "Sat Aug 04 2018 20:19:12 GMT+1000 (Australian Eastern Standard Time)",
          "likes": []
      },
      "thumbnail": "man-small.jpg",
      "src": "man.jpg"
  },
  "..."
]
```

`403` for invalid position token or non logged in user
```json
{
  "error": true,
  "errorMsg": "You Are Not Logged In | Invalid Position Number"
}  
```

> PUT `/user/follow?username=barry`

**Request**

```
username: username of the user the logged in user wishes to follow
```

**Response**
`200` On successful Follow
```json
{
  "error": false,
  "errorMsg": null
}
```

`403` for invalid username or user is not logged in
```json
{
  "error": true,
  "errorMsg": "You Are Not Logged In | Invalid Username"
}  
```


> PUT `/user/unfollow?username=barry`

**Request**

```
username: username of the user the logged in user wishes to unfollow
```

**Response**
`200` On successful UnFollow
```json
{
  "error": false,
  "errorMsg": null
}
```

`403` for invalid username or user is not logged in
```json
{
  "error": true,
  "errorMsg": "You Are Not Logged In | Invalid Username"
}  
```

> GET `/user/info`

**Response**
`200` On successful fetch
```json
{
  "username": "baz",
  "name": "Barry",
  "id"  : 1,
  "posts": [1]
}
```

`403` for user is not logged in
```json
{
  "error": true,
  "errorMsg": "You Are Not Logged In"
}  
```

> PUT `/user/update`

**Request**

```json
{
  "name": "String",
  "password": "String",
  "..."
}
```

**Response**
`200` On successful update
```json
{
  "error": false,
  "errorMsg": ""
}
```

`403` for user is not logged in
```json
{
  "error": true,
  "errorMsg": "You Are Not Logged In"
}  
```


## Milestones
Level 0 focuses on the basic user interface and interaction building of the site.
There is no need to implement any integration with the backend for this level.

### Level 0

**Login**
The site presents a login form and a user can log in with pre-defined hard coded credentials.
You can use the provided users.json so you can create a internal non persistent list of users that you check against

Once logged in, the user is presented with the home page which for now can be a blank page with a simple "Not Yet implemented" message.

**Registration**
An option to register for "2041StaGram" is presented on the login page allowing the user to sign up to the service.
This for now updates the internal state object described above.

**Feed Interface**

The application should present a "feed" of user content on the home page derived from the sample feed.json provided.
The posts should be displayed in reverse chronological order (most revent posts first)

Although this is not a graphic design exercise you should produce pages with a common and somewhat distinctive look-and-feel. You may find CSS useful for this.

Each post must include
1. who the post was made by
2. when it was posted
3. the image
4. how many likes
5. the post description
6. how many comments the post has

## Level 1
Level 1 focuses on fetching data from the API.

**Login**
The site presents a login form and verifies the provided credentials with the backend (`/login`). Once logged in, the user can see the home page.

**Registration**
An option to register for "2041StaGram" is presented allowing the user to sign up to the service. The user information is POSTed to the backend to create the user in the database. (`/signup`)

**Feed Interface**
The content shown in the user's feed is sourced from the backend. (`/user/feed`)

## Level 2
Level 2 focuses on a richer UX and will require some backend interaction.

**Show likes**
Allow an option for a user to see a list of all users who have liked a post.
Possibly a modal but the design is up to you.

**Show Comments**
Allow an option for a user to see all the comments on a post.
same as above.

**Like user generated content**
A logged in user can like a post on their feed and trigger a api request `/post/like`
For now it's ok if the like doesn't show up until the page is refreshed.

**"Post" new content**
Users can upload and post new content from a modal or seperate page via `/post/new`

**Pagination**
Users can page between sets of results in the feed using the position token from `user/feed`

**Profile**
Users can see their own profile information such as username, number of posts, number of likes, profile pic.
get this information from `/user/info`

## Level 3
Level 3 focuses on more advanced features that will take time to implement and will
involve a more rigourously designed app to execute.

**Infinite Scroll**
Instead of pagination, users an infinitely scroll through results

**Comments**
Users can write comments on "posts" via `post/comment`

**Live Update**
If a user likes a post or comments on a post, the posts likes and comments should
update without requiring a page reload/refresh.

**Update Profile**
Users can update their personal profile via `/user/update` E.g:
* Update email address
* Update their profile picture
* Update password

**User Pages**
Let a user click on a user's name/picture from a post and see a page with the users name, profile pic, and other info.
The user should also see on this page all posts made by that person.
The user should be able to see their own page as well.

This can be done as a modal or as a seperate page (url fragmentation can be implemented if wished.)

**Follow**
Let a user follow/unfollow another user too add/remove their posts to their feed via `user/follow`
Add a list of everyone a user follows in their profile page.
Add just the count of followers / follows to everyones public user page

## Level 4
Push Notifications
Users can receive push notifications when a user they follow posts an image

TODO: Determine if it's feasible to write a backend that supports this. Long polling? Websockets?

### Offline Access
Users can access the "2041StaGram" at all times by using Web Workers to cache the page (and previous content) locally.

### Fragment based URL routing
Users can access different pages using URL fragments:

/#profile=me
/#feed
/#profile=janecitizen
