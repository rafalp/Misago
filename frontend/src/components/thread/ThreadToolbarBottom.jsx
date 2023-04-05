import React from "react"
import { Toolbar, ToolbarItem, ToolbarSection, ToolbarSpacer } from "../Toolbar"
import ThreadPagination from "./ThreadPagination"
import ThreadPostsLeft from "./ThreadPostsLeft"
import ThreadPostsModeration from "./ThreadPostsModeration"
import ThreadReplyButton from "./ThreadReplyButton"
import ThreadSubscriptionButton from "./ThreadSubscriptionButton"

const ThreadToolbarBottom = ({
  thread,
  posts,
  user,
  selection,
  moderation,
  onReply,
}) => (
  <Toolbar>
    <ToolbarSection>
      <ToolbarItem>
        <ThreadPagination
          baseUrl={thread.url.index}
          posts={posts}
          scrollToTop
        />
      </ToolbarItem>
      {moderation.enabled && (
        <ToolbarItem className="hidden-sm hidden-md hidden-lg" shrink>
          <ThreadPostsModeration
            thread={thread}
            user={user}
            selection={selection}
            dropup
          />
        </ToolbarItem>
      )}
    </ToolbarSection>
    <ToolbarSection className="hidden-xs hidden-sm" auto>
      <ToolbarItem>
        <ThreadPostsLeft posts={posts} />
      </ToolbarItem>
    </ToolbarSection>
    <ToolbarSpacer className="hidden-md hidden-lg" />
    {user.is_authenticated && (
      <ToolbarSection>
        <ToolbarItem>
          <ThreadSubscriptionButton thread={thread} />
        </ToolbarItem>
        {thread.acl.can_reply && (
          <ToolbarItem>
            <ThreadReplyButton onClick={onReply} />
          </ToolbarItem>
        )}
        {moderation.enabled && (
          <ToolbarItem className="hidden-xs" shrink>
            <ThreadPostsModeration
              thread={thread}
              user={user}
              selection={selection}
              dropup
            />
          </ToolbarItem>
        )}
      </ToolbarSection>
    )}
  </Toolbar>
)

export default ThreadToolbarBottom
