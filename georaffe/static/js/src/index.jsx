import React from 'react';
import ReactDOM from 'react-dom';
import { HashRouter } from 'react-router-dom';
import App from './App.jsx';

ReactDOM.render(
  <HashRouter>
    {/* <BrowserRouter> */}
    <App />
    {/* </BrowserRouter>, */}
  </HashRouter>,
  document.querySelector('#root'),
);
