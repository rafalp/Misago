import React from "react"
import Avatar from "../../avatar"
import { FlexRow, FlexRowCol, FlexRowSection } from "../../FlexRow"
import ThreadFlags from "../../ThreadFlags"
import { PageHeader, PageHeaderBanner, PageHeaderContainer, PageHeaderDetails } from "../../PageHeader"
import ThreadSubscriptionButton from "../ThreadSubscriptionButton"
import ThreadHeaderBreadcrumbs from "./ThreadHeaderBreadcrumbs"

const ThreadHeader = ({ thread, user }) => (
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
              {thread.starter ? (
                <a href={thread.url.starter}>
                  <Avatar size={32} user={thread.starter} />
                </a>
              ) : <Avatar size={32} />}
            </FlexRowCol>
            <FlexRowCol>
              {thread.starter ? (
                <a href={thread.url.starter}>
                  {thread.starter.username}
                </a>
              ) : thread.starter_name}
            </FlexRowCol>
            <FlexRowCol shrink>
              <ThreadFlags thread={thread} />
            </FlexRowCol>
          </FlexRowSection>
          {user.is_authenticated && (
            <FlexRowSection>
              <FlexRowCol>
                <ThreadSubscriptionButton thread={thread} />
              </FlexRowCol>
              <FlexRowCol shrink>[MOD]</FlexRowCol>
            </FlexRowSection>
          )}
        </FlexRow>
      </PageHeaderDetails>
    </PageHeader>
  </PageHeaderContainer>
)

export default ThreadHeader