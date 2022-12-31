import React from "react"
import { FlexRow, FlexRowCol, FlexRowSection } from "../../FlexRow"
import ThreadFlags from "../../ThreadFlags"
import ThreadReplies from "../../ThreadReplies"
import ThreadStarterCard from "../../ThreadStarterCard"
import {
  PageHeader,
  PageHeaderBanner,
  PageHeaderContainer,
  PageHeaderDetails,
} from "../../PageHeader"
import ThreadModeration from "../ThreadModeration"
import ThreadSubscriptionButton from "../ThreadSubscriptionButton"
import ThreadHeaderBreadcrumbs from "./ThreadHeaderBreadcrumbs"

const ThreadHeader = ({ thread, posts, user, moderation }) => (
  <PageHeaderContainer>
    <PageHeader>
      <PageHeaderBanner>
        <ThreadHeaderBreadcrumbs breadcrumbs={thread.path} />
        <h1>{thread.title}</h1>
      </PageHeaderBanner>
      <PageHeaderDetails>
        <FlexRow>
          <FlexRowSection auto>
            <FlexRowCol shrink>
              <ThreadStarterCard thread={thread} />
            </FlexRowCol>
            <FlexRowCol auto />
            {thread.replies > 0 && (
              <FlexRowCol shrink>
                <ThreadReplies thread={thread} />
              </FlexRowCol>
            )}
            <FlexRowCol shrink>
              <ThreadFlags thread={thread} />
            </FlexRowCol>
          </FlexRowSection>
          {user.is_authenticated && (
            <FlexRowSection>
              <FlexRowCol>
                <ThreadSubscriptionButton thread={thread} />
              </FlexRowCol>
              {moderation.enabled && (
                <FlexRowCol shrink>
                  <ThreadModeration
                    thread={thread}
                    posts={posts}
                    moderation={moderation}
                  />
                </FlexRowCol>
              )}
            </FlexRowSection>
          )}
        </FlexRow>
      </PageHeaderDetails>
    </PageHeader>
  </PageHeaderContainer>
)

export default ThreadHeader
