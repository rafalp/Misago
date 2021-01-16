import React from "react"
import Tribute from "tributejs"
import { UserSearchResult } from "./useSearchUsersQuery"
import useSearchUsersQuery from "./useSearchUsersQuery"

interface EditorMentionsProps {
  children: React.ReactNode
  mocks?: Array<UserSearchResult>
}

const EditorMentions: React.FC<EditorMentionsProps> = ({
  children,
  mocks,
}) => {
  const [initialized, setInitialized] = React.useState(false)
  const container = React.useRef<HTMLDivElement | null>(null)
  const tribute = React.useRef<Tribute<any> | null>(null)

  const searchUsers = useSearchUsersQuery()
  const element = container.current

  React.useEffect(() => {
    if (!initialized || !element || tribute.current) return

    const textarea = element.querySelector("textarea")
    if (!textarea) return

    tribute.current = new Tribute<UserSearchResult>({
      values: mocks
        ? mocks
        : (text, cb) => {
            searchUsers(text).then(cb)
          },
      selectTemplate: function (item) {
        return "@" + item.original.name
      },
      menuItemTemplate: function ({ original }) {
        const name = escapeHtml(original.name)
        const fullName = escapeHtml(original.fullName || "")
        const url = escapeHtml(original.avatar.url)

        const avatar = `<img class="user-avatar" src="${url}" alt=""/>`
        if (fullName.length) {
          return `${avatar} <span class="tribute-main">${fullName}</span><span class="tribute-sub">@${name}</span>`
        }

        return `${avatar} <span class="tribute-main">${name}</span>`
      },
      noMatchTemplate: function () {
        return '<span style:"visibility: hidden;"></span>'
      },
      searchOpts: {
        pre: "",
        post: "",
        skip: true,
      },
      itemClass: "dropdown-item",
      selectClass: "active",
    })

    tribute.current.attach(textarea)

    return () => {
      if (tribute.current) tribute.current.detach(textarea)
    }
  }, [initialized, element, mocks, searchUsers])

  return (
    <div
      className="form-editor-mentions"
      ref={(element) => {
        if (element) {
          container.current = element
          setInitialized(true)
        }
      }}
    >
      {children}
    </div>
  )
}

const escapeHtml = (value: string) => {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;")
}

export default EditorMentions
