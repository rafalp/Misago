import { Trans } from "@lingui/macro"
import React from "react"
import { ModalFormBody } from "../../../UI"
import ThreadsModerationModal from "./ThreadsModerationModal"
import { ThreadsModerationModalAction } from "./ThreadsModerationModalContext"

const ThreadsModerationModalClose: React.FC = () => {
  return (
    <ThreadsModerationModal
      action={ThreadsModerationModalAction.CLOSE}
      title={<Trans id="moderation.close_threads">Close threads</Trans>}
    >
      {({ data: { threads, graphqlError, errors }, close }) => {
        return (
          <ModalFormBody>
            {JSON.stringify(threads)}
            {JSON.stringify(graphqlError)}
            {JSON.stringify(errors)}
          </ModalFormBody>
        )
      }}
    </ThreadsModerationModal>
  )
}

export default ThreadsModerationModalClose
