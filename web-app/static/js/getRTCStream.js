const localStream = navigator.getUserMedia({vide: true, audio: true}, );

const peerConnection = new RTCPeerConnection(iceConfig);
localStream.getTracks().forEach(track => {
    peerConnection.addTrack(track, localStream);
});