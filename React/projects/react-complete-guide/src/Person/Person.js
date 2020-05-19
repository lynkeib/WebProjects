import React from 'react';
import './Person.css';

const person = (props) => {
    return (
        <div className="Person">
            <p>I'm a {props.name} age {props.age}</p>
            <p>{props.children}</p>
        </div>
    )
}

export default person;