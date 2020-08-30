import initStoryshots from "@storybook/addon-storyshots"

initStoryshots({
  storyNameRegex: /^((?!.*?No Snapshot).)*$/,
})
