import React from "react"
import EmptyMessage from "./empty-message"
import Group from "./group"
import Loader from "misago/components/loader"

export default function ({
  display,
  groups,
  isAuthenticated,
  loading,
  profile,
}) {
  if (!display) return null

  if (loading) {
    return <Loader />
  }

  if (!groups.length) {
    return <EmptyMessage isAuthenticated={isAuthenticated} profile={profile} />
  }

  return (
    <div>
      {groups.map((group, i) => {
        return <Group fields={group.fields} key={i} name={group.name} />
      })}
    </div>
  )
}
