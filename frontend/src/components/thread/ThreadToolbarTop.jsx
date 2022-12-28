import React from "react"
import { Toolbar, ToolbarItem, ToolbarSection, ToolbarSpacer } from "../Toolbar"
import ThreadPagination from "./ThreadPagination"
import ThreadPollButton from "./ThreadPollButton"
import ThreadPostsModeration from "./ThreadPostsModeration"
import ThreadReplyButton from "./ThreadReplyButton"
import ThreadShortcutsButton from "./ThreadShortcutsButton"
import ThreadSubscriptionButton from "./ThreadSubscriptionButton"

const ThreadToolbarTop = ({
  thread,
  posts,
  user,
  selection,
  moderation,
  onPoll,
  onReply,
}) => (
  <Toolbar>
    <ToolbarSection className="hidden-xs">
      <ToolbarItem>
        <ThreadShortcutsButton thread={thread} user={user} />
      </ToolbarItem>
      <ToolbarItem className="hidden-xs hidden-sm">
        <ThreadPagination baseUrl={thread.url.index} posts={posts} />
      </ToolbarItem>
    </ToolbarSection>
    <ToolbarSpacer />
    {user.is_authenticated && (
      <ToolbarSection>
        <ToolbarItem>
          <ThreadSubscriptionButton thread={thread} />
        </ToolbarItem>
      </ToolbarSection>
    )}
    {thread.acl.can_start_poll && !thread.poll && (
      <ToolbarSection className="hidden-xs">
        <ToolbarItem>
          <ThreadPollButton onClick={onPoll} />
        </ToolbarItem>
      </ToolbarSection>
    )}
    {thread.acl.can_reply ? (
      <ToolbarSection>
        <ToolbarItem className="hidden-sm hidden-md hidden-lg" shrink>
          <ThreadShortcutsButton thread={thread} user={user} />
        </ToolbarItem>
        <ToolbarItem>
          <ThreadReplyButton onClick={onReply} />
        </ToolbarItem>
        {thread.acl.can_start_poll && !thread.poll && (
          <ToolbarItem className="hidden-sm hidden-md hidden-lg" shrink>
            <ThreadPollButton onClick={onPoll} compact />
          </ToolbarItem>
        )}
        {moderation.enabled && (
          <ToolbarItem className="hidden-xs" shrink>
            <ThreadPostsModeration
              thread={thread}
              user={user}
              selection={selection}
            />
          </ToolbarItem>
        )}
      </ToolbarSection>
    ) : (
      <ToolbarSection>
        <ToolbarItem className="hidden-sm hidden-md hidden-lg" shrink>
          <ThreadShortcutsButton thread={thread} user={user} />
        </ToolbarItem>
        {thread.acl.can_start_poll && !thread.poll && (
          <ToolbarItem>
            <ThreadPollButton onClick={onPoll} />
          </ToolbarItem>
        )}
        {moderation.enabled && (
          <ToolbarItem shrink>
            <ThreadPostsModeration
              thread={thread}
              user={user}
              selection={selection}
            />
          </ToolbarItem>
        )}
      </ToolbarSection>
    )}
  </Toolbar>
)

export default ThreadToolbarTop
