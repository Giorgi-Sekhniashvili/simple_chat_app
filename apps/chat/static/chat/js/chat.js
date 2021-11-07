const privateChat = JSON.parse(document.getElementById('private_chat').textContent)
const loggedInUserId = JSON.parse(document.getElementById('logged_in_user_id').textContent)
const webSocket = new ReconnectingWebSocket(`ws://${window.location.host}/ws/chat/${privateChat}/`)


const chatApp = Vue.createApp({
    delimiters: ["[[", "]]"],
    data() {
        return {
            chatMessages: [],
            message: '',
        }
    },
    methods: {
        submitMessage() {
            console.log('message = ', this.message)
            if (this.message.length > 0) {
                webSocket.send(JSON.stringify({
                    newMessage: this.message,
                }))
                this.message = null
            }
        },
        async getMessages() {
            const response = await fetch(`${window.location.origin}/api/chat/${privateChat}/`)
            const data = await response.json()
            console.log(data)
            this.chatMessages = data
        },

        isThisMessageUsers(message) {
            return message.user === loggedInUserId;
        }
    },
    mounted() {
        this.getMessages()

        webSocket.onmessage = (event) => {
            console.log('onmessage=', event)
            const data = JSON.parse(event.data)
            this.chatMessages = [...this.chatMessages, data]
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
