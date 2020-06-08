import { Trans } from "@lingui/macro"
import React from "react"
import ThreadsModerationModal from "../ThreadsModerationModal"
import { ThreadsModerationModalAction } from "../ThreadsModerationModalContext"
import ThreadsModerationModalMoveForm from "./ThreadsModerationModalMoveForm"

const ThreadsModerationModalMove: React.FC = () => (
  <ThreadsModerationModal
    action={ThreadsModerationModalAction.MOVE}
    title={<Trans id="moderation.move_threads">Move threads</Trans>}
  >
    {({ data: { threads }, close }) => {
      return <ThreadsModerationModalMoveForm threads={threads} close={close} />
    }}
  </ThreadsModerationModal>
)

export default ThreadsModerationModalMove
