import React from "react"
import ThreadReplyError from "./ThreadReplyError"

interface IThreadReplyErrorBoundaryProps {
  children: React.ReactNode
}

class ThreadReplyErrorBoundary extends React.Component<
  IThreadReplyErrorBoundaryProps
> {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) return <ThreadReplyError />
    return this.props.children
  }
}

export default ThreadReplyErrorBoundary
