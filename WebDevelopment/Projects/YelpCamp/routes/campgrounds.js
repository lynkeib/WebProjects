var express = require("express")
var router = express.Router()

var Campground = require("../models/campground.js")


// INDEX - show all campgrounds
router.get("/", function(req, res){
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
router.post("/", isLoggedIn, function(req, res){
	// get data from form, and add to campground array
	var name = req.body.name
	var image = req.body.image
	var desc = req.body.desc
	var author = {
		id: req.user._id,
		username: req.user.username
	}
	// Create a new campground into the db
	Campground.create({"name":name, "image":image, "description":desc, "author":author}, function(err, newCampground){
		if(err){
			cnosole.log(err)
		}else{
			// redirect back to campground page
			res.redirect("/campgrounds")
		}
	})
})

// NEW - show form to create new campground
router.get("/new", isLoggedIn, function(req, res){
	res.render("campgrounds/new.ejs")
})

// SHOW - 
router.get("/:id", function(req, res){
	// res.send("This will be a SHOW page")
	Campground.findById(req.params.id).populate("comments").exec( function(err, foundCampground){
		if(err){
			console.log(err)
		}else{
			res.render("campgrounds/show.ejs", {"campground":foundCampground})
		}
	})
})

// EDIT
router.get("/:id/edit", checkCampgroundOwnership, function(req, res){
	Campground.findById(req.params.id, function(err, foundCampground){
		res.render("campgrounds/edit.ejs", {"campground":foundCampground})
	})
})

// UPDATE
router.put("/:id", checkCampgroundOwnership, function(req, res){
	// find and update the campground
	Campground.findByIdAndUpdate(req.params.id, req.body.campground, function(err, updatedCamp){
		if(err){
			res.redirect("/campgrounds")
		}else{
			res.redirect("/campgrounds/" + req.params.id)
		}
	})
	
	// redict to the show page
})

// DELETE
router.delete("/:id", checkCampgroundOwnership, function(req, res){
	Campground.findByIdAndRemove(req.params.id, function(err){
		if(err){
			res.redirect("/campgrounds")
		}else{
			res.redirect("/campgrounds")
		}
	})
})

// middleware
function isLoggedIn(req, res, next){
	if(req.isAuthenticated()){
		return next()
	}
	res.redirect("/login")
}
		
// check campground ownership
function checkCampgroundOwnership(req, res, next){
	// is user logged in?
	if(req.isAuthenticated()){
		Campground.findById(req.params.id, function(err, foundCampground){
		if(err){
			res.redirect("back")
		}else{
			// does user own the campground
			if(foundCampground["author"]["id"].equals(req.user._id)){
				next()
			}else{
				res.redirect("back")
			}
		}
	})
	// otherwise 
	}else{
		res.redirect("back")
	}
}

module.exports = router
