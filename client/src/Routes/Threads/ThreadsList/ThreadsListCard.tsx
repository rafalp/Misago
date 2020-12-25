import React from "react"
import { Card } from "../../../UI/Card"

interface ThreadsListCardProps {
  children: React.ReactNode
}

const ThreadsListCard: React.FC<ThreadsListCardProps> = ({ children }) => (
  <Card className="threads-list">{children}</Card>
)

export default ThreadsListCard
