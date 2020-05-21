import React from 'react';
import './Cockpit.css';
import styled from 'styled-components';

const cockpit = (props) => {

    const classes = [];
    if (props.persons.length <= 2) {
        classes.push("red");
    }
    if (props.persons.length <= 1) {
        classes.push("bold");
    }

    const StyledButton = styled.button`
        background-color: ${props => props.alt === true ? 'red' : 'green'};
        color:white;
        font: inherit;
        border: 1px solid blue;
        padding: 8px;
        cursor: pointer;
        &:hover {
            background-color: ${props => props.alt === true ? 'lightred' : 'lightgreen'};
            color:black;
        }
        `;

    return (
        <div>
            <h1 className={classes.join(' ')}>Test</h1>
            <StyledButton
                alt={props.hidden}
                onClick={props.clicked}>Switch name</StyledButton>
        </div>
    );
};

export default cockpit;