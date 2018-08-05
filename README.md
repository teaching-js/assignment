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
  - users.json # A sample list of user/profile objects
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

### Errors

Any endpoint can error with a `40x` error code which signals a issue with the request.
See below

```
400 bad request (forgot a field, malformed request)
401 not authorized (not logged in)
403 forbidden (logged in, but not allowed to ser resource)
```

### End points

#### Account Creation

> POST `/login`

Logs in a user and sets a cookie with a session token

**Request**

```json
{
  "username": "string",
  "password": "string",
}
```

> POST `/signup`

Signs up a user for the service and sets a cookie with a session token

**Request**

```json
{
  "email": "string",
  "username": "string",
  "password": "string",
}
```

#### User functions

> GET `/user`

gets a user object for the current logged in user

**Response**

On successful fetch
```json
{
  "username": "baz",
  "name": "Barry",
  "id"  : 1,
  "posts": [1]
}
```

> PUT `/user`

Updates the current logged in user to match the given user object.

**Request**

```json
{
  "name": "String",
  "password": "String",
  "..."
}
```

> GET `/user/feed?p=17`

Retrieves a set of posts from the currently logged in users feed

**Request**

```
p : a number specifying where to begin fetching posts,
    the server will response with 10 posts from the feed in the range
    [10*p,10*p+10). If not specified server will respond with ALL posts
```

**Response**

On successful fetch
```json
[
  {
      "id": "Integer",
      "meta": {
          "author": "String",
          "description_text": "String",
          "published": "String",
          "likes": ["String","..."]
      },
      "thumbnail": "String",
      "src": "String"
  },
  "..."
]
```

> PUT `/user/follow?username=barry`

Adds the specified user to the list of users that the current logged in user follows

**Request**

```
username: username of the user that is to be followed
```

> PUT `/user/unfollow?username=barry`

Removed the specified user from list of users that the current logged in user follows

**Request**

```
username: username of the user the logged in user wishes to unfollow
```

#### Post Functions


> POST `/post`

Creates a new post under the current logged in user

**Request**

```json
{
  "description_text": "string",
  "src": "string"
}
```

> DELETE `/post?id=xxx`

Deletes a specified post

**Request**

```
id : the post id of the post that is to be deleted
```

> GET `/post?id=xxx`

Gets a post object by it's id

**Request**

```
id : the post id of the post that is to be fetched
```

**Response**

On successful Fetch
```json
{
    "id": "Integer",
    "meta": {
        "author": "String",
        "description_text": "String",
        "published": "String",
        "likes": ["String","..."]
    },
    "thumbnail": "String",
    "src": "String"
}
```

> PUT `/post/like?postId=13`

Registers that the current logged in user "likes" the specified posts

**Request**

```
id : Id of the post the current logged in user wishes to like
```

> POST `/post/comment?id=12`

Registers a new comment from current logged in user on the specified post

**Request**

```
id : id of the post the current logged in user wishes to comment on
```

```json
{
  "comment": "string"
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
The site presents a login form and verifies the provided credentials with the backend (`POST /login`). Once logged in, the user can see the home page.

**Registration**
An option to register for "2041StaGram" is presented allowing the user to sign up to the service. The user information is POSTed to the backend to create the user in the database. (`POST /signup`)

**Feed Interface**
The content shown in the user's feed is sourced from the backend. (`GET /user/feed`)

## Level 2
Level 2 focuses on a richer UX and will require some backend interaction.

**Show likes**
Allow an option for a user to see a list of all users who have liked a post.
Possibly a modal but the design is up to you.

**Show Comments**
Allow an option for a user to see all the comments on a post.
same as above.

**Like user generated content**
A logged in user can like a post on their feed and trigger a api request `PUT /post/like`
For now it's ok if the like doesn't show up until the page is refreshed.

**"Post" new content**
Users can upload and post new content from a modal or seperate page via `POST /post`

**Pagination**
Users can page between sets of results in the feed using the position token with `GET user/feed`

**Profile**
Users can see their own profile information such as username, number of posts, number of likes, profile pic.
get this information from `GET /user`

## Level 3
Level 3 focuses on more advanced features that will take time to implement and will
involve a more rigourously designed app to execute.

**Infinite Scroll**
Instead of pagination, users an infinitely scroll through results

**Comments**
Users can write comments on "posts" via `POST post/comment`

**Live Update**
If a user likes a post or comments on a post, the posts likes and comments should
update without requiring a page reload/refresh.

**Update Profile**
Users can update their personal profile via `PUT /user` E.g:
* Update email address
* Update their profile picture
* Update password

**User Pages**
Let a user click on a user's name/picture from a post and see a page with the users name, profile pic, and other info.
The user should also see on this page all posts made by that person.
The user should be able to see their own page as well.

This can be done as a modal or as a seperate page (url fragmentation can be implemented if wished.)

**Follow**
Let a user follow/unfollow another user too add/remove their posts to their feed via `PUT user/follow`
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
