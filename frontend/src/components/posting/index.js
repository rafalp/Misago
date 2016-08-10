import React from 'react'; //jshint ignore:line
import Form from 'misago/components/form';
import Loader from './loader'; //jshint ignore:line
import Message from './message'; //jshint ignore:line
import Placeholder from './placeholder'; //jshint ignore:line
import ajax from 'misago/services/ajax';
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
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    if (this.state.isReady) {
      return (
        <div className="posting-form">

          <Placeholder />

          <div className="posting-overlay">
            <div className="posting-cover">
              <div className="posting-inner">

                <div className="container">
                  <p className="lead">TODO: posting form goes here</p>
                </div>
              </div>
            </div>
          </div>

        </div>
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
