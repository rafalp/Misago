import React from "react"
import Avatar from "../avatar"
import { FlexRow, FlexRowCol, FlexRowSection } from "../FlexRow"
import FollowButton from "./follow-button"
import MessageButton from "./message-button"
import ModerationOptions from "./moderation/nav"
import ProfileDataList from "./ProfileDataList"

const ProfileHeader = ({ profile, user, moderation, message, follow }) => (
  <div className="profile-header-card">
    <div className="profile-header-card-avatar">
      <Avatar user={profile} size="400" />
    </div>
    <div className="profile-header-card-body">
      <h1>{profile.username}</h1>
      <ProfileDataList profile={profile} />
      {message && (
        <FlexRow>
          <FlexRowSection auto>
            <FlexRowCol>
              <MessageButton
                className="btn btn-default btn-block btn-outline"
                profile={profile}
                user={user}
              />
            </FlexRowCol>
            {moderation.available && !follow && (
              <FlexRowCol shrink>
                <div className="dropdown">
                  <ProfileModerationButton />
                  <ModerationOptions
                    profile={profile}
                    moderation={moderation}
                  />
                </div>
              </FlexRowCol>
            )}
          </FlexRowSection>
        </FlexRow>
      )}
      {follow && (
        <FlexRow>
          <FlexRowSection auto>
            <FlexRowCol>
              <FollowButton
                className="btn btn-block btn-outline"
                profile={profile}
              />
            </FlexRowCol>
            {moderation.available && (
              <FlexRowCol shrink>
                <div className="dropdown">
                  <ProfileModerationButton />
                  <ModerationOptions
                    profile={profile}
                    moderation={moderation}
                  />
                </div>
              </FlexRowCol>
            )}
          </FlexRowSection>
        </FlexRow>
      )}
      {moderation.available && !follow && !message && (
        <div className="dropdown">
          <button
            className="btn btn-default btn-block btn-outline dropdown-toggle"
            type="button"
            data-toggle="dropdown"
            aria-haspopup="true"
            aria-expanded="false"
          >
            <span className="material-icon">settings</span>
            {gettext("Options")}
          </button>
          <ModerationOptions profile={profile} moderation={moderation} />
        </div>
      )}
    </div>
  </div>
)

const ProfileModerationButton = () => (
  <button
    className="btn btn-default btn-icon btn-outline dropdown-toggle"
    type="button"
    title={gettext("Options")}
    data-toggle="dropdown"
    aria-haspopup="true"
    aria-expanded="false"
  >
    <span className="material-icon">settings</span>
  </button>
)

export default ProfileHeader
