import React from "react"

interface ThreadPostsListProps {
  children: React.ReactNode
}

const ThreadPostsList: React.FC<ThreadPostsListProps> = ({ children }) => (
  <div className="thread-posts-list">{children}</div>
)

export default ThreadPostsList
