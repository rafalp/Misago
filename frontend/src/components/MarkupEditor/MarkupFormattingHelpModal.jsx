import React from "react"
import formatFilesize from "../../utils/file-size"

export default function MarkupFormattingHelpModal() {
  return (
    <div className="modal-dialog modal-lg" role="document">
      <div className="modal-content">
        <div className="modal-header">
          <button
            aria-label={pgettext("modal", "Close")}
            className="close"
            data-dismiss="modal"
            type="button"
          >
            <span aria-hidden="true">&times;</span>
          </button>
          <h4 className="modal-title">
            {pgettext("markup help", "Formatting help")}
          </h4>
        </div>
        <div className="modal-body formatting-help">
          <h4>{pgettext("markup help", "Emphasis text")}</h4>
          <ExampleFormatting
            markup={pgettext("markup help", "_This text will have emphasis_")}
            result={
              <p>
                <em>
                  {pgettext("markup help", "This text will have emphasis")}
                </em>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Bold text")}</h4>
          <ExampleFormatting
            markup={pgettext("markup help", "**This text will be bold**")}
            result={
              <p>
                <strong>
                  {pgettext("markup help", "This text will be bold")}
                </strong>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Removed text")}</h4>
          <ExampleFormatting
            markup={pgettext("markup help", "~~This text will be removed~~")}
            result={
              <p>
                <del>
                  {pgettext("markup help", "This text will be removed")}
                </del>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Bold text (BBCode)")}</h4>
          <ExampleFormatting
            markup={pgettext("markup help", "[b]This text will be bold[/b]")}
            result={
              <p>
                <b>{pgettext("markup help", "This text will be bold")}</b>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Underlined text (BBCode)")}</h4>
          <ExampleFormatting
            markup={pgettext(
              "markup help",
              "[u]This text will be underlined[/u]"
            )}
            result={
              <p>
                <u>{pgettext("markup help", "This text will be underlined")}</u>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Italics text (BBCode)")}</h4>
          <ExampleFormatting
            markup={pgettext(
              "markup help",
              "[i]This text will be in italics[/i]"
            )}
            result={
              <p>
                <i>{pgettext("markup help", "This text will be in italics")}</i>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Link")}</h4>
          <ExampleFormatting
            markup="<http://example.com>"
            result={
              <p>
                <a href="#">example.com</a>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Link with text")}</h4>
          <ExampleFormatting
            markup={
              "[" +
              pgettext("markup help", "Link text") +
              "](http://example.com)"
            }
            result={
              <p>
                <a href="#">{pgettext("markup help", "Link text")}</a>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Link (BBCode)")}</h4>
          <ExampleFormatting
            markup="[url]http://example.com[/url]"
            result={
              <p>
                <a href="#">example.com</a>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Link with text (BBCode)")}</h4>
          <ExampleFormatting
            markup={
              "[url=http://example.com]" +
              pgettext("markup help", "Link text") +
              "[/url]"
            }
            result={
              <p>
                <a href="#">{pgettext("markup help", "Link text")}</a>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Image")}</h4>
          <ExampleFormatting
            markup="!(http://dummyimage.com/38/38)"
            result={
              <p>
                <img alt="" src="http://dummyimage.com/38/38" />
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Image with alternate text")}</h4>
          <ExampleFormatting
            markup={
              "![" +
              pgettext("markup help", "Image text") +
              "](http://dummyimage.com/38/38)"
            }
            result={
              <p>
                <img
                  alt={pgettext("markup help", "Image text")}
                  src="http://dummyimage.com/38/38"
                />
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Image (BBCode)")}</h4>
          <ExampleFormatting
            markup="[img]http://dummyimage.com/38/38[/img]"
            result={
              <p>
                <img alt="" src="http://dummyimage.com/38/38" />
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Mention user by their name")}</h4>
          <ExampleFormatting
            markup="@username"
            result={
              <p>
                <a href="#">@username</a>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Heading 1")}</h4>
          <ExampleFormatting
            markup={pgettext("markup help", "# First level heading")}
            result={<h1>{pgettext("markup help", "First level heading")}</h1>}
          />

          <hr />

          <h4>{pgettext("markup help", "Heading 2")}</h4>
          <ExampleFormatting
            markup={pgettext("markup help", "## Second level heading")}
            result={<h2>{pgettext("markup help", "Second level heading")}</h2>}
          />

          <hr />

          <h4>{pgettext("markup help", "Heading 3")}</h4>
          <ExampleFormatting
            markup={pgettext("markup help", "### Third level heading")}
            result={<h3>{pgettext("markup help", "Third level heading")}</h3>}
          />

          <hr />

          <h4>{pgettext("markup help", "Heading 4")}</h4>
          <ExampleFormatting
            markup={pgettext("markup help", "#### Fourth level heading")}
            result={<h4>{pgettext("markup help", "Fourth level heading")}</h4>}
          />

          <hr />

          <h4>{pgettext("markup help", "Heading 5")}</h4>
          <ExampleFormatting
            markup={pgettext("markup help", "##### Fifth level heading")}
            result={<h5>{pgettext("markup help", "Fifth level heading")}</h5>}
          />

          <hr />

          <h4>{pgettext("markup help", "Unordered list")}</h4>
          <ExampleFormatting
            markup={"- Lorem ipsum\n- Dolor met\n- Vulputate lectus"}
            result={
              <ul>
                <li>Lorem ipsum</li>
                <li>Dolor met</li>
                <li>Vulputate lectus</li>
              </ul>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Ordered list")}</h4>
          <ExampleFormatting
            markup={"1. Lorem ipsum\n2. Dolor met\n3. Vulputate lectus"}
            result={
              <ol>
                <li>Lorem ipsum</li>
                <li>Dolor met</li>
                <li>Vulputate lectus</li>
              </ol>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Quote text")}</h4>
          <ExampleFormatting
            markup={"> " + pgettext("markup help", "Quoted text")}
            result={
              <blockquote>
                <p>{pgettext("markup help", "Quoted text")}</p>
              </blockquote>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Quote text (BBCode)")}</h4>
          <ExampleFormatting
            markup={
              "[quote]\n" +
              pgettext("markup help", "Quoted text") +
              "\n[/quote]"
            }
            result={
              <aside className="quote-block">
                <div className="quote-heading">
                  {gettext("Quoted message:")}
                </div>
                <blockquote className="quote-body">
                  <p>{pgettext("markup help", "Quoted text")}</p>
                </blockquote>
              </aside>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Quote text with author (BBCode)")}</h4>
          <ExampleFormatting
            markup={
              '[quote="' +
              pgettext("markup help", "Quote author") +
              '"]\n' +
              pgettext("markup help", "Quoted text") +
              "\n[/quote]"
            }
            result={
              <aside className="quote-block">
                <div className="quote-heading">
                  {pgettext("markup help", "Quote author has written:")}
                </div>
                <blockquote className="quote-body">
                  <p>{pgettext("markup help", "Quoted text")}</p>
                </blockquote>
              </aside>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Spoiler")}</h4>
          <ExampleFormatting
            markup={
              "[spoiler]\n" +
              pgettext("markup help", "Secret text") +
              "\n[/spoiler]"
            }
            result={
              <ExampleFormattingSpoiler>
                {pgettext("markup help", "Secret text")}
              </ExampleFormattingSpoiler>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Inline code")}</h4>
          <ExampleFormatting
            markup={pgettext("markup help", "`Inline code`")}
            result={
              <p>
                <code>{pgettext("markup help", "Inline code")}</code>
              </p>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Code block")}</h4>
          <ExampleFormatting
            markup={"```\nalert" + '("Hello world!");' + "\n```"}
            result={
              <pre>
                <code className="hljs">alert("Hello world!");</code>
              </pre>
            }
          />

          <hr />

          <h4>
            {pgettext("markup help", "Code block with syntax highlighting")}
          </h4>
          <ExampleFormatting
            markup={"```python\nprint" + '("Hello world!");' + "\n```"}
            result={
              <pre>
                <code className="hljs language-python">
                  <span className="hljs-built_in">print</span>("Hello world!");
                </code>
              </pre>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Code block (BBCode)")}</h4>
          <ExampleFormatting
            markup={"[code]\nalert" + '("Hello world!");' + "\n[/code]"}
            result={
              <pre>
                <code className="hljs">alert("Hello world!");</code>
              </pre>
            }
          />

          <hr />

          <h4>
            {pgettext(
              "markup help",
              "Code block with syntax highlighting (BBCode)"
            )}
          </h4>
          <ExampleFormatting
            markup={
              '[code="python"]\nprint' + '("Hello world!");' + "\n[/code]"
            }
            result={
              <pre>
                <code className="hljs language-python">
                  <span className="hljs-built_in">print</span>("Hello world!");
                </code>
              </pre>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Horizontal rule")}</h4>
          <ExampleFormatting
            markup={"Lorem ipsum\n- - -\nDolor met"}
            result={
              <div>
                <p>Lorem ipsum</p>
                <hr />
                <p>Dolor met</p>
              </div>
            }
          />

          <hr />

          <h4>{pgettext("markup help", "Horizontal rule (BBCode)")}</h4>
          <ExampleFormatting
            markup={"Lorem ipsum\n[hr]\nDolor met"}
            result={
              <div>
                <p>Lorem ipsum</p>
                <hr />
                <p>Dolor met</p>
              </div>
            }
          />
        </div>
        <div className="modal-footer">
          <button
            className="btn btn-default"
            data-dismiss="modal"
            type="button"
          >
            {pgettext("modal", "Close")}
          </button>
        </div>
      </div>
    </div>
  )
}

function ExampleFormatting({ markup, result }) {
  return (
    <div className="formatting-help-item">
      <div className="formatting-help-item-markup">
        <pre>
          <code>{markup}</code>
        </pre>
      </div>
      <div className="formatting-help-item-preview">
        <article className="misago-markup">{result}</article>
      </div>
    </div>
  )
}

class ExampleFormattingSpoiler extends React.Component {
  constructor(props) {
    super(props)

    this.state = {
      reveal: false,
    }
  }

  render() {
    return (
      <aside
        className={
          this.state.reveal ? "spoiler-block revealed" : "spoiler-block"
        }
      >
        <blockquote className="spoiler-body">
          <p>{this.props.children}</p>
        </blockquote>
        {!this.state.reveal && (
          <div className="spoiler-overlay">
            <button
              className="spoiler-reveal"
              type="button"
              onClick={() => {
                this.setState({ reveal: true })
              }}
            >
              {gettext("Reveal spoiler")}
            </button>
          </div>
        )}
      </aside>
    )
  }
}
