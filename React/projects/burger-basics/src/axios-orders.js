import axios from 'axios';

const instance = axios.create({ baseURL: 'https://react-burger-71fca.firebaseio.com/' });

export default instance;