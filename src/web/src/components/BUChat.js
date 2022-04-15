import React from "react";
import { ChatFeed, Message} from "react-chat-ui";
import { render } from "react-dom";
import "./style.css"

const users = {
  0: "You",
  1: "G.R.A.N.T."
};

class BUChat extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      messages: [
        new Message({ id: 1, message: "Hello! Welcome to the Brock University Chat Bot!", senderName: "G.R.A.N.T." }),
      ],
      useCustomBubble: false,
      curr_user: 0,

      active: (props.locked && props.active) || false,
      value: props.value || "",
      error: props.error || "",
      label: props.label || "Type a message..."
    };
  }

  onMessageSubmit(e) {
    const input = this.message;
    e.preventDefault();
    if (!input.value) {
      return false;
    }
    this.pushMessage(0, input.value);
    input.value = "";
    this.pushMessage(1, "Brock University 'Important Dates' page can be found at https://www.brocku.ca/important-dates" );
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
    const { active, value, error, label } = this.state;
    const { locked } = this.props;
    const fieldClassName = `field ${(locked ? active : active || value) &&
      "active"} ${locked && !active && "locked"}`;
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

                backgroundColor: "#dc4141"

              },
            }
            }
          />
          <div className={fieldClassName}>
          {active &&
            value}
            <form onSubmit={e => this.onMessageSubmit(e)}>
              <input
                ref={m => {
                  this.message = m;
                }}
                className="message-input"
                placeholder="Type a message..."
                onFocus={() => !locked && this.setState({ active: true })}
                onBlur={() => !locked && this.setState({ active: false })}
              />
              <label htmlFor={1} className={error && "error"}>
                {error || label}
              </label>
            </form>
          </div>
          
        </div>
      </div>
    );
  }
}

export default BUChat;
