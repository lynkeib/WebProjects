import React from 'react';

const Validation = (props) => {

    let warning = "";
    if (props.textLength < 5) {
        warning = "Test too short";
    } else {
        warning = "Test long enough";
    }
    return (
        <p>{warning}</p>
    )
}

export default Validation;