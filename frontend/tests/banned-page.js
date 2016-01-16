import assert from 'assert';
import moment from 'moment';
import misago from 'misago/index';
import store from 'misago/services/store'; // jshint ignore:line
import showBannedPage from 'misago/utils/banned-page';
import * as testUtils from 'misago/utils/test-utils';

let ban = {
  message: {
    plain: 'Lorem ipsum dolor met sit amet elit!',
    html: '<p>Lorem ipsum dolor met sit amet elit!</p>'
  },
  expires_on: moment().add(7, 'days')
};

describe('Show Banned Page', function() {
  beforeEach(function() {
    misago._context = {
      'SETTINGS': {
        'forum_name': 'Fake Forum'
      },
      'BANNED_URL': 'banned/'
    };

    /* jshint ignore:start */
    store.constructor();
    store.addReducer('tick', function(state={tick: 1}, action=null) {
      return {tick: 1};
    }, {});
    store.init();
    /* jshint ignore:end */
  });

  afterEach(function() {
    testUtils.emptyTestContainers();
  });

  it("renders banned page", function(done) {
    showBannedPage(ban, false);

    window.setTimeout(function() {
      assert.equal(
        $('#page-mount .page-error-banned .lead p').text().trim(),
        "Lorem ipsum dolor met sit amet elit!",
        "utility renders ban message");

      assert.equal(
        $('#page-mount .page-error-banned p.message-footnote').text().trim(),
        "This ban expires in 7 days.",
        "utility renders ban message expiration");

      done();
    }, 200);
  });

  it("changes context", function() {
    showBannedPage(ban, true);

    assert.equal(document.title, "You are banned | Fake Forum",
      "page title was changed");
    assert.equal(
      String(document.location.href).substr(-19), 'test-runner/banned/',
      "page location was changed.");
  });
});
