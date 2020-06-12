import reducer from './auth';
import * as actionTypes from '../actions/actionsTypes';

describe("auth reducer", () => {
    it("should return the niitial state", () => {
        expect(reducer(undefined, {})).toEqual({
            token: null,
            userId: null,
            error: null,
            loading: false,
            authRedirectPath: '/'
        });
    })

    it("should store the token upon login", () => {
        expect(reducer({
            token: null,
            userId: null,
            error: null,
            loading: false,
            authRedirectPath: '/'
        }, { type: actionTypes.AUTH_SUCCESS, idToken: "test", userId: "test" })).toEqual({
            token: "test",
            userId: "test",
            error: null,
            loading: false,
            authRedirectPath: '/'
        })
    })
});