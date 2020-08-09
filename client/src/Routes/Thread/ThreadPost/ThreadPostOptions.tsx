import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary, Dropdown, DropdownButton } from "../../../UI"
import { IModerationAction, IPost } from "../Thread.types"

interface IThreadPostOptionsProps {
  acl: { edit: boolean }
  post: IPost
  moderation: {
    actions: Array<IModerationAction>
  } | null
  editPost: () => void
}

const ThreadPostOptions: React.FC<IThreadPostOptionsProps> = ({
  acl,
  post,
  moderation,
  editPost,
}) => (
  <Dropdown
    toggle={({ ref, toggle }) => (
      <ButtonSecondary
        elementRef={ref}
        icon="ellipsis-h"
        iconSolid
        small
        onClick={toggle}
      />
    )}
    menu={() => (
      <>
        <DropdownButton
          text={<Trans id="post.permalink">Permalink</Trans>}
          icon="link"
          iconSolid
          onClick={() => {}}
        />
        {acl.edit && (
          <DropdownButton
            text={<Trans id="post.edit">Edit</Trans>}
            icon="edit"
            iconSolid
            onClick={editPost}
          />
        )}
        {moderation &&
          moderation.actions.map((action) => (
            <DropdownButton
              key={action.icon}
              text={action.name}
              icon={action.icon}
              iconSolid={action.iconSolid}
              disabled={action.disabled}
              onClick={action.action}
            />
          ))}
      </>
    )}
  />
)

export default ThreadPostOptions
