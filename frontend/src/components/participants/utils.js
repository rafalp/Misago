export function getParticipantsCopy(participants) {
  const count = participants.length
  const message = npgettext(
    "thread participants stat",
    "This thread has %(users)s participant.",
    "This thread has %(users)s participants.",
    count
  )

  return interpolate(
    message,
    {
      users: count,
    },
    true
  )
}
