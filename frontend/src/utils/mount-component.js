import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux'; // jshint ignore:line
import store from 'misago/services/store'; // jshint ignore:line

export default function(Component, rootElementId, connected=true) {
  let rootElement = document.getElementById(rootElementId);

  if (rootElement) {
    if (connected) {
      ReactDOM.render(
        /* jshint ignore:start */
        <Provider store={store.getStore()}>
          <Component />
        </Provider>,
        /* jshint ignore:end */
        rootElement
      );
    } else {
      ReactDOM.render(
        /* jshint ignore:start */
        <Component />,
        /* jshint ignore:end */
        rootElement
      );
    }
  }
}
