import assert from 'assert';
import moment from 'moment'; // jshint ignore:line
import React from 'react'; // jshint ignore:line
import ReactDOM from 'react-dom'; // jshint ignore:line
import BannedPage from 'misago/components/banned-page'; // jshint ignore:line

describe("Banned page", function() {
  afterEach(function() {
    window.emptyTestContainers();
  });

  it('renders', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <BannedPage message={{html: '<p>Lorem ipsum!</p>'}} expires={null} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    assert.equal(
      $('#test-mount .page-error-banned .lead p').text().trim(),
      "Lorem ipsum!",
      "component renders with html ban message");
  });

  it('renders with fallback message', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <BannedPage message={{plain: 'Lorem ipsum plain!'}} expires={null} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    assert.equal(
      $('#test-mount .page-error-banned p.lead').text().trim(),
      "Lorem ipsum plain!",
      "component renders with plaintext ban message");
  });

  it('renders with permanent expiration date', function() {
    /* jshint ignore:start */
    ReactDOM.render(
      <BannedPage message={{plain: 'Lorem ipsum plain!'}} expires={null} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    assert.equal(
      $('#test-mount .page-error-banned p.message-footnote').text().trim(),
      "This ban is permanent.",
      "component renders with perma ban expiration");
  });

  it('renders with future expiration date', function() {
    /* jshint ignore:start */
    let expires = moment().add(7, 'days');
    ReactDOM.render(
      <BannedPage message={{plain: 'Lorem ipsum plain!'}} expires={expires} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    assert.equal(
      $('#test-mount .page-error-banned p.message-footnote').text().trim(),
      "This ban expires in 7 days.",
      "component renders with past ban expiration");
  });

  it('renders with past expiration date', function() {
    /* jshint ignore:start */
    let expires = moment().subtract(7, 'days');
    ReactDOM.render(
      <BannedPage message={{plain: 'Lorem ipsum plain!'}} expires={expires} />,
      document.getElementById('test-mount')
    );
    /* jshint ignore:end */

    assert.equal(
      $('#test-mount .page-error-banned p.message-footnote').text().trim(),
      "This ban has expired.",
      "component renders with past ban expiration");
  });
});
