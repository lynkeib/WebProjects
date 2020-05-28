import React, { Component } from 'react';

const asyncComponent = (importCpomponent) => {
    return class extends Component {

        state = {
            component: null
        }

        componentDidMount() {
            importCpomponent().then(cmp => {
                this.setState({ component: cmp.default });
            });
        }

        render() {
            const C = this.state.component;
            return C ? <C {...this.props}></C> : null;
        }
    }
}

export default asyncComponent;