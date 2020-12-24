import React from "react"
import { Card, CardBanner, CardBody, CardColorBand } from "../../../UI/Card"
import { GridPageHeader } from "../../../UI/Grid"
import {
  TidbitMembers,
  TidbitPosts,
  TidbitThreads,
  Tidbits,
} from "../../../UI/Tidbits"
import { CategoryBanner } from "../../../types"

interface IThreadsHeaderProps {
  banner?: {
    full: CategoryBanner
    half: CategoryBanner
  } | null
  color?: string | null
  text: React.ReactNode
  stats?: {
    posts: number
    threads: number
    users?: number
  }
}

const ThreadsHeader: React.FC<IThreadsHeaderProps> = ({
  banner,
  color,
  text,
  stats,
}) => (
  <Card className="threads-header">
    {color && <CardColorBand color={color} />}
    {banner && <CardBanner {...banner.full} desktop />}
    {banner && <CardBanner {...banner.half} mobile />}
    <CardBody className="threads-header-body">
      <GridPageHeader
        title={text}
        tidbits={
          stats && (
            <Tidbits>
              <TidbitThreads value={stats.threads} />
              <TidbitPosts value={stats.posts} />
              {typeof stats.users !== "undefined" && (
                <TidbitMembers value={stats.users} />
              )}
            </Tidbits>
          )
        }
      />
    </CardBody>
  </Card>
)

export default React.memo(ThreadsHeader)
