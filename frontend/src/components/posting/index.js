import React from 'react'; //jshint ignore:line
import Form from 'misago/components/form';
import Loading from './loading'; //jshint ignore:line
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
    console.log(rejection);
  };
  /* jshint ignore:end */

  render() {
    /* jshint ignore:start */
    if (this.state.isReady) {
      return (
        <div className="container">
          <p className="lead">Posting action has started!</p>
        </div>
      );
    } else if (this.state.isErrored) {
      return (
        <div className="container">
          <p className="lead">Posting action has errored!</p>
        </div>
      );
    } else {
      return (
        <Loading />
      );
    }
    /* jshint ignore:end */
  }
}
