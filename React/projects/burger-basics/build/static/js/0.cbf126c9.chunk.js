webpackJsonp([0],{142:function(e,t,n){"use strict";function a(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function r(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!==typeof t&&"function"!==typeof t?e:t}function o(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}Object.defineProperty(t,"__esModule",{value:!0});var i=n(0),c=n.n(i),u=n(149),l=n(7),s=n(152),p=n(6),d=function(){function e(e,t){for(var n=0;n<t.length;n++){var a=t[n];a.enumerable=a.enumerable||!1,a.configurable=!0,"value"in a&&(a.writable=!0),Object.defineProperty(e,a.key,a)}}return function(t,n,a){return n&&e(t.prototype,n),a&&e(t,a),t}}(),m=function(e){function t(){var e,n,o,i;a(this,t);for(var c=arguments.length,u=Array(c),l=0;l<c;l++)u[l]=arguments[l];return n=o=r(this,(e=t.__proto__||Object.getPrototypeOf(t)).call.apply(e,[this].concat(u))),o.checkoutCancelledHandler=function(){o.props.history.goBack()},o.checkoutContinuedHandler=function(){o.props.history.replace("/checkout/contact-data")},i=n,r(o,i)}return o(t,e),d(t,[{key:"render",value:function(){var e=c.a.createElement(l.c,{to:"/"});if(this.props.ings){var t=this.props.purchased?c.a.createElement(l.c,{to:"/"}):null;e=c.a.createElement("div",null,t,c.a.createElement(u.a,{ingredients:this.props.ings,checkoutCancelled:this.checkoutCancelledHandler,checkoutContinued:this.checkoutContinuedHandler}),c.a.createElement(l.d,{path:this.props.match.path+"/contact-data",component:s.a}))}return e}}]),t}(i.Component),h=function(e){return{ings:e.burgerBuilder.ingredients,purchased:e.order.purchased}};t.default=Object(p.b)(h,null)(m)},145:function(e,t,n){"use strict";var a=n(0),r=n.n(a),o=n(146),i=n.n(o),c=function(e){var t=null,n=[i.a.inputElement];switch(e.invalid&&e.shouldValidate&&e.touched&&n.push(i.a.Invalid),e.elementType){case"input":t=r.a.createElement("input",Object.assign({className:n.join(" ")},e.elementConfig,{value:e.value,onChange:e.changed}));break;case"textarea":t=r.a.createElement("textarea",Object.assign({className:i.a.inputElement},e.elementConfig,{value:e.value,onChange:e.changed}));break;case"select":t=r.a.createElement("select",{className:i.a.inputElement,value:e.value,onChange:e.changed},e.elementConfig.options.map(function(e){return r.a.createElement("option",{key:e.value,value:e.value},e.displayValue)}));break;default:t=r.a.createElement("input",Object.assign({className:n.join(" ")},e.elementConfig,{value:e.value,onChange:e.changed}))}return r.a.createElement("div",{className:i.a.Input},r.a.createElement("label",{className:i.a.Label},e.label),t)};t.a=c},146:function(e,t,n){var a=n(147);"string"===typeof a&&(a=[[e.i,a,""]]);var r={};r.transform=void 0;n(141)(a,r);a.locals&&(e.exports=a.locals)},147:function(e,t,n){t=e.exports=n(140)(!0),t.push([e.i,".Input__Input__s67N0{width:100%;padding:10px;-webkit-box-sizing:border-box;box-sizing:border-box}.Input__Label___n-1m{font-weight:700;display:block;margin-bottom:8px}.Input__InputElement__2-aFx{outline:none;border:1px solid #ccc;background-color:#fff;font:inherit;padding:6px 10px;width:100%}.Input__InputElement__2-aFx:focus{outline:none;background-color:#ccc}.Input__Invalid__1sl1p{border:1px solid red;background-color:#fda49a}","",{version:3,sources:["/Users/chengyinliu/D/Github/WebProjects/React/projects/burger-basics/src/components/UI/Input/Input.css"],names:[],mappings:"AAAA,qBACI,WAAiB,AACjB,aAAiB,AACjB,8BAA+B,AACvB,qBAAuB,CAClC,AAED,qBACI,gBAAoB,AACpB,cAAqB,AACrB,iBAAmB,CACtB,AAED,4BACI,aAAuB,AACvB,sBAAiC,AACjC,sBAAwB,AACxB,aAA0B,AAC1B,iBAA2B,AAC3B,UAAuB,CAC1B,AAED,kCACI,aAAuB,AACvB,qBAAuB,CAC1B,AAED,uBACI,qBAAgC,AAChC,wBAA0B,CAE7B",file:"Input.css",sourcesContent:[".Input {\n    width     : 100%;\n    padding   : 10px;\n    -webkit-box-sizing: border-box;\n            box-sizing: border-box;\n}\n\n.Label {\n    font-weight  : bold;\n    display      : block;\n    margin-bottom: 8px;\n}\n\n.InputElement {\n    outline         : none;\n    border          : 1px solid #ccc;\n    background-color: white;\n    font            : inherit;\n    padding         : 6px 10px;\n    width           : 100%;\n}\n\n.InputElement:focus {\n    outline         : none;\n    background-color: #ccc;\n}\n\n.Invalid {\n    border          : 1px solid red;\n    background-color: #fda49a;\n\n}"],sourceRoot:""}]),t.locals={Input:"Input__Input__s67N0",Label:"Input__Label___n-1m",InputElement:"Input__InputElement__2-aFx",Invalid:"Input__Invalid__1sl1p"}},148:function(e,t,n){"use strict";n.d(t,"a",function(){return a});var a=function(e,t){var n=!0;return t.required&&(n=""!==e.trim()&&n),t.minLength&&(n=e.length>=t.minLength&&n),t.maxLength&&(n=e.length<=t.maxLength&&n),n}},149:function(e,t,n){"use strict";var a=n(0),r=n.n(a),o=n(50),i=n(47),c=n(150),u=n.n(c),l=function(e){return r.a.createElement("div",{className:u.a.CheckoutSummary},r.a.createElement("h1",null,"We hope it tastes well!"),r.a.createElement("div",{style:{width:"100%",margin:"auto"}},r.a.createElement(o.a,{ingredients:e.ingredients})),r.a.createElement(i.a,{btnType:"Danger",clicked:e.checkoutCancelled},"CANCEL"),r.a.createElement(i.a,{btnType:"Success",clicked:e.checkoutContinued},"CONTINUE"))};t.a=l},150:function(e,t,n){var a=n(151);"string"===typeof a&&(a=[[e.i,a,""]]);var r={};r.transform=void 0;n(141)(a,r);a.locals&&(e.exports=a.locals)},151:function(e,t,n){t=e.exports=n(140)(!0),t.push([e.i,".CheckoutSummary__CheckoutSummary__1xBm4{text-align:center;width:80%;margin:auto}","",{version:3,sources:["/Users/chengyinliu/D/Github/WebProjects/React/projects/burger-basics/src/components/Order/CheckoutSummary/CheckoutSummary.css"],names:[],mappings:"AAAA,yCACI,kBAAmB,AACnB,UAAgB,AAChB,WAAiB,CACpB",file:"CheckoutSummary.css",sourcesContent:[".CheckoutSummary {\n    text-align: center;\n    width     : 80%;\n    margin    : auto;\n}\n\n/* @media (min-width: 600px) {\n    .CheckoutSummary {\n        width: 500px;\n    }\n} */"],sourceRoot:""}]),t.locals={CheckoutSummary:"CheckoutSummary__CheckoutSummary__1xBm4"}},152:function(e,t,n){"use strict";function a(e,t){if(!(e instanceof t))throw new TypeError("Cannot call a class as a function")}function r(e,t){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!t||"object"!==typeof t&&"function"!==typeof t?e:t}function o(e,t){if("function"!==typeof t&&null!==t)throw new TypeError("Super expression must either be null or a function, not "+typeof t);e.prototype=Object.create(t&&t.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),t&&(Object.setPrototypeOf?Object.setPrototypeOf(e,t):e.__proto__=t)}var i=n(0),c=n.n(i),u=n(47),l=n(153),s=n.n(l),p=n(12),d=n(48),m=n(145),h=n(6),A=n(49),f=n(11),g=n(148),b=function(){function e(e,t){for(var n=0;n<t.length;n++){var a=t[n];a.enumerable=a.enumerable||!1,a.configurable=!0,"value"in a&&(a.writable=!0),Object.defineProperty(e,a.key,a)}}return function(t,n,a){return n&&e(t.prototype,n),a&&e(t,a),t}}(),C=function(e){function t(){var e,n,o,i;a(this,t);for(var c=arguments.length,u=Array(c),l=0;l<c;l++)u[l]=arguments[l];return n=o=r(this,(e=t.__proto__||Object.getPrototypeOf(t)).call.apply(e,[this].concat(u))),o.state={orderForm:{name:{elementType:"input",elementConfig:{type:"text",placeholder:"Your Name"},value:"",validation:{required:!0},valid:!1,touched:!1},street:{elementType:"input",elementConfig:{type:"text",placeholder:"Your Street"},value:"",validation:{required:!0},valid:!1,touched:!1},zipCode:{elementType:"input",elementConfig:{type:"text",placeholder:"Your Zip"},value:"",validation:{required:!0,minLength:5,maxLength:5},valid:!1,touched:!1},country:{elementType:"input",elementConfig:{type:"text",placeholder:"Your Country"},value:"",validation:{required:!0},valid:!1,touched:!1},email:{elementType:"input",elementConfig:{type:"email",placeholder:"Your Email"},value:"",validation:{required:!0},valid:!1,touched:!1},deliveryMethod:{elementType:"select",elementConfig:{options:[{value:"fastest",displayValue:"Fastest"},{value:"cheapest",displayValue:"Cheapest"}]},value:"fastest",valid:!0,validation:{}}},formIsValid:!1,loading:!1},o.orderHandler=function(e){e.preventDefault();var t={};for(var n in o.state.orderForm)t[n]=o.state.orderForm[n].value;var a={ingredients:o.props.ings,price:o.props.price,orderData:t,userId:o.props.userId};o.props.onOrderBurger(a,o.props.token)},o.inputChangedHandler=function(e,t){var n=Object.assign({},o.state.orderForm),a=Object.assign({},n[t]);a.value=e.target.value,a.valid=Object(g.a)(e.target.value,a.validation),a.touched=!0,n[t]=a;var r=!0;for(var i in n)r=n[i].valid&&r;o.setState({orderForm:n,formIsValid:r})},i=n,r(o,i)}return o(t,e),b(t,[{key:"render",value:function(){var e=this,t=[];for(var n in this.state.orderForm)t.push({id:n,config:this.state.orderForm[n]});var a=c.a.createElement("form",{onSubmit:this.orderHandler},t.map(function(t){return c.a.createElement(m.a,{key:t.id,elementType:t.config.elementType,elementConfig:t.config.elementConfig,vlaue:t.config.value,invalid:!t.config.valid,shouldValidate:t.config.validation,touched:t.config.touched,changed:function(n){return e.inputChangedHandler(n,t.id)}})}),c.a.createElement(u.a,{btnType:"Success",disabled:!this.state.formIsValid},"ORDER"));return this.props.loading&&(a=c.a.createElement(d.a,null)),c.a.createElement("div",{className:s.a.ContactData},c.a.createElement("h4",null,"Enter your contact data"),a)}}]),t}(i.Component),v=function(e){return{ings:e.burgerBuilder.ingredients,price:e.burgerBuilder.totalPrice,loading:e.order.loading,token:e.auth.token,userId:e.auth.userId}},y=function(e){return{onOrderBurger:function(t,n){return e(f.g(t,n))}}};t.a=Object(h.b)(v,y)(Object(A.a)(C,p.a))},153:function(e,t,n){var a=n(154);"string"===typeof a&&(a=[[e.i,a,""]]);var r={};r.transform=void 0;n(141)(a,r);a.locals&&(e.exports=a.locals)},154:function(e,t,n){t=e.exports=n(140)(!0),t.push([e.i,".ContactData__ContactData__1J81r{margin:20px auto;width:80%;text-align:center;-webkit-box-shadow:0 2px 3px #ccc;box-shadow:0 2px 3px #ccc;border:1px solid #eee;padding:10px;-webkit-box-sizing:border-box;box-sizing:border-box}@media (min-width:600px){.ContactData__ContactData__1J81r{width:500px}}","",{version:3,sources:["/Users/chengyinliu/D/Github/WebProjects/React/projects/burger-basics/src/containers/Checkout/ContactData/ContactData.css"],names:[],mappings:"AAAA,iCACI,iBAAsB,AACtB,UAAgB,AAChB,kBAAmB,AACnB,kCAAmC,AAC3B,0BAA2B,AACnC,sBAA2B,AAC3B,aAAiB,AACjB,8BAA+B,AACvB,qBAAuB,CAClC,AAED,yBACI,iCACI,WAAa,CAChB,CACJ",file:"ContactData.css",sourcesContent:[".ContactData {\n    margin    : 20px auto;\n    width     : 80%;\n    text-align: center;\n    -webkit-box-shadow: 0 2px 3px #ccc;\n            box-shadow: 0 2px 3px #ccc;\n    border    : 1px solid #eee;\n    padding   : 10px;\n    -webkit-box-sizing: border-box;\n            box-sizing: border-box;\n}\n\n@media (min-width: 600px) {\n    .ContactData {\n        width: 500px;\n    }\n}"],sourceRoot:""}]),t.locals={ContactData:"ContactData__ContactData__1J81r"}}});
//# sourceMappingURL=0.cbf126c9.chunk.js.map