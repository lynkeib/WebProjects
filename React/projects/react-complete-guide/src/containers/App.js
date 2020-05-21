import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import Persons from '../components/Persons/Persons';
// import Radium, {StyleRoot} from 'radium';

import Cockpit from '../components/Cockpit/Cockpit'



class App extends Component {

  state = {
    persons: [
      { id: '1', name: "Max", age: 12 },
      { id: '2', name: "1234", age: 123 },
      { id: '3', name: "12345", age: 345 }
    ],
    hidden: false
  }

  deletePersonHandler = (index) => {
    // const persons = this.state.persons.slice();
    const persons = [...this.state.persons];
    persons.splice(index, 1);
    this.setState({ persons: persons });
  }

  togglePersonHandler = () => {
    let doesShow = this.state.hidden;
    this.setState({ hidden: !doesShow });
  }

  nameChangeHandler = (e, id) => {
    const personIndex = this.state.persons.findIndex(p => p.id === id);
    const person = { ...this.state.persons[personIndex] };
    person.name = e.target.value;
    const persons = [...this.state.persons];
    persons[personIndex] = person;
    this.setState({ persons: persons });
  }

  render() {
    // const style = {
    //   backgroundColor: 'green',
    //   color:'white',
    //   font: 'inherit',
    //   border: '1px solid blue',
    //   padding: '8px',
    //   cursor: 'pointer',
    //   ':hover':{
    //     backgroundColor:'lightgreen',
    //     color:'black'
    //   }
    // };

    let persons = null;
    if (this.state.hidden) {
      persons = (
        <div>
          <Persons 
          persons={this.state.persons} 
          clicked= {this.deletePersonHandler}
          changed={this.nameChangeHandler}
          />    
        </div>
      );
      // style.backgroundColor = 'red';
      // style[':hover']={
      //   backgroundColor:'lightred',
      //   color:'black'
      // }
    }
    return (
      <div className="App">
        <Cockpit 
        hidden = {this.state.hidden}
        persons = {this.state.persons}
        clicked={this.togglePersonHandler}
        />
        {persons}
      </div>
    );
  }
}

export default App;
