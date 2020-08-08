import { Trans } from "@lingui/macro"
import React from "react"
import { ButtonSecondary, Dropdown, DropdownButton } from "../../../UI"
import { IPost } from "../Thread.types"

interface IThreadPostOptionsProps {
  acl: { edit: boolean }
  post: IPost
  editPost: () => void
}

const ThreadPostOptions: React.FC<IThreadPostOptionsProps> = ({
  acl,
  post,
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
          onClick={() => {}}
        />
        {acl.edit && (
          <DropdownButton
            text={<Trans id="post.edit">Edit</Trans>}
            onClick={editPost}
          />
        )}
      </>
    )}
  />
)

export default ThreadPostOptions
