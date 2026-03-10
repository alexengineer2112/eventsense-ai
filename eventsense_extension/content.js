function loadInboxSDK(){

    const script = document.createElement("script");
    script.src = "https://www.inboxsdk.com/build/inboxsdk.js";

    script.onload = () => {
        initializeEventSense();
    };

    document.head.appendChild(script);
}

function initializeEventSense(){

    InboxSDK.load(2, "eventsense-ai").then((sdk) => {

        console.log("EventSense AI Loaded");

        const navItem = sdk.NavMenu.addNavItem({
            name: "EventSense-AI"
        });

        navItem.on("click", () => {
            openEventPopup();
        });

    });

}

function openEventPopup(){

    const name = prompt("New Event");

    if(!name) return;

    console.log("New Event:", name);

}

loadInboxSDK();