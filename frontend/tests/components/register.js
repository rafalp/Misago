import assert from 'assert';
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import misago from 'misago/index';
import { RegisterForm, RegisterComplete } from 'misago/components/register'; // jshint ignore:line
import modal from 'misago/services/modal';
import snackbar from 'misago/services/snackbar';

let snackbarStore = null;

describe("Register Complete", function() {
  afterEach(function() {
    window.emptyTestContainers();
  });

  it("renders user-activated message", function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <RegisterComplete activation="user"
                        username="Bob"
                        email="bob@boberson.com" />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount .modal-message');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('p').first().text().trim(),
      "Bob, your account has been created but you need to activate it before you will be able to sign in.",
      "component renders valid message");

    assert.equal(element.find('p').last().text().trim(),
      "We have sent an e-mail to bob@boberson.com with link that you have to click to activate your account.",
      "component renders valid activation instruction");
  });

  it("renders admin-activated message", function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <RegisterComplete activation="admin"
                        username="Bob"
                        email="bob@boberson.com" />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    let element = $('#test-mount .modal-message');
    assert.ok(element.length, "component renders");

    assert.equal(element.find('p').first().text().trim(),
      "Bob, your account has been created but board administrator will have to activate it before you will be able to sign in.",
      "component renders valid message");

    assert.equal(element.find('p').last().text().trim(),
      "We will send an e-mail to bob@boberson.com when this takes place.",
      "component renders valid activation instruction");
  });
});