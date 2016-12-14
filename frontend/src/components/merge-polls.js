// jshint ignore:start
import React from 'react';
import Button from './button';
import Form from './form';
import FormGroup from './form-group';
import ajax from 'misago/services/ajax';
import modal from 'misago/services/modal';

export default class extends Form {
  constructor(props) {
    super(props);

    this.state = {
      isLoading: false,

      poll: 0,
    };
  }

  clean() {
    const confirmation = confirm(gettext("Are you sure? This will delete other polls."));
    return confirmation
  }

  send() {
    const data = Object.assign({}, this.props.data, {
      poll: this.state.poll
    });

    return ajax.post(this.props.api, data);
  }

  handleSuccess = (success) => {
    this.props.onSuccess(success);
    modal.hide();
  };

  handleError = (rejection) => {
    this.props.onError(rejection);
  };

  onPollChange = (event) => {
    this.changeValue('poll', event.target.value);
  };

  render() {
    return (
      <div className="modal-dialog" role="document">
        <div className="modal-content">
          <div className="modal-header">
            <button
              aria-label={gettext("Close")}
              className="close"
              data-dismiss="modal"
              type="button"
            >
              <span aria-hidden="true">&times;</span>
            </button>
            <h4 className="modal-title">{gettext("Merge polls")}</h4>
          </div>
          <form onSubmit={this.handleSubmit}>
            <div className="modal-body">
              <p>{gettext("Select poll to use in merged thread. Other polls will be deleted.")}</p>
              <FormGroup
                label={gettext("Poll")}
                for="id_poll"
              >
                <select
                  className="form-control"
                  id="id_poll"
                  onChange={this.onPollChange}
                  value={this.state.poll}
                >
                  {this.props.polls.map((poll) => {
                    return (
                      <option value={poll[0]} key={poll[0]}>
                        {poll[1]}
                      </option>
                    );
                  })}
                </select>
              </FormGroup>
            </div>
            <div className="modal-footer">
              <Button className="btn-primary" loading={this.state.isLoading}>
                {gettext("Merge polls")}
              </Button>
            </div>
          </form>
        </div>
      </div>
    );
  }
}