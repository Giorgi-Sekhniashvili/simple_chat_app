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
            webSocket.send(JSON.stringify({
                message: this.message,
            }))
            this.message = null

        },
        getMessages() {
            fetch(`${window.location.origin}/api/chat/${privateChat}/`)
                .then(response => response.json())
                .then(data => {
                        console.log(data)
                        this.chatMessages = data
                    }
                ).catch(e => (console.log(e)))
        }
    },
    mounted() {
        this.getMessages()

        webSocket.onmessage = (event) => {
            console.log('onmessage=', event)
        }
        webSocket.onopen = () => {
            console.log('websocket is open')
        }
        webSocket.onclose = () => {
            console.log('websocket has closed')
        }
    }

})

chatApp.mount('#chat')





