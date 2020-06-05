import React from 'react';
import NavigationItem from './NavigationItem/NavigationItem';
import classes from './NavigationItems.css'

const navigationItems = () => (
    <ul className={classes.NavigationItems}>
        <NavigationItem link="/" exact>Burger Builder</NavigationItem>
        <NavigationItem link="/orders">Checkout</NavigationItem>
        <NavigationItem link="/auth">Auth</NavigationItem>
    </ul>
)

export default navigationItems;