import { Trans } from "@lingui/macro"
import React from "react"
import { ModalFormBody } from "../../../UI"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"

const ThreadsModerationModalOpen: React.FC = () => {
  return (
    <ThreadsModerationModal
      action={ThreadsModerationModalAction.OPEN}
      title={<Trans id="moderation.open_threads">Open threads</Trans>}
    >
      {({ data: { threads, graphqlError, errors }, close }) => {
        return (
          <ModalFormBody>
            {JSON.stringify(graphqlError)}
            {JSON.stringify(errors)}
          </ModalFormBody>
        )
      }}
    </ThreadsModerationModal>
  )
}

export default ThreadsModerationModalOpen
