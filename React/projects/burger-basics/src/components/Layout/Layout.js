import React from 'react';
import Aux from '../../hoc/Aux';
import classes from './Layout.css';


const layout = (props) => (
    <Aux>
        <div>
            Tollbar, sideDrawer, Backdrop
        </div>
        <main className={classes.Content}>
            {props.children}
        </main>
    </Aux>
);

export default layout;