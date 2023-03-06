import * as Janus from './janus.js'
import adapter from '../../node_modules/webrtc-adapter/out/adapter.js'; 
window['adapter'] = adapter;

alert('hello')

const output1 = document.getElementById('topleft');
output1.innerHTML = "Connecting to Janus...";

Janus.init({
    debug: true,
    dependencies: Janus.useDefaultDependencies(), // or: Janus.useOldDependencies() to get the behaviour of previous Janus versions
    callback: function() {
            // Done!
    }
 });

 var janus = new Janus(
    {
        server: 'http://127.0.0.0:8088/janus', // 'ws://yourserver:8188/'
        success: function() {
            // Done! attach to plugin XYZ
            output.innerHTML = 'Connected to Janus';
        },
        error: function(cause) {
            // Error, can't go on...
            output.innerHTML = 'Not onnected to Janus';

        },
        destroyed: function() {
            // I should get rid of this
            output.innerHTML = 'Destroyed';
        }
    });

janus.attach(
    {
        plugin: "janus.plugin.echotest",
        success: function(pluginHandle) {
            // Plugin attached! 'pluginHandle' is our handle
            output.innerHTML = 'Connected to Janus';

        },
        error: function(cause) {
            // Couldn't attach to the plugin
        },
        consentDialog: function(on) {
            // e.g., Darken the screen if on=true (getUserMedia incoming), restore it otherwise
        },
        onmessage: function(msg, jsep) {
            // We got a message/event (msg) from the plugin
            // If jsep is not null, this involves a WebRTC negotiation
        },
        onlocaltrack: function(track, added) {
            // A local track to display has just been added (getUserMedia worked!) or removed
        },
        onremotetrack: function(track, mid, added) {
            // A remote track (working PeerConnection!) with a specific mid has just been added or removed
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