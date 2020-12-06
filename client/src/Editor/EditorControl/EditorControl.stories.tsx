import { action } from "@storybook/addon-actions"
import React from "react"
import EditorControlCodeModal from "./EditorControlCodeModal"
import EditorControlImageModal from "./EditorControlImageModal"
import EditorControlLinkModal from "./EditorControlLinkModal"
import EditorControlListModal from "./EditorControlListModal"

export default {
  title: "Editor/Controls",
}

export const InsertCodeModal = () => (
  <EditorControlCodeModal
    context={{
      disabled: false,
      textarea: null,
      getSelection: () => "",
      getValue: () => "",
      replaceSelection: action("replace selection"),
    }}
    isOpen={true}
    close={action("close modal")}
  />
)

export const InsertImageModal = () => (
  <EditorControlImageModal
    context={{
      disabled: false,
      textarea: null,
      getSelection: () => "",
      getValue: () => "",
      replaceSelection: action("replace selection"),
    }}
    isOpen={true}
    close={action("close modal")}
  />
)

export const InsertLinkModal = () => (
  <EditorControlLinkModal
    context={{
      disabled: false,
      textarea: null,
      getSelection: () => "",
      getValue: () => "",
      replaceSelection: action("replace selection"),
    }}
    isOpen={true}
    close={action("close modal")}
  />
)

export const InsertListModal = () => (
  <EditorControlListModal
    context={{
      disabled: false,
      textarea: null,
      getSelection: () => "",
      getValue: () => "",
      replaceSelection: action("replace selection"),
    }}
    isOpen={true}
    close={action("close modal")}
  />
)
