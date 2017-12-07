import * as React from 'react';
import * as ReactRedux from 'react-redux';

import userManager from './userManager';

class MainView extends React.Component {
  render() {
    const { user } = this.props;
    const name = user ? user.profile.name : "<unnamed>";
    return (
      <div>
        <h1>Welcome, {name}!</h1>
        <button onClick={this.onLogoutButtonClicked}>Logout</button>
        <h2>User info</h2>
        <pre>
        {JSON.stringify(user, null, 2)}
        </pre>
      </div>
    );
  }

  onLogoutButtonClicked = (event) => {
    event.preventDefault();
    userManager.removeUser();
  }
}

const mapStateToProps = (state) => ({
  user: state.oidc.user,
});

const mapDispatchToProps = null;

const MainPage = ReactRedux.connect(
  mapStateToProps, mapDispatchToProps)(MainView);

export default MainPage;
