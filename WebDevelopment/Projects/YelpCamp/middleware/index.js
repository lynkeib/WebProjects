// all the middlewares go here
var Campground = require('../models/campground.js');
var Comment = require('../models/comment.js');

var middlewareObj = {};

middlewareObj['isLoggedIn'] = function isLoggedIn(req, res, next) {
	if (req.isAuthenticated()) {
		return next();
	}
	req.flash("error", "Please Login First");
	res.redirect('/login');
};

middlewareObj['checkCampgroundOwnership'] = function checkCampgroundOwnership(req, res, next) {
	// is user logged in?
	if (req.isAuthenticated()) {
		Campground.findById(req.params.id, function(err, foundCampground) {
			if (err || !foundCampground) {
				req.flash("error", "Campground not found");
				res.redirect('back');
			} else {
				// does user own the campground
				if (foundCampground['author']['id'].equals(req.user._id)) {
					next();
				} else {
					req.flash("error", "You don't have permission to do that");
					res.redirect('back');
				}
			}
		});
		// otherwise
	} else {
		req.flash("error", "Please Login First");
		res.redirect('back');
	}
};

middlewareObj['checkCommentOwnership'] = function checkCommentOwnership(req, res, next) {
	// is user logged in?
	if (req.isAuthenticated()) {
		Comment.findById(req.params.comment_id, function(err, foundComment) {
			if (err || !foundComment) {
				req.flash("error", "Comment not found");
				res.redirect('back');
			} else {
				// does user own the campground
				if (foundComment['author']['id'].equals(req.user._id)) {
					next();
				} else {
					req.flash("error", "You don't have permission to do that")
					res.redirect('back');
				}
			}
		});
		// otherwise
	} else {
		req.flash("error", "Please Login First")
		res.redirect('back');
	}
};

module.exports = middlewareObj;