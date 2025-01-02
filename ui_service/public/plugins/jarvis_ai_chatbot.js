function _jarvis_getOptions() {
	const scriptURL = new URL(document.currentScript.src);
	const target = scriptURL.searchParams.get("target") || "127.0.0.1:8080";
	const topic = scriptURL.searchParams.get("topic") || "__all__";
	const appMode = "plugin";
	const targetUrl = `http://${target}?appMode=${appMode}&topic=${topic}`;
	const logoImageUrl = `http://${target}/logo.png`;
	return {
		"target": target,
		"topic": topic,
		"appMode": appMode,
		"targetUrl": targetUrl,
		"logoImageUrl": logoImageUrl,
	}
}

function _jarvis_createChatIframe() {
	const options = _jarvis_getOptions();
	const chatIframe = document.createElement("iframe");
	chatIframe.setAttribute("src", options.targetUrl);
	chatIframe.style.width = "100%";
	chatIframe.style.height = "100%";
	chatIframe.style.border = "none";
	return chatIframe;
}

function _jarvis_createChatContainer() {
	const chatContainer = document.createElement("div");
	chatContainer.style.height = "570px";
	chatContainer.style.width = "400px";
	chatContainer.style.position = "fixed";
	chatContainer.style.overflow = "hidden";
	chatContainer.style.backgroundColor  = "white";
	chatContainer.style.display  = "none";
	chatContainer.style.bottom =  "60px";
	chatContainer.style.right = "55px";
	chatContainer.style.boxShadow = "0px 0px 15px grey";
	chatContainer.style.borderRadius = "5px";
	chatContainer.style.zIndex = "9999";
	return chatContainer;
}

function _jarvis_createChatButton() {
	const options = _jarvis_getOptions();
	const chatButton = document.createElement("div");
	chatButton.setAttribute("title", "Open JARVIS Chat.");
	chatButton.style.height = "50px";
	chatButton.style.width = "50px";
	chatButton.style.position = "fixed";
	chatButton.style.bottom =  "30px";
	chatButton.style.right = "30px";
	chatButton.style.borderRadius = "50%";
	chatButton.style.cursor = "pointer";
	chatButton.style.boxShadow = "0px 0px 15px gray";
	chatButton.style.zIndex = "9999";

	const buttonImage = document.createElement("img");
	buttonImage.setAttribute("src", options.logoImageUrl);
	buttonImage.setAttribute("alt", "JARVIS");
	buttonImage.style.width = "100%";
	buttonImage.style.height = "100%";

	chatButton.appendChild(buttonImage);

	return chatButton
}

function _jarvis_init(){
	const body = document.getElementsByTagName("body")[0];
	const iframe = _jarvis_createChatIframe();
	const container = _jarvis_createChatContainer();
	const chatButton = _jarvis_createChatButton();

	container.appendChild(iframe);
	body.appendChild(container);
	body.appendChild(chatButton);

	chatButton.onclick = function() {
		let isChatBoxVisible = container.style.display === "none";
		if (isChatBoxVisible) {
			container.style.display = "block";
			chatButton.setAttribute("title", "Close JARVIS Chat.");
		} else {
			container.style.display = "none";
			chatButton.setAttribute("title", "Open JARVIS Chat.");
		}
	};
}

_jarvis_init();