import React from "react"
import ThreadReplyErrorMessage from "./ThreadReplyErrorMessage"

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
    if (this.state.hasError) return <ThreadReplyErrorMessage />
    return this.props.children
  }
}

export default ThreadReplyErrorBoundary
