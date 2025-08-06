document.addEventListener("DOMContentLoaded", (event)=>{
    myVideo = document.getElementById("local_vid");
    myVideo.onloadeddata = ()=>{console.log("W,H: ", myVideo.videoWidth, ", ", myVideo.videoHeight);};
    var muteBttn = document.getElementById("bttn_mute");
    var muteVidBttn = document.getElementById("bttn_vid_mute");
    var callEndBttn = document.getElementById("call_end");

    muteBttn.addEventListener("click", (event)=>{
        audioMuted = !audioMuted;
        setAudioMuteState(audioMuted);        
    });    
    muteVidBttn.addEventListener("click", (event)=>{
        videoMuted = !videoMuted;
        setVideoMuteState(videoMuted);        
    });    
    callEndBttn.addEventListener("click", (event)=>{
        window.location.replace("/");
    });

    document.getElementById("room_link").innerHTML=`or the link: <span class="heading-mark">${window.location.href}</span>`;

});


function makeVideoElement(element_id, display_name)
{
    let wrapper_div = document.createElement("div");
    let vid_wrapper = document.createElement("div");
    let vid = document.createElement("video");
    let name_text = document.createElement("div");

    wrapper_div.id = "div_"+element_id;
    vid.id = "vid_"+element_id;

    wrapper_div.className = "shadow video-item";
    vid_wrapper.className = "vid-wrapper";
    name_text.className = "display-name";
    
    vid.autoplay = true;        
    name_text.innerText = display_name;

    vid_wrapper.appendChild(vid);
    wrapper_div.appendChild(vid_wrapper);
    wrapper_div.appendChild(name_text);

    return wrapper_div;
}

function addVideoElement(element_id, display_name)
{
    document.getElementById("video_grid").appendChild(makeVideoElement(element_id, display_name));
}

//function addVideoElement(peer_id, display_name, isLocal = false) {
//    // جلوگیری از اضافه شدن ویدئوی تکراری
////    if (document.getElementById(peer_id)) {
////        console.log(`Video element for ${peer_id} already exists, skipping...`);
////        return;
////    }
//    let videoGrid = document.getElementById("video-grid");
//    let videoElement = document.createElement("video");
//    videoElement.id = peer_id;
//    videoElement.autoplay = true;
//    videoElement.playsInline = true;
//
//    if (isLocal) {
//        videoElement.muted = true; // صدای ویدیوی محلی را قطع کن
//    }
//
//    let nameTag = document.createElement("div");
//    nameTag.innerText = display_name;
//    nameTag.classList.add("nameTag");
//
//    let videoContainer = document.createElement("div");
//    videoContainer.appendChild(videoElement);
//    videoContainer.appendChild(nameTag);
//
//    videoGrid.appendChild(videoContainer);
//}

function removeVideoElement(element_id)
{    
    let v = getVideoObj(element_id);
    if(v.srcObject){
        v.srcObject.getTracks().forEach(track => track.stop());
    }
    v.removeAttribute("srcObject");
    v.removeAttribute("src");

    document.getElementById("div_"+element_id).remove();
}

function getVideoObj(element_id)
{
    return document.getElementById("vid_"+element_id);
}

function setAudioMuteState(flag)
{
    let local_stream = myVideo.srcObject;
    local_stream.getAudioTracks().forEach((track)=>{track.enabled = !flag;});
    // switch button icon
    document.getElementById("mute_icon").innerText = (flag)? "mic_off": "mic";
}
function setVideoMuteState(flag)
{
    let local_stream = myVideo.srcObject;
    local_stream.getVideoTracks().forEach((track)=>{track.enabled = !flag;});
    // switch button icon
    document.getElementById("vid_mute_icon").innerText = (flag)? "videocam_off": "videocam";
}

function makeVideoElement(element_id, display_name) {
    let wrapper_div = document.createElement("div");
    let vid = document.createElement("video");
    let name_text = document.createElement("div");

    wrapper_div.id = "div_" + element_id;
    vid.id = "vid_" + element_id;

    vid.autoplay = true;
    vid.playsInline = true;

    wrapper_div.className = "remote-video-item";
    vid.className = "remote-video";
    name_text.className = "display-name";
    name_text.innerText = display_name;

    wrapper_div.appendChild(vid);
    wrapper_div.appendChild(name_text);

    return wrapper_div;
}

function addVideoElement(element_id, display_name) {
    document.getElementById("remote_videos").appendChild(makeVideoElement(element_id, display_name));
}

document.getElementById("bttn_location").addEventListener("click", () => {
    if (!navigator.geolocation) {
        alert("مرورگر شما از موقعیت مکانی پشتیبانی نمی‌کند.");
        return;
    }

    navigator.geolocation.getCurrentPosition(
        (position) => {
            const data = {
                latitude: position.coords.latitude,
                longitude: position.coords.longitude,
                room: currentRoom  // یا هر نام متغیر صحیحی که دارید
            };
                        alert("test2");

            socket.emit("bttn_location", data);
            console.log("📤 موقعیت ارسال شد:", data);
        },
        (error) => {
            alert("❌ دریافت موقعیت مکانی با خطا مواجه شد.");
            console.error(error);
        }
    );
});



socket.on("receive_location", (data) => {
    const { latitude, longitude } = data;

    const locationLink = document.createElement("a");
    locationLink.href = `https://www.google.com/maps?q=${latitude},${longitude}`;
    locationLink.target = "_blank";
    locationLink.textContent = "موقعیت مکانی طرف مقابل را ببینید";
    locationLink.className = "d-block my-2 text-primary";

    // نمایش در جایی مناسب مثل یک چت‌باکس یا پیام‌ها
    const messagesBox = document.getElementById("messages") || document.body;
    messagesBox.appendChild(locationLink);
});

socket.on("location_debug", (data) => {
    alert(data.message);
});
