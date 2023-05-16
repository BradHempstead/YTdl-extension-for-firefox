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

function sendMsg(tab){
  curTab = tab[0].url;
  let sending = browser.runtime.sendNativeMessage(
    "ytdlfirefox",
     curTab
  );
  sending.then(onResponse, onError);
}

function getPage(){
  browser.tabs.query({currentWindow: true, active: true})
    .then(sendMsg, onError)
}

/*
On a click on the browser action, send the app a message.
*/
browser.browserAction.onClicked.addListener(() => {
  console.log("Sending:  ping");
  getPage();

});
