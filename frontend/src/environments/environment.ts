/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://localhost:5000', // the running FLASK api server url
  auth0: {
    url: 'dev-p5iqfqz0', // the auth0 domain prefix
    audience: 'https://localhost:5000', // the audience set for the auth0 app
    clientId: 'ksaxfz8ctP2TMZzdSDAlhzkTxTd9hK4F', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:4200', // the base url of the running ionic application
  }
};
