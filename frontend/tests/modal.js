import assert from 'assert';
import React from 'react'; // jshint ignore:line
import store from 'misago/services/store';
import { Modal } from 'misago/services/modal';
import * as testUtils from 'misago/utils/test-utils';

var modal = null;

class TestModalA extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="modal-dialog modal-a">
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 className="modal-title">Modal A</h4>
        </div>
        <div className="modal-body">
          <p>This is first test modal!</p>
        </div>
        <div className="modal-footer">
          <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

class TestModalB extends React.Component {
  render() {
    /* jshint ignore:start */
    return <div className="modal-dialog modal-b">
      <div className="modal-content">
        <div className="modal-header">
          <button type="button" className="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button>
          <h4 className="modal-title">Modal B</h4>
        </div>
        <div className="modal-body">
          <p>This is second test modal!</p>
        </div>
        <div className="modal-footer">
          <button type="button" className="btn btn-default" data-dismiss="modal">Close</button>
        </div>
      </div>
    </div>;
    /* jshint ignore:end */
  }
}

describe("Modal", function() {
  beforeEach(function() {
    modal = new Modal();
    modal.init(document.getElementById('modal-mount'));

    testUtils.initEmptyStore(store);
  });

  afterEach(function() {
    testUtils.emptyTestContainers();
  });

  it('shows component', function(done) {
    modal.show(TestModalA);

    window.setTimeout(function() {
      let element = $('#modal-mount .modal-a');
      assert.ok(element.length, "component was rendered");
      done();
    }, 400);
  });

  it('shows and cycles component', function(done) {
    modal.show(TestModalA);

    window.setTimeout(function() {
      let element = $('#modal-mount .modal-a');
      assert.ok(element.length, "component was rendered");

      modal.show(TestModalB);

      window.setTimeout(function() {
        let element = $('#modal-mount .modal-b');
        assert.ok(element.length, "component was toggled");
        done();
      }, 200);
    }, 400);
  });

  it('hides component', function(done) {
    modal.show(TestModalA);

    window.setTimeout(function() {
      let element = $('#modal-mount .modal-a');
      assert.ok(element.length, "component was rendered");
      modal.hide();

      let wait = function() {
        if($('#modal-mount').children().length === 0) {
          assert.ok(true, "modal was emptied");
          done();
        } else {
          window.setTimeout(wait, 100);
        }
      };
      wait();
    }, 400);
  });
});
