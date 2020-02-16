var express = require("express")
var router = express.Router()
var passport = require('passport')
var User = require("../models/user.js")


// adding landing page
router.get("/", function(req, res){
	res.render("landing.ejs")
})


// =============
// Auth Route
// =============

// Show the reg form
router.get("/register", function(req, res){
	res.render("register.ejs")
})

// handle sign up logic
router.post("/register", function(req, res){
	User.register(new User({"username":req.body.username}), req.body.password, function(err, user){
		if(err){
			console.log(err)
			return res.render("register.ejs")
		}
		passport.authenticate("local")(req, res, function(){
			res.redirect("/campgrounds")
		})
	})
})

// show login form
router.get("/login", function(req, res){
	res.render('login.ejs')
})

// handle login logic
router.post('/login', passport.authenticate("local", {
		successRedirect:"/campgrounds",
		failureRedirect:"/login"
	}), function(req, res){
})

// add logout route
router.get("/logout", function(req, res){
	req.logout()
	res.redirect("/campgrounds")
})

function isLoggedIn(req, res, next){
	if(req.isAuthenticated()){
		return next()
	}
	res.redirect("/login")
}

module.exports = router

