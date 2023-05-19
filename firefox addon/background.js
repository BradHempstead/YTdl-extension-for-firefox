function onResponse(response) {
  console.log(`Received ${response}`);
}

function onError(error) {
  console.log(`Error: ${error}`);
}



function getCurrentTab() {
  let queryOptions = { active: true, lastFocusedWindow: true };
  var tabs = browser.tabs.query(queryOptions);
  console.log(tabs);
  return tabs;
}

function sendMsg(msg){
  let sending = browser.runtime.sendNativeMessage(
    "ytdlfirefox",
     msg
  );
  sending.then(onResponse, onError);
}

function createMsg(select, tab){
  msg = select;
  curTab = tab[0].url;
  msg = msg + " " + curTab;
  sendMsg(msg);
}

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
browser.contextMenus.create({
    id: "download-from-video-youtube",
    title: "Download video from YouTube",
    contexts: ["all"],
    onclick: getPage.bind(null,"mp4")
});

browser.contextMenus.create({
    id: "download-audio-from-youtube",
    title: "Download audio from YouTube",
    contexts: ["all"],
    onclick: getPage.bind(null, "mp3")
});
