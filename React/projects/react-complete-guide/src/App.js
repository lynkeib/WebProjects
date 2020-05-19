import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import Person from './Person/Person';

class App extends Component {

  state = {
    persons : [
      {name:"Max", age:12},
      {name:"1234", age:123},
      {name:"12345", age:345}
    ]
  }

  switchNameHandler = () => {
    // this.state.persons[0].name = "KKK";
    this.setState({persons : [
      {name:"KKKK", age:12},
      {name:"1234", age:123},
      {name:"12345", age:345}
    ]});
  }

  render() {
    return (
      <div className="App">
        <h1>Test</h1>
        <button onClick={() => this.switchNameHandler()}>Switch name</button>
        <Person name={this.state.persons[0].name}/>
        <Person name={this.state.persons[1].name} age={this.state.persons[1].age}>Just test</Person>
      </div>
    );
  }

}

export default App;
