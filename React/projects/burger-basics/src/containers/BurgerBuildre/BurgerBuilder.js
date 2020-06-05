import React, { Component } from 'react';
import Aux from '../../hoc/Aux/Aux';
import Burger from '../../components/Burger/Burger';
import BuildControls from '../../components/Burger/BuildControls/BuildControls';
import Modal from '../../components/UI/Modal/Modal';
import OrderSummary from '../../components/Burger/OrderSummary/OrderSummary';
import axios from '../../axios-orders';
import Spinner from '../../components/UI/Spinner/Spinner';
import withErrorHandler from '../../hoc/withErrorHandler/withErrorHandler';
import { connect } from 'react-redux';
import * as actions from '../../store/actions/index';

class BurgerBuilder extends Component {
    state = {
        purchasing: false,
        loading: false,
        error: false
    }

    componentDidMount() {
        // axios.get('/ingredients.json')
        //     .then(response => {
        //         this.setState({ ingredients: response.data })
        //     })
        //     .catch(error => { this.setState({ error: true }) });
        this.props.onInitIngredients();
    }

    // updatePurchaseState = (ingredients) => {
    //     // const ingredients = { ...this.state.ingredients };
    //     const sum = Object.keys(ingredients)
    //         .map(igKey => (
    //             ingredients[igKey]
    //         ))
    //         .reduce((sum, el) => sum + el, 0);
    //     this.setState({ purchasable: sum > 0 });
    // }
    updatePurchaseState = (ingredients) => {
        // const ingredients = { ...this.state.ingredients };
        const sum = Object.keys(ingredients)
            .map(igKey => (
                ingredients[igKey]
            ))
            .reduce((sum, el) => sum + el, 0);
        return sum > 0;
    }

    purchaseHandler = () => {
        this.setState({ purchasing: true });
    }

    // addIngredientHandler = (type) => {
    //     const oldCount = this.state.ingredients[type];
    //     const updatedCount = oldCount + 1;
    //     const updatedIngredients = { ...this.state.ingredients };
    //     updatedIngredients[type] = updatedCount;

    //     const oldPrice = this.state.totalPrice;
    //     const newPrice = oldPrice + INGREDIENT_PRICES[type];
    //     this.setState({ ingredients: updatedIngredients, totalPrice: newPrice });
    //     this.updatePurchaseState(updatedIngredients);
    // }

    // removeIngredientHandler = (type) => {
    //     const oldCount = this.state.ingredients[type];
    //     if (oldCount > 0) {
    //         const updatedCount = oldCount - 1;
    //         const updatedIngredients = { ...this.state.ingredients };
    //         updatedIngredients[type] = updatedCount;

    //         const oldPrice = this.state.totalPrice;
    //         const newPrice = oldPrice - INGREDIENT_PRICES[type];
    //         this.setState({ ingredients: updatedIngredients, totalPrice: newPrice });
    //         this.updatePurchaseState(updatedIngredients);
    //     }
    // }

    purchaseCancelHandler = () => {
        this.setState({ purchasing: false })
    }

    // purchaseContinueHandler = () => {
    //     // alert("Continue");
    //     const queryParams = [];
    //     for (let i in this.state.ingredients) {
    //         queryParams.push(encodeURIComponent(i) + '=' + encodeURIComponent(this.state.ingredients[i]));
    //     }
    //     queryParams.push('price=' + this.state.totalPrice);
    //     const queryString = queryParams.join("&");
    //     this.props.history.push({
    //         pathname: '/checkout',
    //         search: '?' + queryString
    //     });
    // }
    purchaseContinueHandler = () => {
        this.props.onInitPurchase();
        this.props.history.push({
            pathname: '/checkout'
        });
    }

    render() {
        const disableInfo = {
            ...this.props.ings
        }

        for (let key in disableInfo) {
            disableInfo[key] = disableInfo[key] === 0 ? true : false;
        }
        let orderSummary = null;
        let burger = this.props.error ? <p>Ingredients cannot be loaded</p> : <Spinner />
        if (this.props.ings) {
            burger = (<Aux><Burger ingredients={this.props.ings} />
                <BuildControls
                    ingredientAdded={this.props.onIngredientAdded}
                    ingredientRemove={this.props.onIngredientRemoved}
                    disabled={disableInfo}
                    price={this.props.price}
                    purchasable={this.updatePurchaseState(this.props.ings)}
                    ordered={this.purchaseHandler} /></Aux>);
            orderSummary = <OrderSummary
                ingredients={this.props.ings}
                price={this.props.price}
                purchaseCanceled={this.purchaseCancelHandler}
                purchaseContinued={this.purchaseContinueHandler} />;
        }
        if (this.state.loading) {
            orderSummary = <Spinner />;
        }

        return (
            <Aux>
                <Modal show={this.state.purchasing} modalClosed={this.purchaseCancelHandler}>
                    {orderSummary}
                </Modal>
                {burger}
            </Aux>
        );
    }
}

const mapDispatchToProps = dispatch => {
    return {
        onIngredientAdded: (ingName) => dispatch(actions.addIngredient(ingName)),
        onIngredientRemoved: (ingName) => dispatch(actions.removeIngredient(ingName)),
        onInitIngredients: () => dispatch(actions.initIngredients()),
        onInitPurchase: () => dispatch(actions.purchaseInit())
    };
};

const mapStateToProps = state => {
    return {
        ings: state.burgerBuilder.ingredients,
        price: state.burgerBuilder.totalPrice,
        error: state.burgerBuilder.error
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(withErrorHandler(BurgerBuilder, axios));