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
import ThreadWatchButton from "../ThreadWatchButton"
import ThreadHeaderBreadcrumbs from "./ThreadHeaderBreadcrumbs"

const ThreadHeader = ({ styleName, thread, posts, user, moderation }) => (
  <PageHeaderContainer>
    <PageHeader styleName={styleName}>
      <PageHeaderBanner styleName={styleName}>
        <ThreadHeaderBreadcrumbs breadcrumbs={thread.path} />
        <h1>{thread.title}</h1>
      </PageHeaderBanner>
      <PageHeaderDetails className="page-header-thread-details">
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
            {hasFlags(thread) && (
              <FlexRowCol shrink>
                <ThreadFlags thread={thread} />
              </FlexRowCol>
            )}
          </FlexRowSection>
          {user.is_authenticated && (
            <FlexRowSection>
              <FlexRowCol>
                <ThreadWatchButton thread={thread} />
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

const hasFlags = (thread) => {
  return (
    thread.is_closed ||
    thread.is_hidden ||
    thread.is_unapproved ||
    thread.weight > 0 ||
    thread.best_answer ||
    thread.has_poll ||
    thread.has_unapproved_posts
  )
}

export default ThreadHeader
