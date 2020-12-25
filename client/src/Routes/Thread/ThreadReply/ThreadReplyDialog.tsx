import { Trans } from "@lingui/macro"
import React from "react"
import {
  PostingFormBody,
  PostingFormCollapsible,
  PostingFormDialog,
  PostingFormHeader,
} from "../../../UI/PostingForm"
import { useThreadReplyContext } from "./ThreadReplyContext"

interface ThreadReplyDialogProps {
  children: React.ReactNode
}

const ThreadReplyDialog: React.FC<ThreadReplyDialogProps> = ({ children }) => {
  const context = useThreadReplyContext()
  if (!context) return null

  const {
    fullscreen,
    minimized,
    setFullscreen,
    setMinimized,
    mode,
    cancelReply,
  } = context

  return (
    <PostingFormDialog>
      <PostingFormBody>
        <PostingFormHeader
          fullscreen={fullscreen}
          minimized={minimized}
          cancel={() => cancelReply()}
          setFullscreen={setFullscreen}
          setMinimized={setMinimized}
        >
          {mode === "edit" ? (
            <Trans id="posting.edit">Edit post</Trans>
          ) : (
            <Trans id="posting.reply">Reply thread</Trans>
          )}
        </PostingFormHeader>
        <PostingFormCollapsible>{children}</PostingFormCollapsible>
      </PostingFormBody>
    </PostingFormDialog>
  )
}

export default ThreadReplyDialog
