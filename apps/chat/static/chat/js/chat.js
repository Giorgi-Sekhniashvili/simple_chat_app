const privateChat = JSON.parse(document.getElementById('private_chat').textContent)
const webSocket = new ReconnectingWebSocket(`ws://${window.location.host}/ws/chat/${privateChat}/`)

const chatApp = Vue.createApp({
    data() {
        return {
            chatMessages: [],
            message: null,
        }
    },
    methods: {
        submitMessage() {
            console.log('message = ', this.message)
            this.message = null
        }
    }

})

chatApp.mount('#chat')





