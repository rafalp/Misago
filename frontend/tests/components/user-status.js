import assert from 'assert';
import moment from 'moment'; // jshint ignore:line
import React from 'react'; // jshint ignore:line
import UserStatus, { StatusIcon, StatusLabel } from 'misago/components/user-status'; // jshint ignore:line
import * as testUtils from 'misago/utils/test-utils';

let status = {
  is_hidden: false,
  is_online_hidden: false,
  is_offline_hidden: false,
  is_online: false,
  is_offline: false,
  last_click: moment().subtract(7, 'days'),

  is_banned: false,
  banned_until: moment().add(7, 'days')
};

/* jshint ignore:start */
let user = {
  username: 'Boberson'
};
/* jshint ignore:end */

describe("User Status", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders for offline user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_offline: true
    });

    testUtils.render(
      <UserStatus status={testStatus}>
        Some stuff
      </UserStatus>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .user-status');
    assert.ok(element.hasClass('user-offline'),
      "component renders with valid class");
    assert.equal(element.text().trim(), "Some stuff",
      "component renders its children");
  });

  it('renders for offline (hidden) user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_offline_hidden: true
    });

    testUtils.render(
      <UserStatus status={testStatus}>
        Some stuff
      </UserStatus>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .user-status');
    assert.ok(element.hasClass('user-offline'),
      "component renders with valid class");
    assert.equal(element.text().trim(), "Some stuff",
      "component renders its children");
  });

  it('renders for online user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_online: true
    });

    testUtils.render(
      <UserStatus status={testStatus}>
        Some stuff
      </UserStatus>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .user-status');
    assert.ok(element.hasClass('user-online'),
      "component renders with valid class");
    assert.equal(element.text().trim(), "Some stuff",
      "component renders its children");
  });

  it('renders for online (hidden) user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_online_hidden: true
    });

    testUtils.render(
      <UserStatus status={testStatus}>
        Some stuff
      </UserStatus>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .user-status');
    assert.ok(element.hasClass('user-online'),
      "component renders with valid class");
    assert.equal(element.text().trim(), "Some stuff",
      "component renders its children");
  });

  it('renders for hidden user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_hidden: true
    });

    testUtils.render(
      <UserStatus status={testStatus}>
        Some stuff
      </UserStatus>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .user-status');
    assert.ok(element.hasClass('user-offline'),
      "component renders with valid class");
    assert.equal(element.text().trim(), "Some stuff",
      "component renders its children");
  });

  it('renders for banned user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_banned: true
    });

    testUtils.render(
      <UserStatus status={testStatus}>
        Some stuff
      </UserStatus>
    );
    /* jshint ignore:end */

    let element = $('#test-mount .user-status');
    assert.ok(element.hasClass('user-banned'),
      "component renders with valid class");
    assert.equal(element.text().trim(), "Some stuff",
      "component renders its children");
  });
});

describe("User Status Icon", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders for offline user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_offline: true
    });

    testUtils.render(<StatusIcon status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-icon');
    assert.equal(element.text().trim(), 'panorama_fish_eye',
      "component renders with valid icon");
  });

  it('renders for offline (hidden) user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_offline_hidden: true
    });

    testUtils.render(<StatusIcon status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-icon');
    assert.equal(element.text().trim(), 'label_outline',
      "component renders with valid icon");
  });

  it('renders for online user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_online: true
    });

    testUtils.render(<StatusIcon status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-icon');
    assert.equal(element.text().trim(), 'lens',
      "component renders with valid icon");
  });

  it('renders for online (hidden) user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_online_hidden: true
    });

    testUtils.render(<StatusIcon status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-icon');
    assert.equal(element.text().trim(), 'label',
      "component renders with valid icon");
  });

  it('renders for hidden user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_hidden: true
    });

    testUtils.render(<StatusIcon status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-icon');
    assert.equal(element.text().trim(), 'help_outline',
      "component renders with valid icon");
  });

  it('renders for banned user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_banned: true
    });

    testUtils.render(<StatusIcon status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-icon');
    assert.equal(element.text().trim(), 'remove_circle_outline',
      "component renders with valid icon");
  });
});

describe("User Status Label", function() {
  afterEach(function() {
    testUtils.unmountComponents();
  });

  it('renders for offline user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_offline: true
    });

    testUtils.render(<StatusLabel user={user} status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-label');
    assert.equal(element.text().trim(), gettext("Offline"),
      "component renders with valid label");
    assert.equal(element.attr('title'),
      "Boberson was last seen " + status.last_click.fromNow(),
      "component renders with valid help");
  });

  it('renders for offline (hidden) user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_offline_hidden: true
    });

    testUtils.render(<StatusLabel user={user} status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-label');
    assert.equal(element.text().trim(), gettext("Offline (hidden)"),
      "component renders with valid label");
    assert.equal(element.attr('title'),
      "Boberson was last seen " + status.last_click.fromNow() + " (hidden)",
      "component renders with valid status.help");
  });

  it('renders for online user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_online: true
    });

    testUtils.render(<StatusLabel user={user} status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-label');
    assert.equal(element.text().trim(), gettext("Online"),
      "component renders with valid label");
    assert.equal(element.attr('title'), "Boberson is online",
      "component renders with valid help");
  });

  it('renders for online (hidden) user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_online_hidden: true
    });

    testUtils.render(<StatusLabel user={user} status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-label');
    assert.equal(element.text().trim(), gettext("Online (hidden)"),
      "component renders with valid label");
    assert.equal(element.attr('title'), "Boberson is online (hidden)",
      "component renders with valid help");
  });

  it('renders for hidden user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_hidden: true
    });

    testUtils.render(<StatusLabel user={user} status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-label');
    assert.equal(element.text().trim(), gettext("Hidden"),
      "component renders with valid label");
    assert.equal(element.attr('title'), "Boberson is hiding presence",
      "component renders with valid help");
  });

  it('renders for banned user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_banned: true
    });

    testUtils.render(<StatusLabel user={user} status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-label');
    assert.equal(element.text().trim(), gettext("Banned"),
      "component renders with valid label");
    assert.equal(element.attr('title'),
      "Boberson is banned until " + status.banned_until.format('LL, LT'),
      "component renders with valid help");
  });

  it('renders for permabanned user', function() {
    /* jshint ignore:start */
    let testStatus = Object.assign({}, status, {
      is_banned: true,
      banned_until: null
    });

    testUtils.render(<StatusLabel user={user} status={testStatus} />);
    /* jshint ignore:end */

    let element = $('#test-mount .status-label');
    assert.equal(element.text().trim(), gettext("Banned"),
      "component renders with valid label");
    assert.equal(element.attr('title'), "Boberson is banned",
      "component renders with valid help");
  });
});