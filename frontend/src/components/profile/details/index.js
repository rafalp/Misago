/* jshint ignore:start */
import React from 'react';
import GroupsList from './groups-list';
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

  onEditClick = () => {
    this.setState({ editing: true });
  };

  onCancelClick = () => {
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
          <GroupsList
            display={!this.state.editing}
            groups={profileDetails.groups}
            isAuthenticated={isAuthenticated}
            loading={loading}
            profile={profile}
          />
        </div>
      </ProfileDetailsData>
    );
  }
}