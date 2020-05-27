import React, { Component } from 'react';
import Post from '../../../components/Post/Post';
import axios from '../../../axios'
import './Posts.css';
import { Link } from 'react-router-dom';


class Posts extends Component {

    state = {
        posts: [],
        selectedPostId: null,
        error: false
    }

    postSelectedHandler = id => {
        this.setState({ selectedPostId: id });
    }

    componentDidMount() {
        // let posts = null;
        axios.get('/posts')
            .then(response => {
                const posts = response.data.slice(0, 4);
                const updatedPosts = posts.map(post => ({ ...post, author: 'LALALA' }));
                this.setState({ posts: updatedPosts });
                // posts = response;
            })
        // .catch(error => this.setState({ error: true }));
    }

    render() {
        let posts = <p>Something went wrong</p>
        if (!this.state.error) {
            posts = this.state.posts.map(
                post => (
                    <Link to={'/' + post.id} key={post.id}><Post
                        title={post.title}
                        author={post.author}
                        clicked={this.postSelectedHandler.bind(this, post.id)} />
                    </Link>)
            );
        }

        return (
            <section className="Posts">
                {posts}
            </section>
        )
    }
}

export default Posts;