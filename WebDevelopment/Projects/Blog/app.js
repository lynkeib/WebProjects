var express = require("express"),
	app = express(),
	bodyParser = require("body-parser"),
	mongoose = require("mongoose")

// APP CONFIG
app.use(express.static("public"))
app.use(bodyParser.urlencoded({extended:true}))

// Schema
// - title
// - image
// - body
// - created

mongoose.connect("mongodb://localhost:27017/restful_blog_app", { useNewUrlParser: true , useUnifiedTopology:true})

// MONGOOSE MODEL CONFIG
var blogSchema = new mongoose.Schema({
	title: String,
	image: String,
	body: String,
	create: {type: Date, default: Date.now}
})
var Blog = mongoose.model("Blog", blogSchema)

// Blog.create({"title":"lalala", "image":"https://images.unsplash.com/photo-1494545261862-dadfb7e1c13d?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=500&q=60", "body":"This is a blog post"})

// RESTFUL ROUTES

app.get("/", function(req, res){
	res.redirect("/blogs")
})

// INDEX ROUTE
app.get("/blogs", function(req, res){
	Blog.find({}, function(err, blogs){
		if(err){
			console.log("Error")
		}else{
			res.render("index.ejs", params={"blogs":blogs})
		}
	})
})

// NEW TOUTE
app.get("/blogs/new", function(req, res){
	res.render("new.ejs")
})

// CREATE ROUTE
app.post("/blogs", function(req, res){
	// create
	Blog.create(req.body.blog, function(err, newblog){
		if(err){
			res.render("new.ejs")
		}else{
			// redirect
			res.redirect("/blogs")
		}
	})
})

// SHOW ROUTE
app.get("/blogs/:id", function(req, res){
	Blog.findById(req.params.id, function(err, foundBlog){
		if(err){
			res.redirect("/blogs")
		}else{
			res.render("show.ejs", params={"blog":foundBlog})
		}
	})
})


app.listen(PORT=3000, function(){
	console.log("Server is running")
})


