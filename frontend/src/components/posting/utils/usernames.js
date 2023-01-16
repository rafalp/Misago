export default function (usernames) {
  const normalisedNames = usernames
    .split(",")
    .map((i) => i.trim().toLowerCase())
  const removedBlanks = normalisedNames.filter((i) => i.length > 0)
  const removedDuplicates = removedBlanks.filter((name, pos) => {
    return removedBlanks.indexOf(name) == pos
  })

  return removedDuplicates
}
