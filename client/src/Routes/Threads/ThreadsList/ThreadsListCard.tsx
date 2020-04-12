import React from "react"
import { Card } from "../../../UI"

interface IThreadsListCardProps {
  children: React.ReactNode
}

const ThreadsListCard: React.FC<IThreadsListCardProps> = ({ children }) => (
  <Card className="threads-list">{children}</Card>
)

export default ThreadsListCard
