import React, { Component } from 'react';
import Button from '../../../components/UI/Button/Button';
import classes from './ContactData.css';
import axios from '../../../axios-orders';
import Spinner from '../../../components/UI/Spinner/Spinner';

class ContactData extends Component {

    state = {
        name: '',
        email: '',
        address: {
            street: '',
            postalCode: ''
        },
        loading: false
    }

    orderHandler = (event) => {
        event.preventDefault();
        this.setState({ loading: true });
        const order = {
            ingredients: this.props.ingredients,
            price: this.props.price,

            customer: {
                name: "test",
                address: {
                    street: 'test',
                    zipCode: '12345',
                    contry: 'test'
                },
                email: '123@124.com'
            },
            deliveryMethod: 'slowest'
        }

        axios.post('/orders.json', order)
            .then(response => {
                this.setState({ loading: false })
                this.props.history.push('/')
            })
            .catch(error => { this.setState({ loading: false }) });
    }

    render() {

        let form = (<form>
            <input className={classes.Input} type="text" name="name" placeholder="Your name" />
            <input className={classes.Input} type="email" name="email" placeholder="Your email" />
            <input className={classes.Input} type="text" name="street" placeholder="Your street" />
            <input className={classes.Input} type="text" name="postal" placeholder="Your postal" />
            <Button btnType="Success" clicked={this.orderHandler}>ORDER</Button>
        </form>);
        if (this.state.loading) {
            form = <Spinner />
        }

        return (
            <div className={classes.ContactData}>
                <h4>Enter your contact data</h4>
                {form}
            </div>
        );
    }
}

export default ContactData;