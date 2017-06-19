/* jshint ignore:start */
import React from 'react';
import Form from './form';
import GroupsList from './groups-list';
import Header from './header';
import ProfileDetailsData from 'misago/data/profile-details';
import title from 'misago/services/page-title';

export default class extends React.Component {
  constructor(props) {
    super(props);

    this.state = {
      editing: false
    };
  }

  componentDidMount() {
    title.set({
      title: gettext("Details"),
      parent: this.props.profile.username
    });
  }

  onEdit = () => {
    this.setState({ editing: true });
  };

  onCancel = () => {
    this.setState({ editing: false });
  };

  render() {
    const { dispatch, isAuthenticated, profile, profileDetails } = this.props;
    const loading = profileDetails.id !== profile.id;

    return (
      <ProfileDetailsData
        data={profileDetails}
        dispatch={dispatch}
        user={profile}
      >
        <div className="profile-details">
          <Header
            onEdit={this.onEdit}
            showEditButton={!!profileDetails.edit && !this.state.editing}
          />
          <GroupsList
            display={!this.state.editing}
            groups={profileDetails.groups}
            isAuthenticated={isAuthenticated}
            loading={loading}
            profile={profile}
          />
          <Form
            api={profile.api.change_details}
            onCancel={this.onCancel}
            dispatch={dispatch}
            display={this.state.editing}
          />
        </div>
      </ProfileDetailsData>
    );
  }
}