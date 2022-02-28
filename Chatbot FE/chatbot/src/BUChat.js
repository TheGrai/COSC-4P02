import React from "react";
import { ChatFeed, Message} from "react-chat-ui";

const users = {
  0: "You",
  1: "Bot"
};

class BUChat extends React.Component {
  constructor() {
    super();
    this.state = {
      messages: [
        new Message({ id: 1, message: "Hello! Welcome to the Brock University Chat Bot!", senderName: "G.R.A.N.T." }),
      ],
      useCustomBubble: false,
      curr_user: 0
    };
  }

  onMessageSubmit(e) {
    const input = this.message;
    e.preventDefault();
    if (!input.value) {
      return false;
    }
    this.pushMessage(this.state.curr_user, input.value);
    input.value = "";
    return true;
  }

  pushMessage(recipient, message) {
    const prevState = this.state;
    const newMessage = new Message({
      id: recipient,
      message,
      senderName: users[recipient]
    });
    prevState.messages.push(newMessage);
    this.setState(this.state);
  }

  render() {
    return (
      <div className="container">
        <div className="chatfeed-wrapper">
          <ChatFeed
            maxHeight={window.innerHeight - 100}
            messages={this.state.messages} // Boolean: list of message objects
            isTyping={this.state.is_typing}
            showSenderName
            bubbleStyles={{
              chatbubble: {

                backgroundColor: "#b81414"

              },
            }
            }
          />

          <form onSubmit={e => this.onMessageSubmit(e)}>
            <input
              ref={m => {
                this.message = m;
              }}
              placeholder="Type a message..."
              className="message-input"
            />
          </form>
          
        </div>
      </div>
    );
  }
}

export default BUChat;
