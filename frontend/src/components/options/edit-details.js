/* jshint ignore:start */
import React from 'react';
import Form from 'misago/components/edit-profile-details';
import title from 'misago/services/page-title';
import snackbar from 'misago/services/snackbar';

export default class extends React.Component {
  componentDidMount() {
    title.set({
      title: gettext("Edit profile details"),
      parent: gettext("Change your options")
    });
  }

  onSuccess = () => {
    snackbar.info(gettext("Your profile details have been updated."));
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