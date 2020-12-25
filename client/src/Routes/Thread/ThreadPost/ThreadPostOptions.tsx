import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary } from "../../../UI/Button"
import { Dropdown, DropdownButton } from "../../../UI/Dropdown"
import { ModerationAction, Post } from "../Thread.types"
import { useThreadReplyContext } from "../ThreadReply"
import ThreadPostPermalink from "./ThreadPostPermalink"

interface ThreadPostOptionsProps {
  acl: { edit: boolean }
  post: Post
  threadId: string
  threadSlug: string
  moderation: {
    actions: Array<ModerationAction>
  } | null
}

const ThreadPostOptions: React.FC<ThreadPostOptionsProps> = ({
  acl,
  post,
  threadId,
  threadSlug,
  moderation,
}) => {
  const context = useThreadReplyContext()

  return (
    <Dropdown
      toggle={({ ref, toggle }) => (
        <ButtonSecondary
          elementRef={ref}
          icon="fas fa-ellipsis-h"
          small
          onClick={toggle}
        />
      )}
      menu={() => (
        <>
          <ThreadPostPermalink
            post={post}
            threadId={threadId}
            threadSlug={threadSlug}
          />
          {acl.edit && (
            <DropdownButton
              text={<Trans id="post.edit">Edit</Trans>}
              icon="fas fa-edit"
              onClick={() => {
                if (context) context.editReply(post)
              }}
            />
          )}
          {moderation &&
            moderation.actions.map((action) => (
              <DropdownButton
                key={action.icon}
                text={action.name}
                icon={action.icon}
                disabled={action.disabled}
                onClick={action.action}
              />
            ))}
        </>
      )}
    />
  )
}

export default ThreadPostOptions
