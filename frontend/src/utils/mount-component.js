import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux'; // jshint ignore:line
import store from 'misago/services/store'; // jshint ignore:line

export default function(Component, rootElementId, connected=true) {
  let rootElement = document.getElementById(rootElementId);

  /* jshint ignore:start */
  let finalComponent = Component.props ? Component : <Component />;
  /* jshint ignore:end */

  if (rootElement) {
    if (connected) {
      ReactDOM.render(
        /* jshint ignore:start */
        <Provider store={store.getStore()}>
          {finalComponent}
        </Provider>,
        /* jshint ignore:end */
        rootElement
      );
    } else {
      /* jshint ignore:start */
      ReactDOM.render(finalComponent, rootElement);
      /* jshint ignore:end */
    }
  }
}
