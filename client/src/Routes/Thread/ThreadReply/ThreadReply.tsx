import React from "react"
import { PostingForm } from "../../../UI/PostingForm"
import ThreadReplyEditForm from "./ThreadReplyEditForm"
import ThreadReplyErrorBoundary from "./ThreadReplyErrorBoundary"
import ThreadReplyNewForm from "./ThreadReplyNewForm"
import { useThreadReplyContext } from "./ThreadReplyContext"
import ThreadReplySpacer from "./ThreadReplySpacer"

interface ThreadReplyProps {
  threadId: string
}

const ThreadReply: React.FC<ThreadReplyProps> = ({ threadId }) => {
  const context = useThreadReplyContext()
  const [height, setHeight] = React.useState(0)
  const element = React.useRef<HTMLDivElement | null>(null)
  const { isActive, fullscreen, minimized, mode, post } = context || {}

  React.useLayoutEffect(() => {
    const interval = window.setInterval(() => {
      if (isActive && element.current) {
        setHeight(element.current.offsetHeight || 0)
      }
    }, 750)

    return () => window.clearInterval(interval)
  }, [setHeight, isActive, element])

  if (!context) return null

  return (
    <>
      <ThreadReplySpacer
        height={isActive && !fullscreen && !minimized ? height : 0}
      />
      <PostingForm
        fullscreen={fullscreen}
        minimized={minimized}
        ref={element}
        show={isActive}
      >
        <ThreadReplyErrorBoundary>
          {mode === "edit" && post ? (
            <ThreadReplyEditForm context={context} post={post} />
          ) : (
            <ThreadReplyNewForm context={context} threadId={threadId} />
          )}
        </ThreadReplyErrorBoundary>
      </PostingForm>
    </>
  )
}

export default React.memo(ThreadReply)
