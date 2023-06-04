/*print response from native messaging to console*/
function onResponse(response) {
  console.log(`Received ${response}`);
}

/*print errors to console */
function onError(error) {
  console.log(`Error: ${error}`);
}


/*Create promise for collecting current tabs url (cheeck if used) */
function getCurrentTab() {
  let queryOptions = { active: true, lastFocusedWindow: true };
  var tabs = browser.tabs.query(queryOptions);
  console.log(tabs);
  return tabs;
}

/*send the download type and url over native message to an instanced version of the python code
then print the response or error to console */
function sendMsg(msg){
  let sending = browser.runtime.sendNativeMessage(
    "ytdlfirefox",
     msg
  );
  sending.then(onResponse, onError);
}

/*format the data string for sending to python instance and call the sendMsg function once done */
function createMsg(select, tab){
  msg = select;
  curTab = tab[0].url;
  msg = msg + " " + curTab;
  sendMsg(msg);
}

/*Get the current tab (creates promise) and then call createMsg passing it the download selection
and tab data */
function getPage(select, wack){
  browser.tabs.query({currentWindow: true, active: true})
    .then(createMsg.bind(null, select), onError)
}

/*
On a click on the browser action, send the app a message.
*/
/*
browser.browserAction.onClicked.addListener(() => {
  console.log("Sending:  ping");
  getPage("mp3 ");

});
*/

/*Add the download video context menu item */
browser.contextMenus.create({
    id: "download-from-video-youtube",
    title: "Download video from YouTube",
    contexts: ["all"],
    onclick: getPage.bind(null,"video")
});

/*Add the download audio context menu item */
browser.contextMenus.create({
    id: "download-audio-from-youtube",
    title: "Download audio from YouTube",
    contexts: ["all"],
    onclick: getPage.bind(null, "audio")
});
