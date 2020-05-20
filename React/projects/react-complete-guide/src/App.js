import React, { Component } from 'react';
// import logo from './logo.svg';
import './App.css';
import Person from './Person/Person';
import person from './Person/Person';

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
    const person = {...this.state.persons[personIndex]};
    person.name = e.target.value;
    const persons = [...this.state.persons];
    persons[personIndex] = person;
    this.setState({persons:persons});
  }

  render() {
    const style = {
      backgroundColor: 'white',
      font: 'inherit',
      border: '1px solid blue',
      padding: '8px',
      cursor: 'pointer'
    };

    let persons = null;
    if (this.state.hidden) {
      persons = (
        <div>
          {this.state.persons.map((person, index) => {
            return <Person
              name={person.name}
              age={person.age}
              key={person.id}
              click={this.deletePersonHandler.bind(this, index)}
              changed={(event) => this.nameChangeHandler(event, person.id)}>
            </Person>
          })}
        </div>
      );
    }

    return (
      <div className="App">
        <h1>Test</h1>
        <button onClick={this.togglePersonHandler} style={style}>Switch name</button>
        {persons}
      </div>
    );
  }

}

export default App;
