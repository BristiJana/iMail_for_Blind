import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';

import App from './App';
import Main from './Main';

const Home = () => {
  return (
    <div>
      <Router>
      
        <Switch>
          <Route path="/" exact>
            <App/>
          </Route>

          <Route path="/main" exact>
            <Main />
          </Route>
          
        </Switch>
      </Router>
    </div>
  );
};

export default Home;

