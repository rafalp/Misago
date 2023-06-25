import React from "react"
import Avatar from "../avatar"
import { FlexRow, FlexRowCol, FlexRowSection } from "../FlexRow"
import {
  PageHeader,
  PageHeaderBanner,
  PageHeaderContainer,
  PageHeaderDetails,
} from "../PageHeader"
import FollowButton from "./follow-button"
import MessageButton from "./message-button"
import ModerationOptions from "./moderation/nav"
import ProfileDataList from "./ProfileDataList"

const ProfileHeader = ({ profile, user, moderation, message, follow }) => (
  <PageHeaderContainer>
    <PageHeader
      styleName={
        profile.rank.css_class ? "rank-" + profile.rank.css_class : "profile"
      }
    >
      <PageHeaderBanner
        styleName={
          profile.rank.css_class ? "rank-" + profile.rank.css_class : "profile"
        }
      >
        <div className="profile-page-header">
          <div className="profile-page-header-avatar">
            <Avatar
              className="user-avatar hidden-sm hidden-md hidden-lg"
              user={profile}
              size={200}
              size2x={400}
            />
            <Avatar
              className="user-avatar hidden-xs hidden-md hidden-lg"
              user={profile}
              size={64}
              size2x={128}
            />
            <Avatar
              className="user-avatar hidden-xs hidden-sm"
              user={profile}
              size={128}
              size2x={256}
            />
          </div>
          <h1>{profile.username}</h1>
        </div>
      </PageHeaderBanner>
      <PageHeaderDetails className="profile-page-header-details">
        <FlexRow>
          <FlexRowSection auto>
            <FlexRowCol>
              <ProfileDataList profile={profile} />
            </FlexRowCol>
          </FlexRowSection>
          {message && (
            <FlexRowSection>
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
          )}
          {follow && (
            <FlexRowSection>
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
          )}
          {moderation.available && !follow && !message && (
            <FlexRowSection>
              <FlexRowCol className="hidden-xs" shrink>
                <div className="dropdown">
                  <ProfileModerationButton />
                  <ModerationOptions
                    profile={profile}
                    moderation={moderation}
                  />
                </div>
              </FlexRowCol>
              <FlexRowCol className="hidden-sm hidden-md hidden-lg">
                <div className="dropdown">
                  <button
                    className="btn btn-default btn-block btn-outline dropdown-toggle"
                    type="button"
                    data-toggle="dropdown"
                    aria-haspopup="true"
                    aria-expanded="false"
                  >
                    <span className="material-icon">settings</span>
                    {pgettext("profile options btn", "Options")}
                  </button>
                  <ModerationOptions
                    profile={profile}
                    moderation={moderation}
                  />
                </div>
              </FlexRowCol>
            </FlexRowSection>
          )}
        </FlexRow>
      </PageHeaderDetails>
    </PageHeader>
  </PageHeaderContainer>
)

const ProfileModerationButton = () => (
  <button
    className="btn btn-default btn-icon btn-outline dropdown-toggle"
    type="button"
    title={pgettext("profile options btn", "Options")}
    data-toggle="dropdown"
    aria-haspopup="true"
    aria-expanded="false"
  >
    <span className="material-icon">settings</span>
  </button>
)

export default ProfileHeader
