import React from "react"
import { PageError } from "../PageError"

interface IPageErrorBoundaryProps {
  children: React.ReactNode
}

class PageErrorBoundary extends React.Component<IPageErrorBoundaryProps> {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) return <PageError />
    return this.props.children
  }
}

export default PageErrorBoundary
