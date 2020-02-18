require("dotenv").config()

var express = require("express"),
	app = express(),
	bodyParser = require("body-parser"),
	mongoose = require("mongoose"),
	Campground = require("./models/campground.js"),
	Comment = require("./models/comment.js"),
	seedDB = require("./seed.js"),
	passport = require("passport"),
	LocalStrategy = require("passport-local"),
	User = require("./models/user.js"),
	methodOVerride = require("method-override"),
	flash = require("connect-flash");

// link to outter files for routes management
var commentRoutes = require("./routes/comments.js"),
	campgroundRoutes = require("./routes/campgrounds.js"),
	indexRoutes = require("./routes/index.js")

// seedDB()
mongoose.connect("mongodb+srv://yelpcamp:"+ process.env.DBPassword +"@cluster0-gke6f.mongodb.net/test?retryWrites=true&w=majority", {useNewUrlParser:true, useUnifiedTopology: true, useCreateIndex: true}, function(err){
	if(err){
		console.log("Cannot connect")
	}else{
		console.log("Connected")
	}
})
app.use(bodyParser.urlencoded({extended:true}))
app.use(express.static(__dirname + "/public"))
app.use(methodOVerride("_method"))
app.use(flash())
app.locals.moment = require("moment")


// PASSPORT CONFIGURATION
app.use(require("express-session")({
	secret: "lalala",
	resave: false,
	saveUninitialized:false
}))
app.use(passport.initialize())
app.use(passport.session())
passport.use(new LocalStrategy(User.authenticate()))
passport.serializeUser(User.serializeUser())
passport.deserializeUser(User.deserializeUser())

// add user arguments for each url
app.use(function(req, res, next){
	res.locals.currentUser = req.user;
	res.locals.error = req.flash("error");
	res.locals.success = req.flash("success");
	next()
})

// ROUTEs from outter files
app.use("/", indexRoutes)
app.use("/campgrounds", campgroundRoutes)
app.use("/campgrounds/:id/comments", commentRoutes)

// PORT CONFIG
app.listen(PORT=process.env.PORT, function(){
	console.log("YalpCamp Server started")
})