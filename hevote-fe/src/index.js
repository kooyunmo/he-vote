import { BrowserRouter } from 'react-router-dom';
import * as ReactDOM from 'react-dom/client';
import { Suspense } from 'react';

import 'antd/dist/antd.min.css';

import Router from './router';
import * as serviceWorker from './serviceWorker';
import reportWebVitals from './reportWebVitals';


const App = () => (
  <BrowserRouter>
    <Router />
  </BrowserRouter>
);

const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <Suspense fallback="...is loading">
    <App />
  </Suspense>,
);
// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
reportWebVitals();
