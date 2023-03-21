import classnames from "classnames"
import React from "react"
import onebox from "misago/services/one-box"

export default class extends React.Component {
  componentDidMount() {
    onebox.render(this.documentNode)
    $(this.documentNode).find(".spoiler-reveal").click(revealSpoiler)
  }

  componentDidUpdate(prevProps, prevState) {
    onebox.render(this.documentNode)
    $(this.documentNode).find(".spoiler-reveal").click(revealSpoiler)
  }

  shouldComponentUpdate(nextProps, nextState) {
    return nextProps.markup !== this.props.markup
  }

  render() {
    return (
      <article
        className={classnames("misago-markup", this.props.className)}
        dangerouslySetInnerHTML={{ __html: this.props.markup }}
        data-author={this.props.author || undefined}
        ref={(node) => {
          this.documentNode = node
        }}
      />
    )
  }
}

function revealSpoiler(event) {
  var btn = event.target
  $(btn).parent().parent().addClass("revealed")
}
