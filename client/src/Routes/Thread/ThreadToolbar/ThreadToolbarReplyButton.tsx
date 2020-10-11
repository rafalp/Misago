import { Trans } from "@lingui/macro"
import React from "react"
import { useAuthContext } from "../../../Context"
import { ButtonPrimary, ButtonSecondary } from "../../../UI/Button"
import { useThreadReplyContext } from "../ThreadReply"

interface IThreadToolbarReplyButtonProps {
  isClosed?: boolean
}

const ThreadToolbarReplyButton: React.FC<IThreadToolbarReplyButtonProps> = ({
  isClosed,
}) => {
  const { startReply } = useThreadReplyContext() || {}
  const user = useAuthContext()
  const isModerator = user && user.isModerator

  return !isClosed || isModerator ? (
    <ButtonPrimary
      text={<Trans id="thread.new_reply">Reply</Trans>}
      icon="fas fa-edit"
      responsive
      onClick={startReply}
    />
  ) : (
    <ButtonSecondary
      text={<Trans id="thread.closed">Closed</Trans>}
      icon="fas fa-lock"
      disabled
      responsive
    />
  )
}

export default ThreadToolbarReplyButton
