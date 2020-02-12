var express = require("express");
var app = express();
var bodyParser = require("body-parser");

app.use(bodyParser.urlencoded({extended:true}));

// adding landing page
app.get("/", function(req, res){
	res.render("landing.ejs")
})

var campgrounds = [
		{"name":"this", "image":"https://images.unsplash.com/photo-1475483768296-6163e08872a1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&q=60"},
		{"name":"jenny", "image":"https://images.unsplash.com/photo-1530541930197-ff16ac917b0e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&q=60"},
		{"name":"lalala", "image":"https://images.unsplash.com/photo-1471115853179-bb1d604434e0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&q=60"},
	{"name":"this", "image":"https://images.unsplash.com/photo-1475483768296-6163e08872a1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&q=60"},
		{"name":"jenny", "image":"https://images.unsplash.com/photo-1530541930197-ff16ac917b0e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&q=60"},
		{"name":"lalala", "image":"https://images.unsplash.com/photo-1471115853179-bb1d604434e0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&q=60"},
	{"name":"this", "image":"https://images.unsplash.com/photo-1475483768296-6163e08872a1?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&q=60"},
		{"name":"jenny", "image":"https://images.unsplash.com/photo-1530541930197-ff16ac917b0e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&q=60"},
		{"name":"lalala", "image":"https://images.unsplash.com/photo-1471115853179-bb1d604434e0?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=900&q=60"}
	]

// campgrounds
app.get("/campgrounds", function(req, res){
	res.render("campgrounds.ejs", params={"campgrounds":campgrounds})
})

// campgrounds post
app.post("/campgrounds", function(req, res){
	// get data from form, and add to campground array
	var name = req.body.name
	var image = req.body.image
	campgrounds.push({"name":name, "image":image})
	// redirect back to campground page
	res.redirect("/campgrounds")
})

app.get("/campgrounds/new", function(req, res){
	res.render("new.ejs")
})


app.listen(PORT=3000, function(){
	console.log("YalpCamp Server started")
})