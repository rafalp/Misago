import React from 'react'; //jshint ignore:line
import Editor from 'misago/components/editor'; //jshint ignore:line
import Form from 'misago/components/form';
import Container from './container'; //jshint ignore:line
import Loader from './loader'; //jshint ignore:line
import Message from './message'; //jshint ignore:line
import ajax from 'misago/services/ajax';
import posting from 'misago/services/posting'; //jshint ignore:line
import * as validators from 'misago/utils/validators'; //jshint ignore:line

export default class extends Form {
    constructor(props) {
    super(props);

    const initial = props.options.initial || {};
    const validators = {};

    if (props.options.mode === 'START_THREAD') {
      validators.title = [];
    }

    this.state = {
      isReady: false,
      isLoading: false,
      isErrored: false,

      title: initial.title || '',
      category: initial.category || null,
      categories: [],
      message: initial.message || '',
      pin: initial.pin || 0,
      close: initial.close || false,

      validators: validators,
      errors: {}
    };
  }

  componentDidMount() {
    ajax.get(this.props.options.url).then(this.loadSuccess, this.loadError);
  }

  /* jshint ignore:start */
  loadSuccess = (data) => {
    this.setState({
      isReady: true,
      categories: data
    });
  };

  loadError = (rejection) => {
    this.setState({
      isErrored: rejection.detail
    });
  };

  onClose = () => {
    const close = confirm(gettext("Are you sure you want to discard your message?"));
    if (close) {
      posting.close();
    }
  };
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    if (this.state.isReady) {
      return (
        <Container className="posting-form">
          <div className="row first-row">
            <div className="col-md-6">
              <input className="form-control" type="text" placeholder={gettext("Thread title")} />
            </div>
            <div className="col-md-4">
              <input className="form-control" type="text" placeholder={gettext("Category")} />
            </div>
            <div className="col-md-2">
              <button type="button" className="btn btn-default">
                <span className="material-icon">bookmark</span>
              </button>
              <button type="button" className="btn btn-default">
                <span className="material-icon">visibility_off</span>
              </button>
              <button type="button" className="btn btn-default">
                <span className="material-icon">lock_outline</span>
              </button>
            </div>
          </div>
          <div className="row">
            <div className="col-md-12">

              <Editor
                onClose={this.onClose}
                submitLabel={gettext("Post thread")}
              />

            </div>
          </div>
        </Container>
      );
    } else if (this.state.isErrored) {
      return (
        <Message message={this.state.isErrored} />
      );
    } else {
      return (
        <Loader />
      );
    }
    /* jshint ignore:end */
  }
}
