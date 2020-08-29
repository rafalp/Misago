import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary, Dropdown, DropdownButton } from "../../../UI"
import { IModerationAction, IPost } from "../Thread.types"
import ThreadPostPermalink from "./ThreadPostPermalink"

interface IThreadPostOptionsProps {
  acl: { edit: boolean }
  post: IPost
  threadId: string
  threadSlug: string
  moderation: {
    actions: Array<IModerationAction>
  } | null
  editPost: () => void
}

const ThreadPostOptions: React.FC<IThreadPostOptionsProps> = ({
  acl,
  post,
  threadId,
  threadSlug,
  moderation,
  editPost,
}) => (
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
            onClick={editPost}
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

export default ThreadPostOptions
