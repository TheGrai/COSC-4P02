import './App.css';
import React from "react"
import { useState } from "react";
import BUChat from "./components/BUChat";
import CGChat from "./components/CGChat";

//When running this application in IntelliJ IDEA, use the following configurations
//Create a new configuration from npm, the name is npm start, point the package.json directory to the package.json file in this source
//The command should be run, and the scripts should be start. React will start with npm and open a new page on your browser.

const styles = {
  button1: {
    backgroundColor: "#5683d6",
    borderColor: "#1D2129",
    borderStyle: "solid",
    borderRadius: 20,
    borderWidth: 2,
    color: "#1D2129",
    fontSize: 18,
    fontWeight: "300",
    paddingTop: 8,
    paddingBottom: 8,
    paddingLeft: 16,
    paddingRight: 16,
    outline: "none"
  },
  button2: {
    backgroundColor: "#f77c7c",
    borderColor: "#1D2129",
    borderStyle: "solid",
    borderRadius: 20,
    borderWidth: 2,
    color: "#1D2129",
    fontSize: 18,
    fontWeight: "300",
    paddingTop: 8,
    paddingBottom: 8,
    paddingLeft: 16,
    paddingRight: 16,
    outline: "none"
  },
  chatTitle: {

    fontSize: 18,
    fontWeight: "bold"

  }

}

function App() {
  const [isBrock, setVersion] = useState(false);

  return (
    <div className="App">
        <div class="switchButton">
          {isBrock ? <button style = {styles.button1} onClick={() => setVersion(!isBrock)}>Switch Version</button>
                  :<button style = {styles.button2} onClick={() => setVersion(!isBrock)}>Switch Version</button>}
        </div>
        { isBrock ? <BrockCB />:<CanadaGamesCB/>}
    </div>
  );
}

function BrockCB() {

  document.body.style.backgroundColor = '#ed9a9a';

  return (
    <div> 
      <p style = {styles.chatTitle}>Brock University Chat</p>
      <BUChat />
    </div>
    
  )
}

function CanadaGamesCB() {

  document.body.style.backgroundColor = '#abc5f5';

  return (
    <div> 
      <p style = {styles.chatTitle}>Canada Games Chat</p>
      <CGChat />
    </div>
  )
}
export default App;
