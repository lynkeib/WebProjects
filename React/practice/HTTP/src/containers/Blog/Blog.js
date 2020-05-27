import React, { Component } from 'react';
import axios from 'axios';

import Post from '../../components/Post/Post';
import FullPost from '../../components/FullPost/FullPost';
import NewPost from '../../components/NewPost/NewPost';
import './Blog.css';

class Blog extends Component {

    state = {
        posts: [],
        selectedPostId: null
    }

    componentDidMount() {
        let posts = null;
        axios.get('/posts')
            .then(response => {
                const posts = response.data.slice(0, 4);
                const updatedPosts = posts.map(post => ({ ...post, author: 'LALALA' }));
                this.setState({ posts: updatedPosts });
                // posts = response;
            });
    }

    postSelectedHandler = id => {
        this.setState({ selectedPostId: id });
    }

    render() {

        const posts = this.state.posts.map(
            post => <Post
                title={post.title}
                key={post.id}
                author={post.author}
                clicked={this.postSelectedHandler.bind(this, post.id)} />
        );

        return (
            <div className='Blog'>
                <header>
                    <nav>
                        <ul>
                            <li><a href='/'>Home</a></li>
                            <li><a href='/'>New Post</a></li>
                        </ul>
                    </nav>
                </header>
                <section className="Posts">
                    {posts}
                </section>
                <section>
                    <FullPost id={this.state.selectedPostId} />
                </section>
                <section>
                    <NewPost />
                </section>
            </div>
        );
    }
}

export default Blog;