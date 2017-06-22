/* jshint ignore:start */
import React from 'react';
import Form from 'misago/components/edit-details';
import title from 'misago/services/page-title';
import snackbar from 'misago/services/snackbar';

export default class extends React.Component {
  componentDidMount() {
    title.set({
      title: gettext("Edit details"),
      parent: gettext("Change your options")
    });
  }

  onSuccess = () => {
    snackbar.info(gettext("Your details have been updated."));
  };

  render() {
    return (
      <Form
        api={this.props.user.api.change_details}
        onSuccess={this.onSuccess}
      />
    );
  }
}