import React, { Component } from 'react';
import logo from './logo.svg';
import './App.css';
import Validation from './Validation/Validation';

class App extends Component {

  state = {
    string:"1234"
  }

  changeHandler = (event) => {
    let ele = document.getElementById('wordLength');
    const text = event.target.value;
    this.setState({string:text});
    ele.innerHTML = event.target.value.length;
  }

  deleteHandler = (event, index) => {
    const string = [...this.state.string];
    string.splice(index, 1);

    this.setState({ string: string.join("")});
  }

  map = Array.prototype.map;

  style = {
    display:'inline-block',
    padding:'16px',
    textAlign:'center',
    margin:'16px',
    border:'1px solid black'
  }

  render() {
    return (
      <div className="App">
        <input type="text" onChange={(event) => this.changeHandler(event)} value={this.state.string}></input>
        <p id='wordLength'>0</p>
        <Validation textLength = {this.state.string.length}></Validation>
        {/* {this.state.string.map((char, index) => {
          return <box style={this.style}></box>
        })} */}
        {this.map.call(this.state.string, (c, index) => {
          return <box style={this.style} onClick={(event) => this.deleteHandler(event, index)}>{c}</box>
        })}
      </div>
    );
  }
}

export default App;
