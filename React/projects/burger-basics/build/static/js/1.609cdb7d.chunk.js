webpackJsonp([1],{144:function(e,n,t){"use strict";function a(e,n,t){return n in e?Object.defineProperty(e,n,{value:t,enumerable:!0,configurable:!0,writable:!0}):e[n]=t,e}function o(e,n){if(!(e instanceof n))throw new TypeError("Cannot call a class as a function")}function i(e,n){if(!e)throw new ReferenceError("this hasn't been initialised - super() hasn't been called");return!n||"object"!==typeof n&&"function"!==typeof n?e:n}function r(e,n){if("function"!==typeof n&&null!==n)throw new TypeError("Super expression must either be null or a function, not "+typeof n);e.prototype=Object.create(n&&n.prototype,{constructor:{value:e,enumerable:!1,writable:!0,configurable:!0}}),n&&(Object.setPrototypeOf?Object.setPrototypeOf(e,n):e.__proto__=n)}Object.defineProperty(n,"__esModule",{value:!0});var u=t(0),l=t.n(u),c=t(145),s=t(47),p=t(158),A=t.n(p),d=t(11),h=t(6),b=t(48),g=t(7),f=t(148),m=function(){function e(e,n){for(var t=0;t<n.length;t++){var a=n[t];a.enumerable=a.enumerable||!1,a.configurable=!0,"value"in a&&(a.writable=!0),Object.defineProperty(e,a.key,a)}}return function(n,t,a){return t&&e(n.prototype,t),a&&e(n,a),n}}(),v=function(e){function n(){var e,t,r,u;o(this,n);for(var l=arguments.length,c=Array(l),s=0;s<l;s++)c[s]=arguments[s];return t=r=i(this,(e=n.__proto__||Object.getPrototypeOf(n)).call.apply(e,[this].concat(c))),r.state={controls:{email:{elementType:"input",elementConfig:{type:"email",placeholder:"Email"},value:"",validation:{required:!0,isEmail:!0},valid:!1,touched:!1},password:{elementType:"input",elementConfig:{type:"password",placeholder:"Password"},value:"",validation:{required:!0,minLength:6},valid:!1,touched:!1}},isSignup:!0},r.switchAuthModeHandler=function(){r.setState(function(e){return{isSignup:!e.isSignup}})},r.inputChangedHandler=function(e,n){var t=Object.assign({},r.state.controls,a({},n,Object.assign({},r.state.controls[n],{value:e.target.value,valid:Object(f.a)(e.target.value,r.state.controls[n].validation),touched:!0})));r.setState({controls:t})},r.submitHandler=function(e){e.preventDefault(),r.props.onAuth(r.state.controls.email.value,r.state.controls.password.value,r.state.isSignup)},u=t,i(r,u)}return r(n,e),m(n,[{key:"componentDidMount",value:function(){this.props.buildingBurger||"/"===this.props.authRedirectPath||this.props.onSetAuthRedirectPath()}},{key:"render",value:function(){var e=this,n=[];for(var t in this.state.controls)n.push({id:t,config:this.state.controls[t]});var a=n.map(function(n){return l.a.createElement(c.a,{key:n.id,elementType:n.config.elementType,elementConfig:n.config.elementConfig,vlaue:n.config.value,invalid:!n.config.valid,shouldValidate:n.config.validation,touched:n.config.touched,changed:function(t){return e.inputChangedHandler(t,n.id)}})});this.props.loading&&(a=l.a.createElement(b.a,null));var o=null;this.props.error&&(o=l.a.createElement("p",null,this.props.error.message));var i=null;return this.state.isAuthenticated&&(i=l.a.createElement(g.c,{to:this.props.authRedirectPath})),l.a.createElement("div",{className:A.a.Auth},i,o,l.a.createElement("form",{onSubmit:function(n){return e.submitHandler(n)}},a,l.a.createElement(s.a,{btnType:"Success"},"Submit")),l.a.createElement(s.a,{clicked:this.switchAuthModeHandler,btnType:"Danger"},"Switch to ",this.state.isSignup?"signin":"signup"))}}]),n}(u.Component),B=function(e){return{loading:e.auth.loading,error:e.auth.error,isAuthenticated:null!==e.auth.token,buildingBurger:e.burgerBuilder.building,authRedirectPath:e.auth.authRedirectPath}},C=function(e){return{onAuth:function(n,t,a){return e(d.b(n,t,a))},onSetAuthRedirectPath:function(){return e(d.j("/"))}}};n.default=Object(h.b)(B,C)(v)},145:function(e,n,t){"use strict";var a=t(0),o=t.n(a),i=t(146),r=t.n(i),u=function(e){var n=null,t=[r.a.inputElement];switch(e.invalid&&e.shouldValidate&&e.touched&&t.push(r.a.Invalid),e.elementType){case"input":n=o.a.createElement("input",Object.assign({className:t.join(" ")},e.elementConfig,{value:e.value,onChange:e.changed}));break;case"textarea":n=o.a.createElement("textarea",Object.assign({className:r.a.inputElement},e.elementConfig,{value:e.value,onChange:e.changed}));break;case"select":n=o.a.createElement("select",{className:r.a.inputElement,value:e.value,onChange:e.changed},e.elementConfig.options.map(function(e){return o.a.createElement("option",{key:e.value,value:e.value},e.displayValue)}));break;default:n=o.a.createElement("input",Object.assign({className:t.join(" ")},e.elementConfig,{value:e.value,onChange:e.changed}))}return o.a.createElement("div",{className:r.a.Input},o.a.createElement("label",{className:r.a.Label},e.label),n)};n.a=u},146:function(e,n,t){var a=t(147);"string"===typeof a&&(a=[[e.i,a,""]]);var o={};o.transform=void 0;t(141)(a,o);a.locals&&(e.exports=a.locals)},147:function(e,n,t){n=e.exports=t(140)(!0),n.push([e.i,".Input__Input__s67N0{width:100%;padding:10px;-webkit-box-sizing:border-box;box-sizing:border-box}.Input__Label___n-1m{font-weight:700;display:block;margin-bottom:8px}.Input__InputElement__2-aFx{outline:none;border:1px solid #ccc;background-color:#fff;font:inherit;padding:6px 10px;width:100%}.Input__InputElement__2-aFx:focus{outline:none;background-color:#ccc}.Input__Invalid__1sl1p{border:1px solid red;background-color:#fda49a}","",{version:3,sources:["/Users/chengyinliu/D/Github/WebProjects/React/projects/burger-basics/src/components/UI/Input/Input.css"],names:[],mappings:"AAAA,qBACI,WAAiB,AACjB,aAAiB,AACjB,8BAA+B,AACvB,qBAAuB,CAClC,AAED,qBACI,gBAAoB,AACpB,cAAqB,AACrB,iBAAmB,CACtB,AAED,4BACI,aAAuB,AACvB,sBAAiC,AACjC,sBAAwB,AACxB,aAA0B,AAC1B,iBAA2B,AAC3B,UAAuB,CAC1B,AAED,kCACI,aAAuB,AACvB,qBAAuB,CAC1B,AAED,uBACI,qBAAgC,AAChC,wBAA0B,CAE7B",file:"Input.css",sourcesContent:[".Input {\n    width     : 100%;\n    padding   : 10px;\n    -webkit-box-sizing: border-box;\n            box-sizing: border-box;\n}\n\n.Label {\n    font-weight  : bold;\n    display      : block;\n    margin-bottom: 8px;\n}\n\n.InputElement {\n    outline         : none;\n    border          : 1px solid #ccc;\n    background-color: white;\n    font            : inherit;\n    padding         : 6px 10px;\n    width           : 100%;\n}\n\n.InputElement:focus {\n    outline         : none;\n    background-color: #ccc;\n}\n\n.Invalid {\n    border          : 1px solid red;\n    background-color: #fda49a;\n\n}"],sourceRoot:""}]),n.locals={Input:"Input__Input__s67N0",Label:"Input__Label___n-1m",InputElement:"Input__InputElement__2-aFx",Invalid:"Input__Invalid__1sl1p"}},148:function(e,n,t){"use strict";t.d(n,"a",function(){return a});var a=function(e,n){var t=!0;return n.required&&(t=""!==e.trim()&&t),n.minLength&&(t=e.length>=n.minLength&&t),n.maxLength&&(t=e.length<=n.maxLength&&t),t}},158:function(e,n,t){var a=t(159);"string"===typeof a&&(a=[[e.i,a,""]]);var o={};o.transform=void 0;t(141)(a,o);a.locals&&(e.exports=a.locals)},159:function(e,n,t){n=e.exports=t(140)(!0),n.push([e.i,".Auth__Auth__2YUr1{margin:20px auto;width:80%;text-align:center;-webkit-box-shadow:0 2px 3px #ccc;box-shadow:0 2px 3px #ccc;border:1px solid #eee;padding:10px;-webkit-box-sizing:border-box;box-sizing:border-box}@media (min-width:600px){.Auth__Auth__2YUr1{width:500px}}","",{version:3,sources:["/Users/chengyinliu/D/Github/WebProjects/React/projects/burger-basics/src/containers/Auth/Auth.css"],names:[],mappings:"AAAA,mBACI,iBAAsB,AACtB,UAAgB,AAChB,kBAAmB,AACnB,kCAAmC,AAC3B,0BAA2B,AACnC,sBAA2B,AAC3B,aAAiB,AACjB,8BAA+B,AACvB,qBAAuB,CAClC,AAED,yBACI,mBACI,WAAa,CAChB,CACJ",file:"Auth.css",sourcesContent:[".Auth {\n    margin    : 20px auto;\n    width     : 80%;\n    text-align: center;\n    -webkit-box-shadow: 0 2px 3px #ccc;\n            box-shadow: 0 2px 3px #ccc;\n    border    : 1px solid #eee;\n    padding   : 10px;\n    -webkit-box-sizing: border-box;\n            box-sizing: border-box;\n}\n\n@media (min-width: 600px) {\n    .Auth {\n        width: 500px;\n    }\n}"],sourceRoot:""}]),n.locals={Auth:"Auth__Auth__2YUr1"}}});
//# sourceMappingURL=1.609cdb7d.chunk.js.map