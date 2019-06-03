import React from 'react';
import dva from 'dva';
import createHistory from 'history/createMemoryHistory';
import { Router, Route, Switch } from 'dva/router';

import App from '../../src/routes/app';
import './app.less';

// 1. Initialize
const app = dva({
  history: createHistory(),
});

// 3. Model
app.model(require('../../src/models/app'));

// 4. Router
app.router(({ history }) => (
  <Router history={history}>
    <Switch>
      <Route path="/" exact component={App}/>
    </Switch>
  </Router>
));

// 5. Start
app.start('#root');
