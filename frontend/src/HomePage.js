import * as React from 'react';
import * as ReactRedux from 'react-redux';

import LoginPage from './LoginPage';
import MainPage from './MainPage';

class HomeView extends React.Component {
  render() {
    const { user } = this.props;
    const loggedIn = (user && !user.expired);
    return (loggedIn) ? <MainPage/> : <LoginPage/>;
  }
}

const mapStateToProps = (state) => ({
  user: state.oidc.user
});

const mapDispatchToProps = null;

const HomePage = ReactRedux.connect(
  mapStateToProps, mapDispatchToProps)(HomeView);

export default HomePage;
