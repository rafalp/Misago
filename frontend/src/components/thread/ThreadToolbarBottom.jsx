import React from "react"
import { Toolbar, ToolbarItem, ToolbarSection, ToolbarSpacer } from "../Toolbar"
import ThreadPaginator from "./ThreadPaginator"
import ThreadPostsModeration from "./ThreadPostsModeration"
import ThreadReplyButton from "./ThreadReplyButton"
import ThreadWatchButton from "./ThreadWatchButton"

const ThreadToolbarBottom = ({
  thread,
  posts,
  user,
  selection,
  moderation,
  onReply,
}) => (
  <Toolbar>
    {posts.pages > 1 && (
      <ToolbarSection>
        <ToolbarItem>
          <ThreadPaginator
            baseUrl={thread.url.index}
            posts={posts}
            scrollToTop
          />
        </ToolbarItem>
      </ToolbarSection>
    )}
    <ToolbarSpacer />
    {user.is_authenticated && (
      <ToolbarSection>
        <ToolbarItem className="hidden-xs">
          <ThreadWatchButton thread={thread} dropup />
        </ToolbarItem>
        {thread.acl.can_reply && (
          <ToolbarItem>
            <ThreadReplyButton onClick={onReply} />
          </ToolbarItem>
        )}
        {moderation.enabled && (
          <ToolbarItem shrink>
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
    {user.is_authenticated && (
      <ToolbarSection className="hidden-sm hidden-md hidden-lg">
        <ToolbarItem>
          <ThreadWatchButton thread={thread} dropup />
        </ToolbarItem>
      </ToolbarSection>
    )}
  </Toolbar>
)

export default ThreadToolbarBottom
