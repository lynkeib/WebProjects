var express = require("express"),
	app = express(),
	bodyParser = require("body-parser"),
	mongoose = require("mongoose"),
	Campground = require("./models/campground.js"),
	Comment = require("./models/comment.js"),
	seedDB = require("./seed.js");

seedDB()
mongoose.connect("mongodb://localhost：27017/yelp_camp", {useNewUrlParser:true, useUnifiedTopology: true});
app.use(bodyParser.urlencoded({extended:true}));
app.use(express.static(__dirname + "/public"))

// adding landing page
app.get("/", function(req, res){
	res.render("landing.ejs")
})

// INDEX - show all campgrounds
app.get("/campgrounds", function(req, res){
	// Get all campground from mongodb
	Campground.find({}, function(err, allCampgrounds){
		if(err){
			console.log(err)
		}else{
			res.render("campgrounds/index.ejs", params={"campgrounds":allCampgrounds})
		}
	})
})

// CREATE - add new campground to db
app.post("/campgrounds", function(req, res){
	// get data from form, and add to campground array
	var name = req.body.name
	var image = req.body.image
	var desc = req.body.desc
	// Create a new campground into the db
	Campground.create({"name":name, "image":image, "description":desc}, function(err, newCampground){
		if(err){
			cnosole.log(err)
		}else{
			// redirect back to campground page
			res.redirect("/campgrounds")
		}
	})
})

// NEW - show form to create new campground
app.get("/campgrounds/new", function(req, res){
	res.render("campgrounds/new.ejs")
})

// SHOW - 
app.get("/campgrounds/:id", function(req, res){
	// res.send("This will be a SHOW page")
	Campground.findById(req.params.id).populate("comments").exec( function(err, foundCampground){
		if(err){
			console.log(err)
		}else{
			res.render("campgrounds/show.ejs", {"campground":foundCampground})
		}
	})
})

// ==================
// Comments ROUTES
// ==================

// NEW
app.get("/campgrounds/:id/comments/new", function(req, res){
	Campground.findById(req.params.id, function(err, foundCampground){
		if(err){
			console.log(err)
		}else{
			res.render("comments/new.ejs", params={"campgrounds":foundCampground})
		}
	})
})

// CREATE
app.post("/campgrounds/:id/comments", function(req, res){
	// lookup campground using ID
	Campground.findById(req.params.id, function(err, campground){
		if(err){
			console.log(err)
			res.redirect("/campgrounds")
		}else{
			// Create new comment
			Comment.create(req.body.comment, function(err, comment){
				if(err){
					console.log(err)
				}else{
					// connect new comment to campground
					campground.comments.push(comment)
					campground.save()
					// redirect to show page
					res.redirect("/campgrounds/" + campground["_id"])
				}
			})
		}
	})
})


app.listen(PORT=3000, function(){
	console.log("YalpCamp Server started")
})