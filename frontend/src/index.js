import * as History from 'history';
import * as OidcClient from  'oidc-client';
import * as React from 'react';
import * as ReactDOM from 'react-dom';
import * as ReactRedux from 'react-redux';
import * as ReactRouter from 'react-router';
import * as ReactRouterRedux from 'react-router-redux';
import * as Redux from 'redux';
import * as ReduxLogger from 'redux-logger';
import * as ReduxOidc from 'redux-oidc';

import CallbackPage from './CallbackPage';
import HomePage from './HomePage';
import SilentRenewPage from './SilentRenewPage';
import registerServiceWorker from './registerServiceWorker';
import userManager from './userManager';

import './index.css';

OidcClient.Log.logger = console;

const history = History.createBrowserHistory();
const routerMiddleware = ReactRouterRedux.routerMiddleware(history);
const loggerMiddleware = ReduxLogger.createLogger();
const rootReducer = Redux.combineReducers({
  oidc: ReduxOidc.reducer,
  router: ReactRouterRedux.routerReducer,
});

const store = Redux.createStore(
  rootReducer,
  Redux.applyMiddleware(
    loggerMiddleware,
    routerMiddleware,
  ));

ReduxOidc.loadUser(store, userManager);

ReactDOM.render(
  <ReactRedux.Provider store={store}>
    <ReduxOidc.OidcProvider store={store} userManager={userManager}>
      <ReactRouterRedux.ConnectedRouter history={history}>
        <div>
          <ReactRouter.Route exact path="/" component={HomePage}/>
          <ReactRouter.Route
            path="/login-callback"
            component={CallbackPage}
            />
          <ReactRouter.Route
            path="/login-silent-renew"
            component={SilentRenewPage}
            />
        </div>
      </ReactRouterRedux.ConnectedRouter>
    </ReduxOidc.OidcProvider>
  </ReactRedux.Provider>,
  document.getElementById('root'));

registerServiceWorker();
