import React from 'react';
import './UserInput.css';

const userInput = (props) => {
    return (<input className='input' type='text' onChange={props.onChange} value={props.username}/>)
}

export default userInput;