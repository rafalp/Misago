import React from "react"
import RootError from "../RootError"

interface IAppErrorBoundaryProps {
  children: React.ReactNode
}

class AppErrorBoundary extends React.Component<IAppErrorBoundaryProps> {
  state = { hasError: false }

  static getDerivedStateFromError() {
    return { hasError: true }
  }

  render() {
    if (this.state.hasError) return <RootError />
    return this.props.children
  }
}

export default AppErrorBoundary
