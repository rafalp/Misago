import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom';

export default function(Component, containerId) {
  let container = document.getElementById(containerId);

  if (container) {
    ReactDOM.render(
      /* jshint ignore:start */
      <Component/>,
      /* jshint ignore:end */
      container
    );
  }
}
