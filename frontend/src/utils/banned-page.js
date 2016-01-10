import moment from 'moment'; // jshint ignore:line
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom';
import { Provider, connect } from 'react-redux'; // jshint ignore:line
import BannedPage from 'misago/components/banned-page'; // jshint ignore:line
import misago from 'misago/index';
import store from 'misago/services/store'; // jshint ignore:line

/* jshint ignore:start */
let select = function(state) {
  return state.tick;
};

let RedrawedBannedPage = connect(select)(BannedPage);
/* jshint ignore:end */

export default function(ban, changeState) {
  ReactDOM.unmountComponentAtNode(document.getElementById('page-mount'));

  ReactDOM.render(
    /* jshint ignore:start */
    <Provider store={store.getStore()}>
      <RedrawedBannedPage message={ban.message}
                          expires={ban.expires_on ? moment(ban.expires_on) : null} />
    </Provider>,
    /* jshint ignore:end */
    document.getElementById('page-mount')
  );

  if (typeof changeState === 'undefined' || changeState) {
    let forumName = misago.get('SETTINGS').forum_name;
    document.title = gettext("You are banned") + ' | ' + forumName;
    window.history.pushState({}, "", misago.get('BANNED_URL'));
  }
}