export class Include {
  init(staticUrl) {
    this._staticUrl = staticUrl
    this._included = []
  }

  include(script, remote = false) {
    if (this._included.indexOf(script) === -1) {
      this._included.push(script)
      this._include(script, remote)
    }
  }

  _include(script, remote) {
    $.ajax({
      url: (!remote ? this._staticUrl : "") + script,
      cache: true,
      dataType: "script",
    })
  }
}

export default new Include()
