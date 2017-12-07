import * as ReduxOidc from 'redux-oidc';

const location = window.location;
const proto = location.protocol;
const host = location.hostname;
const portSuffix = location.port ? `:${location.port}` : '';
const baseUrl = `${proto}//${host}${portSuffix}`;

const userManagerConfig = {
  authority: 'http://localhost:8000/openid',
  client_id: '332114',
  redirect_uri: `${baseUrl}/login-callback`,
  response_type: 'id_token token',
  scope: 'openid email profile',
  silent_redirect_uri: `${baseUrl}/login-silent-renew`,
  automaticSilentRenew: true,
  filterProtocolClaims: true,
  loadUserInfo: true,
};

const userManager = ReduxOidc.createUserManager(userManagerConfig);

export default userManager;
