export function posterShare (params = '') {
  if (window.webkit !== undefined) {
    window.webkit.messageHandlers.posterShare.postMessage(params)
  } else if (window.Send !== undefined) {
    window.Send.posterShare(params)
  }
}
