import React, { Component } from 'react';
import axios from 'axios';
import Posts from './Posts/Posts';
import { Route, NavLink, Switch } from 'react-router-dom';
import NewPost from './NewPost/NewPost';
import FullPost from './FullPost/FullPost';

import './Blog.css';

class Blog extends Component {

    render() {
        return (
            <div className='Blog'>
                <header>
                    <nav>
                        <ul>
                            <li><NavLink
                                to='/'
                                exact
                                activeClassName="active"
                                activeStyle={{
                                    color: '#fa923f',
                                    textDecoration: 'underline'
                                }}>Home</NavLink></li>
                            <li><NavLink to={{
                                pathname: '/new-post',
                                hash: '#submit',
                                search: '?quick-submit=true'
                            }}>New Post</NavLink></li>
                        </ul>
                    </nav>
                </header>
                {/* <Route path="/" exact={true} render={() => <Posts />}/> */}
                <Route path='/' exact component={Posts} />
                <Switch>
                    <Route path='/new-post' component={NewPost} />
                    <Route path='/:id' exact component={FullPost} />
                </Switch>
            </div>
        );
    }
}

export default Blog;