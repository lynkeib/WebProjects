import React, { useState, useEffect } from 'react';
import Model from '../../components/UI/Modal/Modal';
import Aux from '../Aux/Aux';

const withErrorHandler = (WrappedComponent, axios) => {
    return props => {

        const [error, setError] = useState(null);


        const reqInterceptor = axios.interceptors.request.use(req => {
            setError(null);
            return req;
        })
        const resInterceptor = axios.interceptors.response.use(res => res, err => {
            setError(err);
        });

        useEffect(() => {
            return () => {
                axios.interceptors.request.eject(reqInterceptor);
                axios.interceptors.request.eject(resInterceptor);
            }
        }, [reqInterceptor, resInterceptor])

        // componentWillMount() {
        //     axios.interceptors.request.use(req => {
        //         this.setState({ error: null });
        //         return req;
        //     })
        //     axios.interceptors.response.use(res => res, error => {
        //         this.setState({ error: error });
        //     });
        // }

        const errorConfirmedHandler = () => {
            setError(null)
        }


        return (
            <Aux>
                <Model
                    show={error}
                    modalClosed={errorConfirmedHandler}>
                    {error ? error.message : null}
                </Model>
                <WrappedComponent {...props} />
            </Aux>)

    }
}

export default withErrorHandler;