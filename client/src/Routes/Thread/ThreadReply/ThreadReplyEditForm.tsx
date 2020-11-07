import { Trans } from "@lingui/macro"
import React from "react"
import {
  PostingFormBody,
  PostingFormCollapsible,
  PostingFormDialog,
  PostingFormHeader,
} from "../../../UI/PostingForm"
import { useThreadReplyContext } from "./ThreadReplyContext"

const Editor = React.lazy(() => import("../../../Editor"))

interface IThreadReplyEditFormProps {
  threadId?: string
}

const ThreadReplyEditForm: React.FC<IThreadReplyEditFormProps> = ({
  threadId,
}) => {
  const context = useThreadReplyContext()

  if (!context) return null

  const { fullscreen, minimized, setFullscreen, setMinimized } = context

  return (
    <PostingFormDialog>
      <PostingFormBody>
        <PostingFormHeader
          fullscreen={fullscreen}
          minimized={minimized}
          setFullscreen={setFullscreen}
          setMinimized={setMinimized}
        >
          <Trans id="posting.edit">Edit post</Trans>
        </PostingFormHeader>
        <PostingFormCollapsible>
          <Editor />
        </PostingFormCollapsible>
      </PostingFormBody>
    </PostingFormDialog>
  )
}

export default ThreadReplyEditForm
