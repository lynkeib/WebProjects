var express = require("express"),
	app = express(),
	bodyParser = require("body-parser"),
	mongoose = require("mongoose");


mongoose.connect("mongodb://localhost：27017/yelp_camp", {useNewUrlParser:true, useUnifiedTopology: true});
app.use(bodyParser.urlencoded({extended:true}));

// SCHEMA SETUP
var campgroundSchema = new mongoose.Schema({
	name:String,
	image:String,
	description:String
})

var Campground = mongoose.model("Campground", campgroundSchema)

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
			res.render("index.ejs", params={"campgrounds":allCampgrounds})
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
	res.render("new.ejs")
})

// SHOW - 
app.get("/campgrounds/:id", function(req, res){
	// res.send("This will be a SHOW page")
	Campground.findById(req.params.id, function(err, foundCampground){
		if(err){
			console.log(err)
		}else{
			res.render("show.ejs", {"campground":foundCampground})
		}
	})
})


app.listen(PORT=3000, function(){
	console.log("YalpCamp Server started")
})