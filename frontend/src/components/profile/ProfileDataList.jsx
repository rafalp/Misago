import React from "react"
import Status, { StatusIcon, StatusLabel } from "../user-status"

const ProfileDataList = ({ profile }) => (
  <ul className="profile-data-list">
    <li className="user-status-display">
      <Status user={profile} status={profile.status}>
        <StatusIcon user={profile} status={profile.status} />
        <StatusLabel
          user={profile}
          status={profile.status}
          className="status-label"
        />
      </Status>
    </li>
    {profile.rank.is_tab ? (
      <li className="user-rank">
        <a href={profile.rank.url} className="item-title">
          {profile.rank.name}
        </a>
      </li>
    ) : (
      <li className="user-rank">
        <span className="item-title">{profile.rank.name}</span>
      </li>
    )}
    {(profile.title || profile.rank.title) && (
      <li className="user-title">{profile.title || profile.rank.title}</li>
    )}
    <li className="user-joined-on">
      <abbr
        title={interpolate(
          gettext("Joined on %(joined_on)s"),
          {
            joined_on: profile.joined_on.format("LL, LT"),
          },
          true
        )}
      >
        {interpolate(
          gettext("Joined %(joined_on)s"),
          {
            joined_on: profile.joined_on.fromNow(),
          },
          true
        )}
      </abbr>
    </li>
    {profile.email && (
      <li className="user-email">
        <a href={"mailto:" + profile.email} className="item-title">
          {profile.email}
        </a>
      </li>
    )}
  </ul>
)

export default ProfileDataList
