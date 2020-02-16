var express = require("express")
var router = express.Router({mergeParams:true})

var Campground = require("../models/campground.js")
var Comment = require("../models/comment.js")

// ==================
// Comments ROUTES
// ==================

// NEW
router.get("/new", isLoggedIn, function(req, res){
	Campground.findById(req.params.id, function(err, foundCampground){
		if(err){
			console.log(err)
		}else{
			res.render("comments/new.ejs", params={"campgrounds":foundCampground})
		}
	})
})

// CREATE
router.post("/", isLoggedIn, function(req, res){
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
					comment.author.id = req.user["_id"]
					comment.author.username = req.user["username"]
					//save comment
					comment.save()
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

//EDIT
router.get("/:comment_id/edit", checkCommentOwnership, function(req, res){
	Comment.findById(req.params.comment_id, function(err, foundComment){
		if(err){
			res.redirect("back")
		}else{
			console.log(req.params.id)
			res.render("comments/edit.ejs", params={"campground_id":req.params.id, "comment":foundComment})
		}
	})
})

// UPDATE
router.put("/:comment_id", checkCommentOwnership, function(req, res){
	Comment.findByIdAndUpdate(req.params.comment_id, req.body.comment, function(err, updatedComment){
		if(err){
			res.redirect("back")
		}else{
			res.redirect("/campgrounds/" + req.params.id)
		}
	})
})

// DESTROY
router.delete("/:comment_id", checkCommentOwnership, function(req, res){
	Comment.findByIdAndRemove(req.params.comment_id, function(err){
		if(err){
			res.redirect("back")
		}else{
			res.redirect("/campgrounds/" + req.params.id)
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

function checkCommentOwnership(req, res, next){
	// is user logged in?
	if(req.isAuthenticated()){
		Comment.findById(req.params.comment_id, function(err, foundComment){
		if(err){
			res.redirect("back")
		}else{
			// does user own the campground
			if(foundComment["author"]["id"].equals(req.user._id)){
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