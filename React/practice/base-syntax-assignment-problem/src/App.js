import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import UserInput from './UserInput/UserInput';
import UserOutput from './UserOutput/UserOutput';

class App extends Component {

  state = {
    userName: 'USR'
  }

  userNameHandler = (e) => {
    this.setState({ userName: e.target.value });
  }

  render() {
    return (
      <div className='App'>
        <UserInput onChange={this.userNameHandler} username={this.state.userName} />
        <UserOutput userName={this.state.userName} />
      </div>
    );
  }
}

export default App;
