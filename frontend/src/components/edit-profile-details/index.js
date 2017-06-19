/* jshint ignore:start */
import React from 'react';
import Loader from './loader';
import Form from './form';
import ajax from 'misago/services/ajax';
import snackbar from 'misago/services/snackbar';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      loading: true,
      groups: null
    };
  }

  componentDidMount() {
    ajax.get(this.props.api).then(
      (groups) => {
        this.setState({
          loading: false,

          groups
        });
      },
      (rejection) => {
        snackbar.apiError(rejection);
        if (this.props.cancel) {
          this.props.cancel();
        }
      }
    );
  }

  render() {
    return (
      <div className="panel panel-default panel-form">
        <div className="panel-heading">
          <h3 className="panel-title">
            {gettext("Edit profile details")}
          </h3>
        </div>
        <Loader display={this.state.loading} />
        <FormDisplay
          api={this.props.api}
          groups={this.state.groups}
          display={!this.state.loading}
          onCancel={this.props.onCancel}
        />
      </div>
    );
  }
}

export function FormDisplay({ api, groups, display, onCancel }) {
  if (!display) return null;

  return (
    <Form
      api={api}
      groups={groups}
      onCancel={onCancel}
    />
  );
}