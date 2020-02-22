Useful websites and key words:

+ Frontend:
  + [MDN](https://mdn.dev): Reference source
  + [Events References](https://developer.mozilla.org/en-US/docs/Web/Events): Event Reference
  + [Bootstrap 3 & 4](https://getbootstrap.com/docs/3.3/): The most popular CSS Framework
  + [Semantic UI](https://semantic-ui.com): Another popular CSS Framework
  + [Google Fonts](https://fonts.google.com): Fonts gallery
  + [CodePen](https://codepen.io): Styles gallery
  + [Unsplash](https://unsplash.com): High-resolution photos collection
  + [Font Awesome](https://fontawesome.com): Icon gallery
  + [jQuery](https://jquery.com): A JavaScript library, API Doc contains all the methods
  + [UIgradients](https://uigradients.com/#Twitch): A website provides beautiful gradient colors
  + [Loupe](http://latentflip.com/loupe/?code=JC5vbignYnV0dG9uJywgJ2NsaWNrJywgZnVuY3Rpb24gb25DbGljaygpIHsKICAgIHNldFRpbWVvdXQoZnVuY3Rpb24gdGltZXIoKSB7CiAgICAgICAgY29uc29sZS5sb2coJ1lvdSBjbGlja2VkIHRoZSBidXR0b24hJyk7ICAgIAogICAgfSwgMjAwMCk7Cn0pOwoKY29uc29sZS5sb2coIkhpISIpOwoKc2V0VGltZW91dChmdW5jdGlvbiB0aW1lb3V0KCkgewogICAgY29uc29sZS5sb2coIkNsaWNrIHRoZSBidXR0b24hIik7Cn0sIDUwMDApOwoKY29uc29sZS5sb2coIldlbGNvbWUgdG8gbG91cGUuIik7!!!PGJ1dHRvbj5DbGljayBtZSE8L2J1dHRvbj4%3D): A simulation website visualizing async

+ Backend:
  + [StackShare](https://stackshare.io): A website sharing different stacks using in different companies
  + [Goorm](https://ide.goorm.io): A Cloud IDE
  + Node.js Packages
    + npm (package management)
    + express
    + ejs
    + body-parser
    + mongoose
    + method-override (to achieve PUT method for forms in html)
    + express-sanitizer
    + passport

+ Terms
  + MEAN Stack: MongoDB, Express, Angular, Node.js
  + CRUD: CREATE, READ, UPDATE, DESTROY
  + REST: REpresentational State Transfer, a mapping between HTTP routes and CRUD
  
      | Name   | PATH            | HTTP Verb | Mongoose Method          |
      |--------|-----------------|-----------|--------------------------|
      | INDEX  | /index          | GET       | item.find()              |
      | NEW    | /index/new      | GET       | N/A                      |
      | CREATE | /index          | POST      | item.create()            |
      | SHOW   | /index/:id      | GET       | item.findById()          |
      | EDIT   | /index/:id/edit | GET       | item.findById()          |
      | UPDATE | /index/:id      | PUT       | item.findByIdAndUpdate() |
      | DELETE | /index/:id      | DELETE    | item.findByIdAndRemove() |
