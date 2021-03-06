+ Note
	+ StateFul & StateLess (State can be used both in class and function)
	+ When passing functions, it is recommended to pass the reference of the function (using .bind to pass args) rather than anonymous function for the sake of high performance 
	+ Elements in .js that are similiar to HTML, they are not HTML, they are JXS, JS in HTML format. Therefore, some props names are different from HTML
	+ Functional & class-based components
		+ Use class if you need to manage State or access to Lifecycle Hooks and you don't want to use React Hooks.
	+ Components Lifecycle - Creation
		+ constructor(props)
		+ getDerivedStateFromProps(props, state)
		+ render()
		+ Render Child Components
		+ componentDidMount()
	+ Components Lifecycle - Update
		+ getDerivedStateFromProps(props, state)
		+ shouldComponentUpdate(nextProps, nextState)
		+ render()
		+ Update Child Components Props
		+ getSnapShotBeforeUpdate(prevProps, prevState, snapshot)
		+ comopnentDidUpdate()
	+ Components Lifecycle - Update (triggered by Parent)
		+ componentWillReceiveProps(nextProps)
		+ shouldComponentUpdate(nextProps, nextState)
		+ componentWillUpdate(nextProps, nextState)
		+ render()
		+ Update Child Components Props
		+ comopnentDidUpdate()
	+ UseEffect
		+ Combine functionalities of all class-based lifecycle hocks into one React hock.
	+ React.memo() (used on functional components for controlling update process == shouldComponentUpdate in class-based)
	+ PureComponent (implemented all the props check in shouldComponetUpdate for Component extention)
	+ Rendering adjacent root JSX elements => using array of elements like [<p key=></p>, <div key=></div>, <input key=/>] in render function __OR__ using Higher Order Component wraps all the tags (Self-defined or <Fragment>)
	+ Redux Workflow:   
	<div>
		<img src="https://gdurl.com/4ynX" width="80%"/>  
	</div>  

	+ About Redux: Action Creators can run Async Code, Reduce can only run Sync Code
	+ When using State in Functional Components, it is needed to update all the proporties in the original state since it's not like state in Class-based Components which has setState to merge original state and the updated state object
	+ Hocks can noly be used in the root level of a Functional Component
	+ Add the second argument of useEffect can make it run only once (after the first render) (an empty array [] can be that second argument, or, the dependency of useEffect) (like componentDidMount)
	+ React Projects Demo (react.rocks, madewithReact)
	+ React Native is a JavaScript library to use JS and React to build mobile web app
	+ Material-UI, a component library (like React bootstrap)
	+ PReact (Light version of React)

+ Useful Packages
	+ Radium
	+ Styled-Components	(using style tag as component)
	+ Prop-Types (props typing)
	+ Axios (Http requests)
	+ React-Router, React-Router-Dom (Add Router function)
	+ Redux (Global State Management)
	+ Enzyme (Unit Test)
