import { Trans } from "@lingui/macro"
import React from "react"
import ThreadModerationModal from "../ThreadModerationModal"
import { ThreadModerationModalAction } from "../ThreadModerationModalContext"
import ThreadModerationModalDeleteForm from "./ThreadModerationModalDeleteForm"

const ThreadModerationModalDelete: React.FC = () => (
  <ThreadModerationModal
    action={ThreadModerationModalAction.DELETE}
    title={<Trans id="moderation.delete_thread">Delete thread</Trans>}
  >
    {({ data: { thread }, close }) => {
      return <ThreadModerationModalDeleteForm thread={thread} close={close} />
    }}
  </ThreadModerationModal>
)

export default ThreadModerationModalDelete
