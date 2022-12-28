import React from "react"
import { Toolbar, ToolbarItem, ToolbarSection, ToolbarSpacer } from "../Toolbar"
import ThreadPagination from "./ThreadPagination"
import ThreadReplyButton from "./ThreadReplyButton"
import ThreadSubscriptionButton from "./ThreadSubscriptionButton"

const ThreadToolbarBottom = ({ thread, posts, user, onReply }) => (
  <Toolbar>
    <ToolbarSection>
      <ToolbarItem>
        <ThreadPagination baseUrl={thread.url.index} posts={posts} />
      </ToolbarItem>
      <ToolbarItem className="hidden-sm hidden-md hidden-lg" shrink>
        [MOD]
      </ToolbarItem>
    </ToolbarSection>
    <ToolbarSpacer />
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
        <ToolbarItem className="hidden-xs" shrink>
          [MOD]
        </ToolbarItem>
      </ToolbarSection>
    )}
  </Toolbar>
)

export default ThreadToolbarBottom