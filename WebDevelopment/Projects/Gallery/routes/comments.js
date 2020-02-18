var express = require('express');
var router = express.Router({ mergeParams: true });
var middlewareObj = require('../middleware/index.js');

var Campground = require('../models/campground.js');
var Comment = require('../models/comment.js');

// ==================
// Comments ROUTES
// ==================

// NEW
router.get('/new', middlewareObj.isLoggedIn, function(req, res) {
	Campground.findById(req.params.id, function(err, foundCampground) {
		if (err) {
			console.log(err);
		} else {
			res.render('comments/new.ejs', (params = { campgrounds: foundCampground }));
		}
	});
});

// CREATE
router.post('/', middlewareObj.isLoggedIn, function(req, res) {
	// lookup campground using ID
	Campground.findById(req.params.id, function(err, campground) {
		if (err) {
			console.log(err);
			res.redirect('/campgrounds');
		} else {
			// Create new comment
			Comment.create(req.body.comment, function(err, comment) {
				if (err) {
					console.log(err);
				} else {
					comment.author.id = req.user['_id'];
					comment.author.username = req.user['username'];
					//save comment
					comment.save();
					// connect new comment to campground
					campground.comments.push(comment);
					campground.save();
					// redirect to show page
					req.flash('success', 'Successfully added a comment');
					res.redirect('/campgrounds/' + campground['_id']);
				}
			});
		}
	});
});

//EDIT
router.get('/:comment_id/edit', middlewareObj.checkCommentOwnership, function(req, res) {
	Campground.fundById(req.params.id, function(err, foundCampground) {
		if (err || !foundCampground) {
			req.flash('error', 'No campground found');
			res.redirect('back');
		} else {
			Comment.findById(req.params.comment_id, function(err, foundComment) {
				if (err) {
					res.redirect('back');
				} else {
					res.render(
						'comments/edit.ejs',
						(params = { campground_id: req.params.id, comment: foundComment })
					);
				}
			});
		}
	});
});

// UPDATE
router.put('/:comment_id', middlewareObj.checkCommentOwnership, function(req, res) {
	Comment.findByIdAndUpdate(req.params.comment_id, req.body.comment, function(
		err,
		updatedComment
	) {
		if (err) {
			res.redirect('back');
		} else {
			res.redirect('/campgrounds/' + req.params.id);
		}
	});
});

// DESTROY
router.delete('/:comment_id', middlewareObj.checkCommentOwnership, function(req, res) {
	Comment.findByIdAndRemove(req.params.comment_id, function(err) {
		if (err) {
			res.redirect('back');
		} else {
			req.flash('success', 'Comment deleted');
			res.redirect('/campgrounds/' + req.params.id);
		}
	});
});

module.exports = router;