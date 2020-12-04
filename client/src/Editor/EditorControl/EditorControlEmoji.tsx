import { EmojiButton } from "@joeattardi/emoji-button"
import { t } from "@lingui/macro"
import React from "react"
import Icon from "../../UI/Icon"
import { IEditorControlProps } from "./EditorControl.types"
import EditorButton from "../EditorButton"

const EditorControlEmoji: React.FC<IEditorControlProps> = ({
  title,
  icon,
  context,
}) => {
  const picker = React.useRef<EmojiButton | null>(null)
  const { textarea, disabled, replaceSelection } = context

  React.useEffect(() => {
    if (!textarea || disabled) return

    picker.current = new EmojiButton({
      i18n: {
        search: t({
          id: "emoji_picker.search",
          message: "Search emojis...",
        }),
        categories: {
          recents: t({
            id: "emoji_picker.recents",
            message: "Recent Emojis",
          }),
          smileys: t({
            id: "emoji_picker.smileys",
            message: "Smileys & Emotion",
          }),
          people: t({
            id: "emoji_picker.people",
            message: "People & Body",
          }),
          animals: t({
            id: "emoji_picker.animals",
            message: "Animals & Nature",
          }),
          food: t({
            id: "emoji_picker.food",
            message: "Food & Drink",
          }),
          activities: t({
            id: "emoji_picker.activities",
            message: "Activities",
          }),
          travel: t({
            id: "emoji_picker.travel",
            message: "Travel & Places",
          }),
          objects: t({
            id: "emoji_picker.objects",
            message: "Objects",
          }),
          symbols: t({
            id: "emoji_picker.symbols",
            message: "Symbols",
          }),
          flags: t({
            id: "emoji_picker.flags",
            message: "Flags",
          }),
          custom: t({
            id: "emoji_picker.custom",
            message: "Custom",
          }),
        },
        notFound: t({
          id: "emoji_picker.not_found",
          message: "No emojis found",
        }),
      },
    })
    picker.current.on("emoji", ({ emoji }) =>
      replaceSelection({ replace: emoji })
    )

    return () => {
      if (picker.current) picker.current.destroyPicker()
    }
  }, [picker, textarea, disabled, replaceSelection])

  return (
    <EditorButton
      className="btn-editor-emoji"
      disabled={disabled}
      title={title}
      icon
      onClick={(event) => {
        if (picker.current) {
          picker.current.togglePicker(event.currentTarget)
        }
      }}
    >
      <Icon icon={icon} fixedWidth />
    </EditorButton>
  )
}

export default EditorControlEmoji
