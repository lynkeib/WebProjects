var NodeGeocoder = require('node-geocoder');

var options = {
	provider: 'google',
	httpAdapter: 'https',
	apiKey: process.env.GEOCODER_API_KEY,
	formatter: null
};

var geocoder = NodeGeocoder(options);

var express = require('express');
var router = express.Router();
var middlewareObj = require('../middleware/index.js');

var Campground = require('../models/campground.js');

// INDEX - show all campgrounds
router.get('/', function(req, res) {
	// Get all campground from mongodb
	Campground.find({}, function(err, allCampgrounds) {
		if (err) {
			console.log(err);
		} else {
			res.render('campgrounds/index.ejs', (params = { campgrounds: allCampgrounds }));
		}
	});
});

// CREATE - add new campground to db
router.post('/', middlewareObj.isLoggedIn, function(req, res) {
	// get data from form, and add to campground array
	var name = req.body.name;
	var price = req.body.price;
	var image = req.body.image;
	var desc = req.body.desc;
	var author = {
		id: req.user._id,
		username: req.user.username
	};
	geocoder.geocode(req.body.location, function(err, data) {
		if (err || data.length === 'ZERO_RESULTS') {
			req.flash('error', 'Invalid address');
			res.redirect('back');
		} else {
			var lat = data[0].latitude;
			var lng = data[0].longitude;
			var location = data[0].formattedAddress;
			var newCampground = {
				name: name,
				image: image,
				description: desc,
				author: author,
				price: price,
				lat: lat,
				lng: lng,
				location: location
			};
			Campground.create(newCampground, function(err, newlyCampground) {
				if (err) {
					cnosole.log(err);
				} else {
					// redirect back to campground page
					res.redirect('/campgrounds');
				}
			});
		}
	});
	// Create a new campground into the db
});

// NEW - show form to create new campground
router.get('/new', middlewareObj.isLoggedIn, function(req, res) {
	res.render('campgrounds/new.ejs');
});

// SHOW -
router.get('/:id', function(req, res) {
	// res.send("This will be a SHOW page")
	Campground.findById(req.params.id)
		.populate('comments')
		.exec(function(err, foundCampground) {
			if (err || !foundCampground) {
				req.flash('error', 'Campground not found');
				res.redirect('back');
			} else {
				res.render('campgrounds/show.ejs', { campground: foundCampground });
			}
		});
});

// EDIT
router.get('/:id/edit', middlewareObj.checkCampgroundOwnership, function(req, res) {
	Campground.findById(req.params.id, function(err, foundCampground) {
		res.render('campgrounds/edit.ejs', { campground: foundCampground });
	});
});

// UPDATE
router.put('/:id', middlewareObj.checkCampgroundOwnership, function(req, res) {
	// find and update the campground
	Campground.findByIdAndUpdate(req.params.id, req.body.campground, function(err, updatedCamp) {
		if (err) {
			res.redirect('/campgrounds');
		} else {
			res.redirect('/campgrounds/' + req.params.id);
		}
	});

	// redict to the show page
});

// DELETE
router.delete('/:id', middlewareObj.checkCampgroundOwnership, function(req, res) {
	Campground.findByIdAndRemove(req.params.id, function(err) {
		if (err) {
			res.redirect('/campgrounds');
		} else {
			res.redirect('/campgrounds');
		}
	});
});

module.exports = router;