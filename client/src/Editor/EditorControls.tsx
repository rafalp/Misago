import { t } from "@lingui/macro"
import React from "react"
import Icon from "../UI/Icon"
import EditorButton from "./EditorButton"

interface IEditorControlsProps {
  disabled?: boolean
}

interface IEditorControl {
  key: string
  title: string
  icon: string
}

const EditorControls: React.FC<IEditorControlsProps> = ({ disabled }) => {
  const controls: Array<IEditorControl> = [
    {
      key: "bold",
      title: t({
        id: "editor.bold",
        message: "Bolder",
      }),
      icon: "fas fa-bold",
    },
    {
      key: "emphasis",
      title: t({
        id: "editor.emphasis",
        message: "Emphasize",
      }),
      icon: "fas fa-italic",
    },
    {
      key: "strikethrough",
      title: t({
        id: "editor.strikethrough",
        message: "Strikethrough",
      }),
      icon: "fas fa-strikethrough",
    },
    {
      key: "hr",
      title: t({
        id: "editor.hr",
        message: "Horizontal ruler",
      }),
      icon: "fas fa-minus",
    },
    {
      key: "link",
      title: t({
        id: "editor.link",
        message: "Link",
      }),
      icon: "fas fa-link",
    },
    {
      key: "image",
      title: t({
        id: "editor.image",
        message: "Image",
      }),
      icon: "far fa-image",
    },
    {
      key: "emoji",
      title: t({
        id: "editor.emoji",
        message: "Insert emoji",
      }),
      icon: "far fa-smile",
    },
    {
      key: "quote",
      title: t({
        id: "editor.quote",
        message: "Quote",
      }),
      icon: "fas fa-quote-right",
    },
    {
      key: "spoiler",
      title: t({
        id: "editor.spoiler",
        message: "Spoiler",
      }),
      icon: "far fa-eye-slash",
    },
    {
      key: "code",
      title: t({
        id: "editor.code",
        message: "Code",
      }),
      icon: "fas fa-code",
    },
  ]

  return (
    <div className="col-auto editor-controls">
      {controls.map(({ key, title, icon }) => (
        <EditorButton
          key={key}
          className={"btn-editor-" + key}
          disabled={disabled}
          title={title}
          icon
          onClick={() => console.log("TODO")}
        >
          <Icon icon={icon} fixedWidth />
        </EditorButton>
      ))}
    </div>
  )
}

export default EditorControls
