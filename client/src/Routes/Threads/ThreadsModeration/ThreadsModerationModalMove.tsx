import { Trans } from "@lingui/macro"
import React from "react"
import { ModalBody } from "../../../UI"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"

const ThreadsModerationModalMove: React.FC = () => (
  <ThreadsModerationModal
    action={ThreadsModerationModalAction.MOVE}
    title={<Trans>Move threads</Trans>}
  >
    {({ threads }) => (
      <ModalBody>
        <ul>
          {threads.map((thread) => (
            <li key={thread.id}>{thread.title}</li>
          ))}
        </ul>
      </ModalBody>
    )}
  </ThreadsModerationModal>
)

export default ThreadsModerationModalMove
