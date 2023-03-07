import './janus.js'
import './adapter.js'; 
window['adapter'] = adapter;

const output1 = document.getElementById('topleft');

output1.innerHTML = "Connecting to Janus...";

const output2 = document.getElementById('topright');

Janus.init({
    debug: true,
    dependencies: Janus.useDefaultDependencies(), // or: Janus.useOldDependencies() to get the behaviour of previous Janus versions
    callback: function() {
            // Done!
    }
 });

 var opaqueId = "videoroomtest-"+Janus.randomString(12);

 let localHandle = null;
 let remoteFeed = null;
 let feedStreams = {}

 var janus = new Janus(
    {
        server: 'http://127.0.0.0:8088/janus', // 'ws://yourserver:8188/'
        success: function() {
            // Done! attach to plugin XYZ
            output1.innerHTML = 'Connected to Janus';

            janus.attach(
                {
                    plugin: "janus.plugin.videoroom",
                    opaqueId: opaqueId,
                    success: function(pluginHandle) {
                        // Plugin attached! 'pluginHandle' is our handle
                        localHandle = pluginHandle;
                        console.log("Plugin attached! (" + localHandle.getPlugin() + ", id=" + localHandle.getId() + ")");
                        console.log("  -- This is a subscriber");

                        // We wait for the plugin to send us an offer
                        let subscribe = {
                            request: "create",
                            room: 1000,
                            is_private: false
                        };
                        localHandle.send({ message: subscribe });
                        let join = {
                            request: "join",
                            room: 1000,
                            ptype: "publisher",
                        };
                        localHandle.send({ message: join });
                    },
                    error: function(cause) {
                        // Couldn't attach to the plugin
                    },
                    consentDialog: function(on) {
                        // e.g., Darken the screen if on=true (getUserMedia incoming), restore it otherwise
                    },
                    onmessage: function(msg, jsep) {
                        console.log(" ::: Got a message :::");
                        console.log(msg);
                        let event = msg["videoroom"];
                        // Handle msg, if needed, and check jsep
                        if (event === "event") {
                            if(msg["publishers"]) {
                                let list = msg["publishers"];
                                Janus.debug("Got a list of available publishers/feeds:", list);
                                let sources = null;
                                for(let f in list) {
                                    if(list[f]["dummy"])
                                        continue;
                                    let id = list[f]["id"];
                                    let display = list[f]["display"];
                                    let streams = list[f]["streams"];
                                    for(let i in streams) {
                                        let stream = streams[i];
                                        stream["id"] = id;
                                        stream["display"] = display;
                                    }
                                    let slot = feedStreams[id] ? feedStreams[id].slot : null;
                                    let remoteVideos = feedStreams[id] ? feedStreams[id].remoteVideos : 0;
                                    feedStreams[id] = {
                                        id: id,
                                        display: display,
                                        streams: streams,
                                        slot: slot,
                                        remoteVideos: remoteVideos
                                    }
                                    Janus.debug("  >> [" + id + "] " + display + ":", streams);
                                    if(!sources)
                                        sources = [];
                                    sources.push(streams);
                                }
                                subscribeToStreams(sources);
                                    
                            }
                        }
                        
                        if(jsep) {
                            // We have an OFFER from the plugin
                            streaming.createAnswer(
                                {
                                    // We attach the remote OFFER
                                    jsep: jsep,
                                    // We only specify data channels here, as this way in
                                    // case they were offered we'll enable them. Since we
                                    // don't mention audio or video tracks, we autoaccept them
                                    // as recvonly (since we won't capture anything ourselves)
                                    tracks: [
                                        { type: 'data' }
                                    ],
                                    success: function(ourjsep) {
                                        // Got our SDP! Send our ANSWER to the plugin
                                        var body = { request: "start" };
                                        streaming.send({ message: body, jsep: ourjsep });
                                    },
                                    error: function(error) {
                                        // An error occurred...
                                    }
                                });
                        }
                    },
                    onlocaltrack: function(track, added) {
                        alert('onlocaltrack');
                        // A local track to display has just been added (getUserMedia worked!) or removed
                    },
                    onremotetrack: function(track, mid, added) {
                        alert('onremotetrack');
            
                    },
                    oncleanup: function() {
                        // PeerConnection with the plugin closed, clean the UI
                        // The plugin handle is still valid so we can create a new one
                    },
                    detached: function() {
                        // Connection with the plugin closed, get rid of its features
                        // The plugin handle is not valid anymore
                    }
                });
        },
        error: function(cause) {
            // Error, can't go on...
            output1.innerHTML = 'Not onnected to Janus';

        },
        destroyed: function() {
            // I should get rid of this
            output1.innerHTML = 'Destroyed';
        }
    });

function subscribeToStreams(sources){
    console.log('subscribeToStreams');
    
    let video_feed = sources[0][1];
    console.log(video_feed);

    let subscribe = { request: 'join', ptype: 'subscriber', room: 1000, streams: [{feed: video_feed['id']}] };
    
    janus.attach(
		{
			plugin: "janus.plugin.videoroom",
			opaqueId: opaqueId,
			
            success: function(pluginHandle) {
				remoteFeed = pluginHandle;
				console.log("Plugin attached! (" + remoteFeed.getPlugin() + ", id=" + remoteFeed.getId() + ")");
				console.log("  -- This is a multistream subscriber");
				// Prepare the streams to subscribe to, as an array: we have the list of
				// streams the feed is publishing, so we can choose what to pick or skip
                console.log('subscribing: ', subscribe);                
				remoteFeed.send({ message: subscribe });
            },
            
            onmessage: function(msg, jsep) {
				console.log(" ::: Got a message (subscriber) :::", msg);
				let event = msg["videoroom"];
				
				if(msg["error"]) {
					alert(msg["error"]);
				} else if(event) {
					if(event === "attached") {
						// Now we have a working subscription, next requests will update this one
						Janus.log("Successfully attached to feed in room " + msg["room"]);
                    } else if(event === "event") {
                        
                    }
                } else {
                    // Nothing
                }

                // Request to start feed
                if(jsep) {
				    console.log("Handling SDP as well...", jsep);
					// Answer and attach
					remoteFeed.createAnswer(
						{
							jsep: jsep,
							// We only specify data channels here, as this way in
							// case they were offered we'll enable them. Since we
							// don't mention audio or video tracks, we autoaccept them
							// as recvonly (since we won't capture anything ourselves)
							tracks: [
								{ type: 'data' }
							],
							success: function(jsep) {
								console.log("Got SDP!");
								console.log(jsep);
								let body = { request: "start", room: 1000 };
								remoteFeed.send({ message: body, jsep: jsep });
							},
							error: function(error) {
								console.log("WebRTC error:", error);
								alert("WebRTC error... " + error.message);
							}
						});
				}
            },

            onremotetrack: function(track, mid, on, metadata) {
                console.log('Receiving remote track: ', track['kind']);
                if (track['kind'] === 'video') {
                    let stream = new MediaStream([track]);
                    console.log(stream.getTracks());
                    console.log(stream.getVideoTracks());
                    const videoElement = document.getElementById("remotevideo");
                    Janus.attachMediaStream(videoElement, stream);
                    console.log('width: ', videoElement.videoWidth);
                }
            },
            error: function(cause) {
                // Error, can't go on...
                console.log('ERROR: ', cause);
            },
            destroyed: function() {
                // I should get rid of this
                console.log('Destroyed');
            }

        });
    }