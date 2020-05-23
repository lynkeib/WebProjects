import React from 'react'
import classes from './Toolbar.css';
import Log from '../../Logo/Logo';

const toolbar = (props) => (
    <header className={classes.Toolbar}>
        <div>MENU</div>
        <Log></Log>
        <nav>...</nav>
    </header>
)

export default toolbar;