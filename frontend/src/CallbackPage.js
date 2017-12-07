import * as React from 'react';
import * as ReactRedux from 'react-redux';
import * as ReactRouterRedux from 'react-router-redux';
import * as ReduxOidc from 'redux-oidc';

import userManager from './userManager';

class CallbackView extends React.Component {
  render() {
    return (
        <ReduxOidc.CallbackComponent
          userManager={userManager}
          successCallback={this.successCallback}
          errorCallback={this.errorCallback}
          >
          <div>
            Redirecting...
          </div>
        </ReduxOidc.CallbackComponent>
    );
  }

  successCallback = () => {
    this.props.onSuccess();
  }

  errorCallback = () => {
    this.props.onError();
  }
}

const mapStateToProps = null;

const mapDispatchToProps = (dispatch) => ({
  onSuccess: () => dispatch(ReactRouterRedux.push('/')),
  onError: () => dispatch(ReactRouterRedux.push('/')),
});

const CallbackPage = ReactRedux.connect(
  mapStateToProps, mapDispatchToProps)(CallbackView);

export default CallbackPage;
