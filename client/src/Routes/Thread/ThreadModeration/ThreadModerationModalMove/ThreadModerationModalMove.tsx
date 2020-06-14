import { Trans } from "@lingui/macro"
import React from "react"
import ThreadModerationModal from "../ThreadModerationModal"
import { ThreadModerationModalAction } from "../ThreadModerationModalContext"
import ThreadModerationModalMoveForm from "./ThreadModerationModalMoveForm"

const ThreadModerationModalMove: React.FC = () => (
  <ThreadModerationModal
    action={ThreadModerationModalAction.MOVE}
    title={<Trans id="moderation.move_thread">Move thread</Trans>}
  >
    {({ data: { thread }, close }) => {
      return <ThreadModerationModalMoveForm thread={thread} close={close} />
    }}
  </ThreadModerationModal>
)

export default ThreadModerationModalMove
