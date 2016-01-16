import assert from 'assert';
import React from 'react'; // jshint ignore:line
import PasswordStrength from 'misago/components/password-strength'; // jshint ignore:line
import zxcvbn from 'misago/services/zxcvbn';
import * as testUtils from 'misago/utils/test-utils';

describe("Password Strength", function() {
  afterEach(function() {
    testUtils.unmountComponents();
    delete window.zxcvbn;
  });

  it('renders very weak password', function(done) {
    window.zxcvbn = function(password, inputs) {
      assert.equal(password, 'very-weak', "valid password is passed to API");
      assert.deepEqual(inputs, ['a', 'b', 'c'],
        "valid password is passed to API");

      return {
        score: 0
      };
    };

    zxcvbn.init({
      include: function() {
        /* noop */
      }
    });
    zxcvbn.load();

    /* jshint ignore:start */
    testUtils.render(
      <PasswordStrength password="very-weak" inputs={['a', 'b', 'c']} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .password-strength');
    assert.ok(element.length, "component renders very weak password");

    window.setTimeout(function() {
      assert.ok(element.find('.progress-bar').hasClass('progress-bar-danger'),
        "progress bar has valid class");
      assert.equal(element.find('.sr-only').text().trim(),
        "Entered password is very weak.",
        "progress bar has valid sr-only label");
      assert.equal(element.find('p').text().trim(),
        "Entered password is very weak.",
        "progress bar has valid description");

      done();
    }, 200);
  });

  it('renders weak password', function(done) {
    window.zxcvbn = function(password, inputs) {
      assert.equal(password, 'weak', "valid password is passed to API");
      assert.deepEqual(inputs, ['a', 'b', 'c'],
        "valid password is passed to API");

      return {
        score: 1
      };
    };

    zxcvbn.init({
      include: function() {
        /* noop */
      }
    });
    zxcvbn.load();

    /* jshint ignore:start */
    testUtils.render(
      <PasswordStrength password="weak" inputs={['a', 'b', 'c']} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .password-strength');
    assert.ok(element.length, "component renders weak password");

    window.setTimeout(function() {
      assert.ok(element.find('.progress-bar').hasClass('progress-bar-warning'),
        "progress bar has valid class");
      assert.equal(element.find('.sr-only').text().trim(),
        "Entered password is weak.",
        "progress bar has valid sr-only label");
      assert.equal(element.find('p').text().trim(),
        "Entered password is weak.",
        "progress bar has valid description");

      done();
    }, 200);
  });

  it('renders average password', function(done) {
    window.zxcvbn = function(password, inputs) {
      assert.equal(password, 'average', "valid password is passed to API");
      assert.deepEqual(inputs, ['a', 'b', 'c'],
        "valid password is passed to API");

      return {
        score: 2
      };
    };

    zxcvbn.init({
      include: function() {
        /* noop */
      }
    });
    zxcvbn.load();

    /* jshint ignore:start */
    testUtils.render(
      <PasswordStrength password="average" inputs={['a', 'b', 'c']} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .password-strength');
    assert.ok(element.length, "component renders average password");

    window.setTimeout(function() {
      assert.ok(element.find('.progress-bar').hasClass('progress-bar-warning'),
        "progress bar has valid class");
      assert.equal(element.find('.sr-only').text().trim(),
        "Entered password is average.",
        "progress bar has valid sr-only label");
      assert.equal(element.find('p').text().trim(),
        "Entered password is average.",
        "progress bar has valid description");

      done();
    }, 200);
  });

  it('renders strong password', function(done) {
    window.zxcvbn = function(password, inputs) {
      assert.equal(password, 'stronk', "valid password is passed to API");
      assert.deepEqual(inputs, ['a', 'b', 'c'],
        "valid password is passed to API");

      return {
        score: 3
      };
    };

    zxcvbn.init({
      include: function() {
        /* noop */
      }
    });
    zxcvbn.load();

    /* jshint ignore:start */
    testUtils.render(
      <PasswordStrength password="stronk" inputs={['a', 'b', 'c']} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .password-strength');
    assert.ok(element.length, "component renders strong password");

    window.setTimeout(function() {
      assert.ok(element.find('.progress-bar').hasClass('progress-bar-primary'),
        "progress bar has valid class");
      assert.equal(element.find('.sr-only').text().trim(),
        "Entered password is strong.",
        "progress bar has valid sr-only label");
      assert.equal(element.find('p').text().trim(),
        "Entered password is strong.",
        "progress bar has valid description");

      done();
    }, 200);
  });

  it('renders very strong password', function(done) {
    window.zxcvbn = function(password, inputs) {
      assert.equal(password, 'very-stronk', "valid password is passed to API");
      assert.deepEqual(inputs, ['a', 'b', 'c'],
        "valid password is passed to API");

      return {
        score: 4
      };
    };

    zxcvbn.init({
      include: function() {
        /* noop */
      }
    });
    zxcvbn.load();

    /* jshint ignore:start */
    testUtils.render(
      <PasswordStrength password="very-stronk" inputs={['a', 'b', 'c']} />
    );
    /* jshint ignore:end */

    let element = $('#test-mount .password-strength');
    assert.ok(element.length, "component renders very strong password");

    window.setTimeout(function() {
      assert.ok(element.find('.progress-bar').hasClass('progress-bar-success'),
        "progress bar has valid class");
      assert.equal(element.find('.sr-only').text().trim(),
        "Entered password is very strong.",
        "progress bar has valid sr-only label");
      assert.equal(element.find('p').text().trim(),
        "Entered password is very strong.",
        "progress bar has valid description");

      done();
    }, 200);
  });
});